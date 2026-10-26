#!/usr/bin/env python3
"""Fill empty meta.platform_name from category / product-code / linked base.

Sources (in order):
  1. Same TitleID-low base (for DLC / updates)
  2. Heuristic from category + product-code type letter + region

Does not overwrite non-empty platform_name.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "utils"))
from db_paths import iter_title_dirs  # noqa: E402

DB = ROOT / "db" / "3ds"

# Virtual Console serial first letter(s) → system key
VC_SERIAL_SYSTEM = {
    "T": "nes",  # TA*, TB*, …
    "R": "gb",  # RA*, RB*, … (Game Boy)
    "Q": "gbc",  # QA*, QB*, …
    "P": "gba",  # PA*, … (GBA) — not to confuse with CTR-P media type
    "U": "snes",  # UA*, … (also KTR New3DS SNES)
    "G": "gg",  # GA*, … Game Gear
}

VC_LABELS = {
    "nes": {
        "JP": "ファミリーコンピュータ",
        "KR": "패밀리컴퓨터",
        "default": "NES",
    },
    "gb": {
        "JP": "ゲームボーイ",
        "default": "Game Boy",
    },
    "gbc": {
        "JP": "ゲームボーイカラー",
        "KR": "게임보이 컬러",
        "default": "Game Boy Color",
    },
    "gba": {
        "JP": "ゲームボーイアドバンス",
        "default": "Game Boy Advance",
    },
    "snes": {
        "JP": "スーパーファミコン",
        "default": "Super Nintendo",
    },
    "gg": {
        "JP": "ゲームギア",
        "default": "Game Gear",
    },
    "pce": {
        "JP": "PCエンジン",
        "default": "PC Engine",
    },
}


def pick_locale(region: str, table: dict[str, str]) -> str:
    region = (region or "").upper()
    if region in table:
        return table[region]
    return table["default"]


def label_dsiware(region: str) -> str:
    return pick_locale(
        region,
        {
            "JP": "ニンテンドーDSiウェア",
            "KR": "닌텐도 DSiWare",
            "default": "Nintendo DSiWare",
        },
    )


def label_update(region: str) -> str:
    return pick_locale(
        region,
        {
            "JP": "更新データ",
            "KR": "업데이트 데이터",
            "FR": "Données de mise à jour",
            "ES": "Datos de actualización",
            "DE": "Update-Daten",
            "IT": "Dati di aggiornamento",
            "default": "Update Data",
        },
    )


def label_video(region: str) -> str:
    return pick_locale(
        region,
        {
            "JP": "ニンテンドー3DSダウンロードソフト",
            "default": "Downloadable Video",
        },
    )


def label_3ds_download(region: str, *, new3ds: bool = False) -> str:
    if new3ds:
        return pick_locale(
            region,
            {
                "EU": "New 3DS (Download)",
                "default": "New 3DS Download Only",
            },
        )
    return pick_locale(
        region,
        {
            "JP": "ニンテンドー3DSダウンロードソフト",
            "EU": "Nintendo 3DS (Download)",
            "FR": "Nintendo 3DS (téléchargement)",
            "KR": "닌텐도 3DS 다운로드",
            "TW": "Nintendo 3DS 下載",
            "CN": "Nintendo 3DS 下載",
            "default": "Nintendo 3DS Download Only",
        },
    )


def label_3ds_card(region: str, *, new3ds: bool = False) -> str:
    if new3ds:
        return pick_locale(
            region,
            {
                "EU": "New 3DS (Card/Download)",
                "default": "New 3DS Retail/Download",
            },
        )
    return pick_locale(
        region,
        {
            "JP": "3DSカード/ダウンロードソフト",
            "EU": "Nintendo 3DS (Card/Download)",
            "FR": "Nintendo 3DS (carte/téléch.)",
            "DE": "Nintendo 3DS (Karte/Download)",
            "ES": "Nintendo 3DS (tarjeta/descarga)",
            "IT": "Nintendo 3DS (scheda/scaric.)",
            "KR": "3DS 카드/다운로드 소프트웨어",
            "default": "Nintendo 3DS Retail/Download",
        },
    )


def label_dlc_fallback(region: str) -> str:
    # Most DLC entries that already have a platform reuse the base 3DS label.
    return label_3ds_download(region)


def parse_pc(pc: str | None) -> tuple[str | None, str | None, str | None]:
    """platform (CTR/TWL/KTR), type letter (N/P/U/M/T), serial stem+letter."""
    pc = (pc or "").upper().strip()
    parts = [p for p in pc.split("-") if p]
    if len(parts) < 3:
        return None, None, None
    return parts[0], parts[1], parts[2]


def vc_system_from_serial(serial: str) -> str | None:
    if not serial:
        return None
    if serial.startswith("PN"):
        return "pce"
    return VC_SERIAL_SYSTEM.get(serial[0])


def infer_platform(
    *,
    category: str,
    region: str,
    product_code: str | None,
    tid: str,
) -> str | None:
    plat, kind, serial = parse_pc(product_code)
    new3ds = plat == "KTR"
    high = tid[:8].upper()

    top = category.split("/")[0]

    if top == "dsiware" or plat == "TWL" or high == "00048004":
        return label_dsiware(region)

    if top == "updates" or kind == "U" or high == "0004000E":
        return label_update(region)

    if top == "videos":
        return label_video(region)

    if top == "virtual-console":
        system = vc_system_from_serial(serial or "")
        if system and system in VC_LABELS:
            return pick_locale(region, VC_LABELS[system])
        return None

    if top == "dlc" or kind == "M" or high == "0004008C":
        # Prefer linked-base copy in caller; fallback here.
        return label_dlc_fallback(region)

    if top in ("digital-demos", "kiosk-demos") or kind == "T" or high == "00040002":
        return label_3ds_download(region, new3ds=new3ds)

    if top.startswith("extras"):
        return None  # already filled (Homebrew / ROM Hack / …)

    # base / region-free / unknown-other
    if kind == "P":
        return label_3ds_card(region, new3ds=new3ds)
    if kind in ("N", "T") or plat in ("CTR", "KTR"):
        return label_3ds_download(region, new3ds=new3ds)
    return label_3ds_download(region, new3ds=new3ds)


def load_titles() -> list[dict]:
    titles: list[dict] = []
    for cat, tid_dir in iter_title_dirs(DB, skip_themes=True):
        mp = tid_dir / "meta.json"
        if not mp.exists():
            continue
        try:
            meta = json.loads(mp.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        tid = tid_dir.name.upper()
        titles.append(
            {
                "tid": tid,
                "low": tid[8:],
                "high": tid[:8],
                "category": cat,
                "path": mp,
                "meta": meta,
                "region": (meta.get("region") or "").upper(),
                "pc": meta.get("product_code"),
                "platform_name": (meta.get("platform_name") or "").strip(),
            }
        )
    return titles


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = load_titles()
    by_low: dict[str, list[dict]] = defaultdict(list)
    for t in titles:
        by_low[t["low"]].append(t)

    stats: dict[str, int] = defaultdict(int)
    actions: list[str] = []

    for t in titles:
        if t["platform_name"]:
            continue

        value: str | None = None
        source = "heuristic"

        # Updates always get the update label (not the base game platform).
        if t["high"] == "0004000E" or t["category"] == "updates":
            value = label_update(t["region"])
            source = "heuristic:update"
        # DLC / demos: prefer platform from the linked application (same UniqueID).
        elif t["high"] in ("0004008C", "00040002"):
            for sib in by_low[t["low"]]:
                if sib["tid"] == t["tid"]:
                    continue
                if sib["high"] == "00040000" and sib["platform_name"]:
                    value = sib["platform_name"]
                    source = f"base:{sib['tid']}"
                    break

        if value is None:
            value = infer_platform(
                category=t["category"],
                region=t["region"],
                product_code=t["pc"],
                tid=t["tid"],
            )
            source = "heuristic"

        if not value:
            stats["skipped"] += 1
            continue

        stats["filled"] += 1
        stats[f"src:{source.split(':')[0]}"] += 1
        stats[f"cat:{t['category'].split('/')[0]}"] += 1
        actions.append(f"{t['category']}/{t['tid']} <- {value!r} ({source})")

        if not args.dry_run:
            t["meta"]["platform_name"] = value
            t["path"].write_text(
                json.dumps(t["meta"], ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    print(f"dry_run={args.dry_run}")
    for k in sorted(stats):
        print(f"  {k}: {stats[k]}")
    print(f"actions: {len(actions)}")
    for line in actions[:30]:
        print(f"  {line}")
    if len(actions) > 30:
        print(f"  ... +{len(actions) - 30} more")


if __name__ == "__main__":
    main()
