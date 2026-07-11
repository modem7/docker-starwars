#!/usr/bin/env python3
"""Shared helpers for syncing src/index.html's embedded film (animation
frame) data with the upstream site this project mirrors:
https://www.asciimation.co.nz/Blinkenlights/

Used by update_film_data.py (pulls new content) and
check_film_freshness.py (reports whether we're behind upstream).
"""
import gzip
import hashlib
import re
import urllib.request

LIVE_URL = "https://www.asciimation.co.nz/Blinkenlights/"

# The engine code in index.html assigns the whole animation to a single
# JS string literal, then immediately checks `if(film)` to kick off
# autoplay - that's a stable, distinctive boundary in both our copy and
# upstream's, so we use it to isolate just the content, not any of the
# surrounding page (ads, analytics, nav links) that upstream also ships.
FILM_START = b"var film = '"
FILM_END = b"if(film)"


def fetch_live_page(url: str = LIVE_URL, timeout: int = 30) -> bytes:
    """Fetch upstream, decompressing gzip if the server sent it.

    Fetching without requesting gzip has been observed to get served a
    stripped ~7KB fallback page (with no film data at all) instead of
    the real ~2MB page - so Accept-Encoding is mandatory here, not
    an optimization.
    """
    req = urllib.request.Request(
        url,
        headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "docker-starwars-content-sync (+https://github.com/modem7/docker-starwars)",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (fixed https URL above)
        raw = resp.read()
        if resp.headers.get("Content-Encoding", "").lower() == "gzip":
            raw = gzip.decompress(raw)
    return raw


def normalize_line_endings(data: bytes) -> bytes:
    """Collapse CRLF to LF.

    Upstream's HTML has stray CRLF sequences mixed in with LF. This
    repo's .gitattributes normalizes all text files to LF, so anything
    checked in - and anything cloned back out - never keeps a raw CR.
    Comparing/writing pre-normalized bytes here means the freshness
    check compares like with like (instead of permanently reporting
    "stale" against a byte git will strip anyway), and a fresh sync
    doesn't quietly get rewritten by git out from under it.
    """
    return data.replace(b"\r\n", b"\n")


def extract_film_block(data: bytes) -> bytes:
    """Return the `var film = '...';` slice, engine code excluded."""
    start = data.find(FILM_START)
    if start == -1:
        raise ValueError("could not find \"var film = '\" marker")
    end = data.find(FILM_END, start)
    if end == -1:
        raise ValueError("could not find \"if(film)\" end marker after film data")
    return normalize_line_endings(data[start:end])


def film_hash(block: bytes) -> str:
    return hashlib.sha256(block).hexdigest()


_LAST_SCENE_RE = re.compile(
    rb'Last scene added:\s*(.*?)</font>\s*<br/?>\s*'
    rb'<font size=\+0 face="Arial">\s*(.*?)\s*</font>',
    re.DOTALL,
)


def extract_last_scene_note(data: bytes) -> tuple[str, str] | None:
    """Return (scene description, date) from upstream's footer, if present."""
    m = _LAST_SCENE_RE.search(data)
    if not m:
        return None
    scene = m.group(1).decode("utf-8", "replace").strip()
    date = m.group(2).decode("utf-8", "replace").strip()
    return scene, date
