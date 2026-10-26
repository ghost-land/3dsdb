"""Helpers to walk db/3ds title folders (including nested extras/*)."""

from __future__ import annotations

import re
from pathlib import Path

TID_RE = re.compile(r"^[0-9A-Fa-f]{16}$")

# Known extras subcategories under db/3ds/extras/
EXTRAS_SUBS = (
    "custom-dsiware",
    "devapps-misc",
    "hb",
    "rom-hacks",
    "translated-games",
)


def iter_title_dirs(db_root: Path, *, skip_themes: bool = True):
    """Yield (category_key, tid_dir) for every title folder.

    category_key is e.g. ``base`` or ``extras/hb``.

    Themes are skipped by default: theme installer packs often share one
    TID / product code, so they are not tracked in this DB for now.
    """
    db_root = Path(db_root)
    for cat in sorted(db_root.iterdir()):
        if not cat.is_dir():
            continue
        if skip_themes and cat.name == "themes":
            continue
        if cat.name == "extras":
            for sub in EXTRAS_SUBS:
                sub_dir = cat / sub
                if not sub_dir.is_dir():
                    continue
                for tid_dir in sub_dir.iterdir():
                    if tid_dir.is_dir() and TID_RE.fullmatch(tid_dir.name):
                        yield f"extras/{sub}", tid_dir
            # Any unexpected loose TID still directly under extras/
            for tid_dir in cat.iterdir():
                if tid_dir.is_dir() and TID_RE.fullmatch(tid_dir.name):
                    yield "extras", tid_dir
            continue
        for tid_dir in cat.iterdir():
            if tid_dir.is_dir() and TID_RE.fullmatch(tid_dir.name):
                yield cat.name, tid_dir
