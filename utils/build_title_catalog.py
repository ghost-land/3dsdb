#!/usr/bin/env python3
"""Build a hyper-organized title catalog for frontend consumption.

Groups the same game across regions (product-code serial), and for each
regional SKU attaches related content:

  base / virtual-console / dsiware / region-free
    └─ update   (same TitleID low, high 0004000E)
    └─ dlc      (same TitleID low, high 0004008C)
    └─ demos    (same serial + region when possible)
    └─ extras   (rom-hacks / translations sharing serial)

Region labeling (hybrid):
  - ``region``       ← meta.region (SKU / locale pick: FR vs US vs JP)
  - ``market``       ← product-code letter (console market: JP/US/EU/KR/TW/CN)
  - ``region_conflict`` when meta market ≠ letter market

Output: data/title_catalog.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "utils"))
from db_paths import iter_title_dirs  # noqa: E402

DB = ROOT / "db" / "3ds"
DEFAULT_OUT = ROOT / "data" / "title_catalog.json"

# Primary hubs that become catalog titles.
PRIMARY_CATEGORIES = {
    "base": "game",
    "region-free": "game",
    "virtual-console": "virtual-console",
    "dsiware": "dsiware",
}

RELATED_ROLES = ("update", "dlc", "demo", "extra")

NAME_REGION_PRIORITY = (
    "US",
    "GB",
    "EU",
    "AU",
    "CA",
    "FR",
    "DE",
    "ES",
    "IT",
    "NL",
    "FREE",
    "JP",
    "KR",
    "TW",
    "CN",
    "RU",
)

# Product-code region letter → console / cartridge market.
LETTER_TO_MARKET = {
    "J": "JP",
    "E": "US",
    "P": "EU",
    "K": "KR",
    "W": "TW",
    "C": "CN",
    # EU language-specific SKUs (still Europe console market)
    "F": "EU",
    "D": "EU",
    "I": "EU",
    "S": "EU",
    "H": "EU",
    "U": "EU",
    "X": "EU",
    "Y": "EU",
    "Z": "EU",
    "A": "EU",
    "V": "EU",
    "T": "EU",
    "B": "EU",
    "L": "EU",
    "M": "EU",
    "N": "EU",
    "R": "EU",
}

# meta.region country shops that still belong to the EU console market.
EU_COUNTRY_REGIONS = frozenset(
    {"FR", "DE", "ES", "IT", "NL", "GB", "AU", "BE", "PT", "RU"}
)

BR_TAG_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

# TitleID high → role when category alone is ambiguous.
HIGH_ROLE = {
    "0004000E": "update",
    "0004008C": "dlc",
    "00040002": "demo",
}


def clean_name(raw: str | None) -> str:
    if not raw:
        return ""
    text = BR_TAG_RE.sub(" ", raw)
    text = HTML_TAG_RE.sub("", text)
    return WS_RE.sub(" ", text).strip()


def parse_product_code(pc: str | None) -> tuple[str | None, str | None, str | None]:
    """Return (platform, serial_stem, region_letter).

    CTR-N-AMKE → (CTR, AMK, E)
    CTR-M-ABEP-00 → (CTR, ABE, P)
    TWL-N-KG9J → (TWL, KG9, J)
    """
    pc = (pc or "").upper().strip()
    if not pc:
        return None, None, None
    parts = [p for p in pc.split("-") if p]
    if len(parts) < 3:
        return None, None, None
    platform = parts[0]
    serial = parts[2]
    if len(serial) < 3:
        return None, None, None
    letter = serial[-1]
    stem = serial[:-1]
    return platform, stem, letter


def meta_to_market(region: str) -> str | None:
    """Collapse meta.region to a console-level market for conflict checks."""
    if not region or region == "UNKNOWN":
        return None
    if region == "FREE":
        return "FREE"
    if region in EU_COUNTRY_REGIONS:
        return "EU"
    if region == "CA":
        return "US"
    return region


def resolve_region_fields(
    *, region: str, letter: str | None, category: str
) -> dict[str, Any]:
    """Hybrid region labeling for catalog entries.

    - region: always meta.region (SKU / locale selection)
    - market: product-code letter when known (console market)
    - region_conflict: meta-implied market ≠ letter market
    """
    if region == "FREE" or category == "region-free":
        return {
            "region": "FREE",
            "market": "FREE",
            "region_source": "meta",
            "region_conflict": False,
        }

    letter_market = LETTER_TO_MARKET.get(letter) if letter else None
    implied = meta_to_market(region)

    if letter_market is None:
        return {
            "region": region,
            "market": implied,
            "region_source": "meta",
            "region_conflict": False,
        }

    conflict = bool(implied and implied != letter_market)
    return {
        "region": region,
        "market": letter_market,
        "region_source": "meta",
        "region_conflict": conflict,
    }


def tid_parts(tid: str) -> tuple[str, str]:
    tid = tid.upper()
    return tid[:8], tid[8:]


def classify(cat: str, high: str) -> str | None:
    """Map folder + TitleID high to a catalog role."""
    if high in HIGH_ROLE:
        return HIGH_ROLE[high]
    if cat in PRIMARY_CATEGORIES:
        return "primary"
    if cat in ("digital-demos", "kiosk-demos"):
        return "demo"
    if cat == "updates":
        return "update"
    if cat == "dlc":
        return "dlc"
    if cat.startswith("extras/"):
        return "extra"
    return None


def entry_from_meta(tid: str, cat: str, meta: dict) -> dict[str, Any]:
    pc = (meta.get("product_code") or "").upper().strip() or None
    platform, serial, letter = parse_product_code(pc)
    region = (meta.get("region") or "").upper().strip() or "UNKNOWN"
    fields = resolve_region_fields(region=region, letter=letter, category=cat)
    return {
        "tid": tid.upper(),
        "category": cat,
        "product_code": pc,
        "platform": platform,
        "serial": serial,
        "pc_letter": letter,
        "name": clean_name(meta.get("name") or meta.get("formal_name")) or None,
        "uid": meta.get("uid") or None,
        "version": meta.get("version") or None,
        **fields,
    }


def load_db() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cat, tid_dir in iter_title_dirs(DB, skip_themes=True):
        high, low = tid_parts(tid_dir.name)
        role = classify(cat, high)
        if role is None:
            continue
        meta: dict = {}
        mp = tid_dir / "meta.json"
        if mp.exists():
            try:
                meta = json.loads(mp.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                meta = {}
        row = entry_from_meta(tid_dir.name, cat, meta)
        row["role"] = role
        row["high"] = high
        row["low"] = low
        row["kind"] = PRIMARY_CATEGORIES.get(cat)
        rows.append(row)
    return rows


def pick_name(candidates: list[dict[str, Any]]) -> str:
    by_region = {e["region"]: e for e in candidates if e.get("name")}
    for region in NAME_REGION_PRIORITY:
        if region in by_region:
            return by_region[region]["name"]
    for e in candidates:
        if e.get("name"):
            return e["name"]
    return candidates[0]["tid"] if candidates else ""


def slim(e: dict[str, Any], *, with_version: bool = False) -> dict[str, Any]:
    out: dict[str, Any] = {
        "tid": e["tid"],
        "category": e["category"],
        "product_code": e.get("product_code"),
        "name": e.get("name"),
        "region": e.get("region"),
        "market": e.get("market"),
        "region_source": e.get("region_source") or "meta",
        "region_conflict": bool(e.get("region_conflict")),
    }
    if e.get("uid"):
        out["uid"] = e["uid"]
    if with_version and e.get("version"):
        out["version"] = e["version"]
    return out


def recompute_counts(releases: dict[str, list]) -> dict[str, int]:
    return {
        "skus": sum(len(v) for v in releases.values()),
        "regions": len(releases),
        "updates": sum(1 for skus in releases.values() for s in skus if s["update"]),
        "dlc": sum(len(s["dlc"]) for skus in releases.values() for s in skus),
        "demos": sum(len(s["demos"]) for skus in releases.values() for s in skus),
        "extras": sum(len(s["extras"]) for skus in releases.values() for s in skus),
    }


def build_catalog(rows: list[dict[str, Any]]) -> dict[str, Any]:
    primaries = [r for r in rows if r["role"] == "primary" and r["serial"] and r["platform"]]
    related = [r for r in rows if r["role"] in RELATED_ROLES]

    # TitleID low → related rows (update / dlc primarily).
    by_low: dict[str, list[dict]] = defaultdict(list)
    for r in related:
        if r["role"] in ("update", "dlc"):
            by_low[r["low"]].append(r)

    demos = [r for r in related if r["role"] == "demo"]
    extras = [r for r in related if r["role"] == "extra"]

    # serial key → soft links when TID-low match fails.
    demos_by_serial: dict[tuple[str, str], list[dict]] = defaultdict(list)
    extras_by_serial: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in demos:
        if r["platform"] and r["serial"]:
            demos_by_serial[(r["platform"], r["serial"])].append(r)
    for r in extras:
        if r["platform"] and r["serial"]:
            extras_by_serial[(r["platform"], r["serial"])].append(r)

    # Group primaries into title families.
    families: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for p in primaries:
        kind = p["kind"] or "game"
        families[(kind, p["platform"], p["serial"])].append(p)

    # Primary low → (title_id, region, sku dict) for hard demo attachment.
    primary_by_low: dict[str, tuple[str, str, dict]] = {}

    titles: list[dict[str, Any]] = []
    tid_index: dict[str, dict[str, Any]] = {}
    claimed_related: set[str] = set()
    title_map: dict[str, dict] = {}

    def index_tid(
        tid: str,
        title_id: str,
        region: str,
        role: str,
        entry: dict[str, Any] | None = None,
    ) -> None:
        info: dict[str, Any] = {"title": title_id, "region": region, "role": role}
        if entry is not None:
            if entry.get("market") is not None:
                info["market"] = entry["market"]
            info["region_conflict"] = bool(entry.get("region_conflict"))
        tid_index[tid] = info

    def ensure_region_sku(
        skus_by_region: dict[str, list], region: str
    ) -> dict[str, Any]:
        """Get first SKU for region, or create a demos-only stub."""
        if region in skus_by_region and skus_by_region[region]:
            return skus_by_region[region][0]
        stub = {
            "base": None,
            "update": None,
            "dlc": [],
            "demos": [],
            "extras": [],
        }
        skus_by_region[region].append(stub)
        return stub

    for (kind, platform, serial), members in sorted(families.items()):
        title_id = f"{kind}/{platform}:{serial}"
        skus_by_region: dict[str, list[dict]] = defaultdict(list)

        for primary in sorted(members, key=lambda x: (x["region"], x["tid"])):
            region = primary["region"]
            update = None
            dlcs: list[dict] = []
            for rel in sorted(by_low.get(primary["low"], []), key=lambda x: x["tid"]):
                if rel["tid"] in claimed_related:
                    continue
                if rel["role"] == "update" and update is None:
                    update = slim(rel, with_version=True)
                    claimed_related.add(rel["tid"])
                    index_tid(rel["tid"], title_id, region, "update", update)
                elif rel["role"] == "dlc":
                    dlc_entry = slim(rel, with_version=True)
                    dlcs.append(dlc_entry)
                    claimed_related.add(rel["tid"])
                    index_tid(rel["tid"], title_id, region, "dlc", dlc_entry)

            base_entry = slim(primary)
            sku = {
                "base": base_entry,
                "update": update,
                "dlc": dlcs,
                "demos": [],
                "extras": [],
            }
            skus_by_region[region].append(sku)
            index_tid(primary["tid"], title_id, region, "base", base_entry)
            primary_by_low[primary["low"]] = (title_id, region, sku)

        title_obj = {
            "id": title_id,
            "kind": kind,
            "platform": platform,
            "serial": serial,
            "name": pick_name(members),
            "regions": [],
            "markets": [],
            "counts": {},
            "releases": skus_by_region,
        }
        titles.append(title_obj)
        title_map[title_id] = title_obj

    # Pass 2: hard-link demos via TitleID low (base_low + 1).
    # Trust the UniqueID link over meta.region — many demos are miscategorized as EU.
    for demo in sorted(demos, key=lambda x: x["tid"]):
        if demo["tid"] in claimed_related or demo["tid"] in tid_index:
            continue
        target = None
        di = int(demo["low"], 16)
        for candidate in (f"{di - 1:08X}", demo["low"]):
            if candidate in primary_by_low:
                target = primary_by_low[candidate]
                break
        if target is None:
            fam = di & 0xFFFFFF00
            for blow, info in primary_by_low.items():
                if (int(blow, 16) & 0xFFFFFF00) == fam:
                    target = info
                    break
        if target is None:
            continue
        title_id, region, sku = target
        demo_entry = slim(demo)
        sku["demos"].append(demo_entry)
        claimed_related.add(demo["tid"])
        index_tid(demo["tid"], title_id, region, "demo", demo_entry)

    # Pass 3: soft-link remaining demos / extras by serial + region (no cross-region dump).
    for title_id, t in title_map.items():
        platform, serial = t["platform"], t["serial"]
        skus_by_region = t["releases"]

        for rel in sorted(
            demos_by_serial.get((platform, serial), [])
            + extras_by_serial.get((platform, serial), []),
            key=lambda x: (x["role"], x["region"], x["tid"]),
        ):
            if rel["tid"] in claimed_related or rel["tid"] in tid_index:
                continue
            region = rel["region"]
            sku = ensure_region_sku(skus_by_region, region)
            bucket = "demos" if rel["role"] == "demo" else "extras"
            entry = slim(rel)
            sku[bucket].append(entry)
            claimed_related.add(rel["tid"])
            index_tid(rel["tid"], title_id, region, rel["role"], entry)

        # Freeze releases as plain sorted dict + counts.
        releases = {
            region: skus
            for region, skus in sorted(skus_by_region.items(), key=lambda x: x[0])
        }
        t["releases"] = releases
        t["regions"] = sorted(releases.keys())
        t["markets"] = sorted(
            {
                s["base"]["market"]
                for skus in releases.values()
                for s in skus
                if s.get("base") and s["base"].get("market")
            }
        )
        t["counts"] = recompute_counts(releases)

    # Orphan updates/DLC whose primary app is missing from the DB still get a stub title.
    orphans_by_key: dict[tuple[str, str, str], dict[str, list]] = defaultdict(
        lambda: defaultdict(list)
    )
    for r in related:
        if r["tid"] in claimed_related or r["tid"] in tid_index:
            continue
        if r["role"] not in ("update", "dlc"):
            continue
        if not r["platform"] or not r["serial"]:
            continue
        # Prefer kind=game stubs for CTR orphans.
        kind = "dsiware" if r["platform"] == "TWL" else "game"
        key = (kind, r["platform"], r["serial"])
        orphans_by_key[key][r["region"]].append(r)

    for (kind, platform, serial), by_region in sorted(orphans_by_key.items()):
        title_id = f"{kind}/{platform}:{serial}"
        # Skip if a real title already claimed this id.
        if any(t["id"] == title_id for t in titles):
            # Attach remaining into existing title as region stubs without base.
            existing = next(t for t in titles if t["id"] == title_id)
            for region, items in sorted(by_region.items()):
                sku = {
                    "base": None,
                    "update": None,
                    "dlc": [],
                    "demos": [],
                    "extras": [],
                }
                for rel in sorted(items, key=lambda x: x["tid"]):
                    if rel["tid"] in tid_index:
                        continue
                    if rel["role"] == "update" and sku["update"] is None:
                        upd = slim(rel, with_version=True)
                        sku["update"] = upd
                        index_tid(rel["tid"], title_id, region, "update", upd)
                    elif rel["role"] == "dlc":
                        dlc_entry = slim(rel, with_version=True)
                        sku["dlc"].append(dlc_entry)
                        index_tid(rel["tid"], title_id, region, "dlc", dlc_entry)
                if sku["update"] or sku["dlc"]:
                    existing["releases"].setdefault(region, []).append(sku)
            existing["regions"] = sorted(existing["releases"].keys())
            existing["markets"] = sorted(
                {
                    s["base"]["market"]
                    for skus in existing["releases"].values()
                    for s in skus
                    if s.get("base") and s["base"].get("market")
                }
            )
            existing["counts"] = recompute_counts(existing["releases"])
            continue

        releases: dict[str, list] = {}
        name_src: list[dict] = []
        for region, items in sorted(by_region.items()):
            sku = {
                "base": None,
                "update": None,
                "dlc": [],
                "demos": [],
                "extras": [],
            }
            for rel in sorted(items, key=lambda x: x["tid"]):
                name_src.append(rel)
                if rel["role"] == "update" and sku["update"] is None:
                    upd = slim(rel, with_version=True)
                    sku["update"] = upd
                    index_tid(rel["tid"], title_id, region, "update", upd)
                elif rel["role"] == "dlc":
                    dlc_entry = slim(rel, with_version=True)
                    sku["dlc"].append(dlc_entry)
                    index_tid(rel["tid"], title_id, region, "dlc", dlc_entry)
            releases[region] = [sku]

        titles.append(
            {
                "id": title_id,
                "kind": kind,
                "platform": platform,
                "serial": serial,
                "name": pick_name(name_src),
                "regions": sorted(releases.keys()),
                "markets": sorted(
                    {
                        s["update"]["market"]
                        for skus in releases.values()
                        for s in skus
                        if s.get("update") and s["update"].get("market")
                    }
                    | {
                        d["market"]
                        for skus in releases.values()
                        for s in skus
                        for d in s.get("dlc") or []
                        if d.get("market")
                    }
                ),
                "incomplete": True,
                "counts": recompute_counts(releases),
                "releases": releases,
            }
        )

    titles.sort(key=lambda t: (t["kind"], t["name"].lower(), t["id"]))

    multi_region = sum(1 for t in titles if len(t["regions"]) > 1)
    with_related = sum(
        1
        for t in titles
        if t["counts"]["updates"] or t["counts"]["dlc"] or t["counts"]["demos"]
    )
    region_conflicts = sum(
        1 for info in tid_index.values() if info.get("region_conflict")
    )

    return {
        "version": 3,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "region_fallback": list(NAME_REGION_PRIORITY),
        "kinds": ["game", "virtual-console", "dsiware"],
        "region_fields": {
            "region": "meta.region — SKU / locale pick (FR vs US vs JP)",
            "market": "product-code letter — console market (JP/US/EU/KR/TW/CN/FREE)",
            "region_conflict": "true when meta-implied market ≠ letter market",
        },
        "stats": {
            "titles": len(titles),
            "multi_region_titles": multi_region,
            "titles_with_related": with_related,
            "indexed_tids": len(tid_index),
            "region_conflicts": region_conflicts,
            "primaries": len(primaries),
            "related_rows": len(related),
        },
        "titles": titles,
        "tid_index": tid_index,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    rows = load_db()
    catalog = build_catalog(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    s = catalog["stats"]
    print(
        f"wrote {args.output} titles={s['titles']} multi_region={s['multi_region_titles']} "
        f"with_related={s['titles_with_related']} tids={s['indexed_tids']}"
    )


if __name__ == "__main__":
    main()
