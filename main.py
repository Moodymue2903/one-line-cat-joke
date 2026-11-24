#!/usr/bin/env python3
"""One-line cat joke entry for the make.fun competition
"The One-Line Cat Joke That Lands".

Running this program writes the joke, exactly one line, to
/output/entry.txt. Nothing else is written to the entry file.
"""

from pathlib import Path
import argparse

JOKE = "My cat knocked my coffee off the table, looked me dead in the eye, and I apologised to her."

OUTPUT_PATH = Path("/output/entry.txt")

MAX_CHARS = 200


def validate(text):
    """Check the joke against the competition gate.

    The gate needs UTF-8 text of 1 to 200 characters, not only
    whitespace, on a single line.
    """
    if not isinstance(text, str):
        raise ValueError("joke must be text")
    if not text.strip():
        raise ValueError("joke must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError("joke is over 200 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")
    text.encode("utf-8")
    return text


def write_entry(path=OUTPUT_PATH):
    """Write the validated joke to the entry file.

    Creates the output folder when it is missing, then writes the
    joke with no trailing newline and no extra text.
    """
    text = validate(JOKE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def verify(path=OUTPUT_PATH):
    """Read the entry file back and confirm it holds the joke exactly."""
    written = path.read_text(encoding="utf-8")
    if written != JOKE:
        raise ValueError("entry file does not match the joke")
    return len(written)


def main():
    """Write the joke to the entry file.

    The output path defaults to /output/entry.txt; --output lets a
    local test run write somewhere else without touching the entry.
    """
    parser = argparse.ArgumentParser(description="Write the one-line cat joke entry.")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH,
                        help="where to write the entry (default: /output/entry.txt)")
    args = parser.parse_args()
    path = write_entry(args.output)
    chars = verify(path)
    print(f"Wrote {chars} characters to {path}")


if __name__ == "__main__":
    main()
