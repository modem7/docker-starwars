#!/usr/bin/env python3
"""Checks whether src/index.html's embedded film data matches what's
currently live at https://www.asciimation.co.nz/Blinkenlights/.

Exit 0: up to date.
Exit 1: stale, or the fetch/parse failed.

Run manually, or on a schedule via
.github/workflows/content-freshness.yml.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from asciimation_sync import (  # noqa: E402
    extract_film_block,
    extract_last_scene_note,
    fetch_live_page,
    film_hash,
)

INDEX_PATH = pathlib.Path(__file__).resolve().parent.parent / "src" / "index.html"


def main() -> int:
    local = INDEX_PATH.read_bytes()
    try:
        local_block = extract_film_block(local)
    except ValueError as exc:
        print(f"::error::could not parse local film block: {exc}")
        return 1

    try:
        live = fetch_live_page()
        live_block = extract_film_block(live)
    except Exception as exc:  # noqa: BLE001 - report and fail either way
        print(f"::error::could not fetch/parse upstream page: {exc}")
        return 1

    local_hash, live_hash = film_hash(local_block), film_hash(live_block)
    if local_hash == live_hash:
        print("Film data is up to date with upstream.")
        return 0

    print("::warning::Local film data is stale compared to upstream.")
    print(f"  local sha256:    {local_hash}  ({len(local_block)} bytes)")
    print(f"  upstream sha256: {live_hash}  ({len(live_block)} bytes)")
    note = extract_last_scene_note(live)
    if note is not None:
        print(f"  upstream latest scene: {note[0]} ({note[1]})")
    print("Run scripts/update_film_data.py to refresh, then rebuild/test before committing.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
