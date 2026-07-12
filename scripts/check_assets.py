#!/usr/bin/env python3
"""Fail CI if any HTML/CSS file references an external host for an *asset*.

Static captures for FFC-EX sites must be fully localized: every stylesheet,
script, image, font, and media file must be served from this repository.
Outbound hyperlinks (<a href="https://...">) to other sites are allowed --
only resource loads are checked.

Usage: python scripts/check_assets.py <site-root>
"""

import os
import re
import sys

ASSET_ATTR_RE = re.compile(
    r"""(?:\b(?:src|srcset|poster|data-src|data-bg|data-background)\s*=\s*["']?\s*(https?://[^"'\s>]+)"""
    r"""|<link\b[^>]*?\bhref\s*=\s*["'](https?://[^"']+)["'])""",
    re.IGNORECASE,
)
CSS_URL_RE = re.compile(r"""url\(\s*["']?(https?://[^"')]+)["']?\s*\)""", re.IGNORECASE)
SRCSET_URL_RE = re.compile(r"(https?://[^\s,\"']+)")

# Content embeds (iframes) intentionally kept: video/map platforms cannot be
# localized. These are documented exceptions, not asset dependencies.
EMBED_ALLOW_RE = re.compile(
    r"^https?://(www\.)?(youtube(-nocookie)?\.com|player\.vimeo\.com|vimeo\.com"
    r"|maps\.google\.com|(www\.)?google\.com/maps)",
    re.IGNORECASE,
)


def check(root: str) -> int:
    failures = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if not name.lower().endswith((".html", ".htm", ".css")):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
            hits = set()
            if name.lower().endswith(".css"):
                hits.update(m.group(1) for m in CSS_URL_RE.finditer(text))
            else:
                for m in ASSET_ATTR_RE.finditer(text):
                    hits.add(m.group(1) or m.group(2))
                # url() inside <style> blocks or style="" attributes
                hits.update(m.group(1) for m in CSS_URL_RE.finditer(text))
            for url in sorted(h for h in hits if h):
                if EMBED_ALLOW_RE.match(url):
                    continue
                failures.append(f"{os.path.relpath(path, root)}: {url}")
    if failures:
        print("External asset references found (must be localized):")
        for line in failures:
            print(f"  {line}")
        return 1
    print("Asset localization check passed: no external asset hosts.")
    return 0


if __name__ == "__main__":
    sys.exit(check(sys.argv[1] if len(sys.argv) > 1 else "public"))
