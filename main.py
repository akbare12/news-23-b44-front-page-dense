#!/usr/bin/env python3
"""news-23 b44 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error:", msg, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if out_dir_abs == os.path.abspath(HERE) or out_dir_abs.startswith(os.path.abspath(HERE) + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must be outside the repository")
    if not os.path.isfile(SRC):
        fail("entry.png not found next to main.py")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        fail("entry.png exceeds 1 MiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG file")
    # IHDR: width/height at bytes 16..24, bit depth + colour type at 24..26
    width, height = struct.unpack(">II", data[16:24])
    bit_depth, colour_type = struct.unpack(">BB", data[24:26])
    if (width, height) != (1024, 1024):
        fail("entry.png is not 1024x1024")
    if bit_depth != 8 or colour_type not in (2, 6):
        fail("unexpected PNG bit depth / colour type")
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        fail("PNG IEND trailer missing or malformed")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        fail("output differs from source")
    print("source", SRC, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest())
    print("wrote", dst, len(written), "bytes",
          "sha256", hashlib.sha256(written).hexdigest())


if __name__ == "__main__":
    main()
