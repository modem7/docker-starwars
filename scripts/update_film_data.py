#!/usr/bin/env python3
"""Pull the current animation data from
https://www.asciimation.co.nz/Blinkenlights/ and splice it into
src/index.html, leaving all engine code untouched.

Deliberately does NOT pull in upstream's Google AdSense block, Google
Analytics snippet, or links to pages we don't mirror locally
(ascii_faq.html, projects.html, the legacy Java applet page, etc.) -
only the film data and the "Last scene added" footer note are synced.

Usage:
    python3 scripts/update_film_data.py

Review the diff, rebuild/test the image, then commit if it looks right.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from asciimation_sync import (  # noqa: E402
    extract_film_block,
    extract_last_scene_note,
    fetch_live_page,
    film_hash,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "src" / "index.html"

# Matches the two-line footer note as it appears in our own index.html
# (added when the film data was last refreshed) so it can be swapped
# for upstream's current text in the same style.
_LOCAL_NOTE_RE = re.compile(
    rb'(Last scene added:\s*)(.*?)(</font><br/>\s*<font size=\+0 face="Arial">\s*)(.*?)(\s*</font>)',
    re.DOTALL,
)


def main() -> int:
    local = INDEX_PATH.read_bytes()
    local_block = extract_film_block(local)

    print("Fetching current content from upstream...")
    live = fetch_live_page()
    live_block = extract_film_block(live)

    if film_hash(local_block) == film_hash(live_block):
        print("Film data is already up to date - nothing to do.")
        return 0

    updated = local.replace(local_block, live_block, 1)

    note = extract_last_scene_note(live)
    if note is not None:
        scene, date = note
        updated, n = _LOCAL_NOTE_RE.subn(
            lambda m: m.group(1) + scene.encode() + m.group(3) + date.encode() + m.group(5),
            updated,
            count=1,
        )
        if n == 0:
            print(f"(Could not find a local footer note to update - upstream's is: {scene!r} / {date!r})")

    INDEX_PATH.write_bytes(updated)

    print(f"Updated {INDEX_PATH.relative_to(REPO_ROOT)}: {len(local_block)} -> {len(live_block)} bytes")
    if note is not None:
        print(f"Upstream's latest scene: {note[0]} ({note[1]})")
    print("Review the diff, rebuild/test the image, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
