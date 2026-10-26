#!/usr/bin/env python3
"""Audit what is still missing / incomplete in db/3ds.

Writes under missing_db/3ds/:
  - missing_<category>.txt  — TIDs from the seed lists that are still absent
  - incomplete.json         — titles present in DB but missing media / thin meta
  - summary.json            — counts

Seed lists = existing missing_*.txt (known wanted TIDs). Re-run after fills
to refresh the picture; does not invent new absent TIDs without a seed.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "utils"))
from db_paths import EXTRAS_SUBS, TID_RE, iter_title_dirs  # noqa: E402

DB = ROOT / "db" / "3ds"
OUT = ROOT / "missing_db" / "3ds"

MEDIA = ("icon.jpg", "banner.jpg", "top_image.jpg")
META_TEXT = ("name", "description", "product_code", "region", "publisher")

# category key in missing_*.txt → db folder / walk rule
CATEGORY_FOLDERS = {
    "base": "base",
    "dlc": "dlc",
    "dsiware": "dsiware",
    "updates": "updates",
    "videos": "videos",
    "virtual-console": "virtual-console",
    "themes": "themes",
    "extras": "extras",
}


def find_tid_dir(category: str, tid: str) -> Path | None:
    tid = tid.upper()
    if category == "extras":
        extras = DB / "extras"
        if not extras.is_dir():
            return None
        for sub in EXTRAS_SUBS:
            p = extras / sub / tid
            if p.is_dir():
                return p
        p = extras / tid
        return p if p.is_dir() else None
    folder = CATEGORY_FOLDERS.get(category)
    if not folder:
        return None
    p = DB / folder / tid
    return p if p.is_dir() else None


def load_seed_tids(category: str) -> list[str]:
    path = OUT / f"missing_{category}.txt"
    if not path.exists():
        return []
    tids: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        tid = line.strip().upper()
        if TID_RE.fullmatch(tid) and tid not in seen:
            seen.add(tid)
            tids.append(tid)
    return tids


def audit_incomplete() -> dict[str, list[dict]]:
    """Walk DB and list titles missing media or thin meta fields."""
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for cat_key, tid_dir in iter_title_dirs(DB, skip_themes=False):
        meta: dict = {}
        mp = tid_dir / "meta.json"
        if mp.exists():
            try:
                meta = json.loads(mp.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                meta = {}

        missing_media = [name for name in MEDIA if not (tid_dir / name).is_file()]
        thin_meta = [
            key
            for key in META_TEXT
            if not str(meta.get(key) or "").strip()
        ]
        no_uid = not str(meta.get("uid") or "").strip()
        no_screens = not (tid_dir / "screenshots").is_dir() or not any(
            (tid_dir / "screenshots").glob("*.jpg")
        )

        if not missing_media and not thin_meta and not no_uid and not no_screens:
            continue

        top = cat_key.split("/")[0]
        entry = {
            "tid": tid_dir.name.upper(),
            "category": cat_key,
            "missing_media": missing_media,
            "thin_meta": thin_meta,
            "missing_uid": no_uid,
            "missing_screenshots": no_screens,
        }
        by_cat[top].append(entry)

    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: x["tid"])
    return dict(sorted(by_cat.items()))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--no-seed-refresh",
        action="store_true",
        help="Do not rewrite missing_*.txt (only write incomplete/summary)",
    )
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)

    still_absent: dict[str, list[str]] = {}
    recovered: dict[str, int] = {}

    for category in CATEGORY_FOLDERS:
        seed = load_seed_tids(category)
        if not seed and not (OUT / f"missing_{category}.txt").exists():
            continue
        absent = [tid for tid in seed if find_tid_dir(category, tid) is None]
        still_absent[category] = absent
        recovered[category] = len(seed) - len(absent)

        if not args.no_seed_refresh:
            path = OUT / f"missing_{category}.txt"
            path.write_text(
                "".join(f"{tid}\n" for tid in absent),
                encoding="utf-8",
            )

    incomplete = audit_incomplete()
    incomplete_counts = {
        cat: {
            "titles": len(items),
            "missing_icon": sum(1 for i in items if "icon.jpg" in i["missing_media"]),
            "missing_banner": sum(1 for i in items if "banner.jpg" in i["missing_media"]),
            "missing_top_image": sum(
                1 for i in items if "top_image.jpg" in i["missing_media"]
            ),
            "missing_uid": sum(1 for i in items if i["missing_uid"]),
            "missing_screenshots": sum(1 for i in items if i["missing_screenshots"]),
            "thin_meta": sum(1 for i in items if i["thin_meta"]),
        }
        for cat, items in incomplete.items()
    }

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "absent_from_db": {cat: len(tids) for cat, tids in still_absent.items()},
        "recovered_since_seed": recovered,
        "incomplete_in_db": incomplete_counts,
    }

    (OUT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (OUT / "incomplete.json").write_text(
        json.dumps(incomplete, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    # Keep missing.json as a tiny pointer to summary for old habits.
    (OUT / "missing.json").write_text(
        json.dumps(
            {"absent_from_db": summary["absent_from_db"], "see": "summary.json"},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"wrote {OUT}/summary.json, incomplete.json, missing_*.txt")


if __name__ == "__main__":
    main()
