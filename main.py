"""One-sentence absurd invention pitch entry for make.fun.

Writes the single pitch sentence to entry.txt in the output directory
($MAKEFUN_OUTPUT_DIR, default /output). Stdlib only, deterministic.

Gate (from the competition rules): /output/entry.txt must be UTF-8 text
of 1 to 220 characters, not only white space. The entry is written with
no trailing newline so the file holds exactly the judged sentence.
"""

import argparse
import os
import sys

ENTRY = (
    "A houseplant that texts your boss to request a sick day for itself "
    "every time you forget to water it for three days straight."
)

MAX_CHARS = 220


def validate(text: str) -> list[str]:
    """Return a list of gate failures for `text` (empty means valid)."""
    problems = []
    if not 1 <= len(text) <= MAX_CHARS:
        problems.append(f"length {len(text)} chars, must be 1-{MAX_CHARS}")
    if not text.strip():
        problems.append("entry is only white space")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if text.count(".") != 1 or not text.endswith("."):
        problems.append("entry must be exactly one sentence "
                        "(one period, at the end)")
    if "!" in text or "?" in text:
        problems.append("entry must not contain '!' or '?' "
                        "(one sentence only)")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:  # pragma: no cover - defensive
        problems.append(f"not encodable as UTF-8: {exc}")
    return problems


def write_entry(out_dir: str) -> str:
    """Write ENTRY to entry.txt under `out_dir`; return the file path."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    return path


def self_test() -> int:
    """Validate ENTRY, write it to a temp dir, read it back, compare bytes."""
    import tempfile

    problems = validate(ENTRY)
    if problems:
        print("self-test FAIL: " + "; ".join(problems), file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        path = write_entry(tmp)
        with open(path, "rb") as f:
            raw = f.read()
        if raw != ENTRY.encode("utf-8"):
            print("self-test FAIL: read-back bytes differ from ENTRY",
                  file=sys.stderr)
            return 1
        if raw.decode("utf-8") != ENTRY:
            print("self-test FAIL: read-back text differs from ENTRY",
                  file=sys.stderr)
            return 1
    print(f"self-test OK: {len(ENTRY)} chars, single line, single sentence, "
          f"byte-identical round-trip")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None,
                        help="output directory (default: "
                             "$MAKEFUN_OUTPUT_DIR or /output)")
    parser.add_argument("--self-test", action="store_true",
                        help="validate ENTRY and check a byte-identical "
                             "write/read round-trip, then exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    problems = validate(ENTRY)
    if problems:
        print("invalid ENTRY: " + "; ".join(problems), file=sys.stderr)
        return 1

    out_dir = args.out or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(out_dir)
    # Read back and confirm the file holds exactly the entry.
    with open(path, encoding="utf-8") as f:
        if f.read() != ENTRY:
            print(f"read-back mismatch in {path}", file=sys.stderr)
            return 1
    print(f"wrote {path} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
