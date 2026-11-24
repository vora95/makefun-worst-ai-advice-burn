#!/usr/bin/env python3
"""Worst AI Advice: delete your backups before updating.

Writes one line of deliberately terrible AI advice to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output/entry.txt).
Stdlib only, fully deterministic.
"""

import hashlib
import os
from pathlib import Path

ENTRY = "Delete your backups before updating \u2014 a clean install runs faster, and you can always rebuild the database from memory."

EXPECTED_SHA256 = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY, encoding="utf-8")
    data = target.read_bytes()
    assert data == ENTRY.encode("utf-8"), "entry.txt differs from ENTRY"
    assert len(ENTRY) <= 140, f"entry too long: {len(ENTRY)} chars"
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256
    # Validation revision: the gate needs exactly one line, UTF-8, 1-140
    # chars, not whitespace-only, and no trailing newline.
    text = data.decode("utf-8")
    assert "\n" not in text, "entry must be a single line"
    assert text.strip() != "", "entry must not be whitespace-only"
    assert 1 <= len(text) <= 140, f"gate: {len(text)} chars out of range"
    print(f"wrote {len(data)} bytes, {len(ENTRY)} chars, sha256 {EXPECTED_SHA256}")


if __name__ == "__main__":
    main()
