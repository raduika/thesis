#!/usr/bin/env python3
"""Reformat LaTeX prose so that each sentence sits on its own line.

Paragraphs (blocks separated by blank lines) are preserved. Display
environments (``\\begin{...}...\\end{...}``), math regions
(``$...$``, ``$$...$$``, ``\\[...\\]``, ``\\(...\\)``) and section-like
commands are left untouched. Common abbreviations and single-letter
initials do not trigger sentence breaks.

Examples
--------
    python tex/sentence_per_line.py tex/tex/introduction.tex
    python tex/sentence_per_line.py -i tex/tex/*.tex
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ABBREVIATIONS = [
    "e.g.", "i.e.", "cf.", "etc.", "vs.", "et al.", "al.",
    "Prof.", "Ing.", "Dr.", "DrSc.", "Mr.", "Mrs.", "Ms.",
    "Ph.D.", "PhD.", "MSc.", "BSc.", "St.", "No.", "Vol.", "Vols.",
    "pp.", "Eq.", "Eqs.", "Fig.", "Figs.", "Ref.", "Refs.",
    "Sec.", "Secs.", "Sect.", "Sects.", "Ch.", "Chap.", "Tab.", "App.",
    "Inc.", "Ltd.", "Co.", "approx.", "resp.", "min.", "max.", "avg.",
    "std.", "Sci.", "Rep.",
]

RE_BLOCK = re.compile(
    r"\\begin\{([^}]+)\}[\s\S]*?\\end\{\1\}"
    r"|\$\$[\s\S]*?\$\$"
    r"|\\\[[\s\S]*?\\\]"
)
RE_INLINE_MATH_DOLLAR = re.compile(r"(?<!\\)\$(?:\\.|[^\\$])*?\$")
RE_INLINE_MATH_PAREN  = re.compile(r"\\\([\s\S]*?\\\)")

RE_STRUCTURAL_HEAD = re.compile(
    r"^\s*\\(chapter|section|subsection|subsubsection|"
    r"input|include|label|bibliography|bibliographystyle|"
    r"newpage|clearpage|cleardoublepage|tableofcontents|"
    r"listoffigures|listoftables|appendix)\b"
)
RE_FULL_COMMENT_LINE = re.compile(r"^\s*%")

ABBR_DOT = "\x01"  # sentinel for protected period
# Uppercase letters: ASCII Latin, Latin-1 Supplement, Czech extras
# (Č Ď Ě Ň Ř Š Ť Ů Ž), Cyrillic A-Я + Ґ (Russian/Ukrainian).
_UPPER = (
    r"A-Z"
    r"À-ÖØ-Þ"
    r"ČĎĚŇŘŠŤŮŽ"
    r"Ѐ-ЯѠ-Ӿ"
)
SPLIT_RE = re.compile(rf"(?<=[.!?])\s+(?=[\\{_UPPER}\"\(\[`'])")


def mask_inline(text: str):
    """Mask inline math so it survives sentence-splitting unbroken."""
    holders: list[str] = []

    def store(m):
        holders.append(m.group(0))
        return f"\x00{len(holders) - 1}\x00"

    for rx in (RE_INLINE_MATH_DOLLAR, RE_INLINE_MATH_PAREN):
        text = rx.sub(store, text)
    return text, holders


def unmask(text: str, holders):
    return re.sub(r"\x00(\d+)\x00", lambda m: holders[int(m.group(1))], text)


def protect_abbrev(text: str) -> str:
    for ab in ABBREVIATIONS:
        stem = ab[:-1]
        pattern = r"\b" + re.escape(stem) + r"\."
        text = re.sub(pattern, stem + ABBR_DOT, text)
    text = re.sub(rf"\b([{_UPPER}])\.(?=\s+[{_UPPER}])", r"\1" + ABBR_DOT, text)
    return text


def restore_abbrev(text: str) -> str:
    return text.replace(ABBR_DOT, ".")


def split_sentences(prose: str) -> list[str]:
    prose = re.sub(r"\s+", " ", prose).strip()
    if not prose:
        return []
    prose = protect_abbrev(prose)
    parts = SPLIT_RE.split(prose)
    return [restore_abbrev(p).strip() for p in parts if p.strip()]


def peel_structural(lines: list[str]):
    head: list[str] = []
    while lines and (RE_STRUCTURAL_HEAD.match(lines[0])
                     or RE_FULL_COMMENT_LINE.match(lines[0])):
        head.append(lines[0].rstrip())
        lines = lines[1:]
    return head, lines


def reformat_block(block: str) -> str:
    if not block.strip():
        return ""
    lines = block.split("\n")
    head, rest_lines = peel_structural(lines)
    rest = "\n".join(rest_lines).strip()
    if not rest:
        return "\n".join(head)

    out_lines: list[str] = list(head)
    cursor = 0
    for m in RE_BLOCK.finditer(rest):
        if m.start() > cursor:
            out_lines.extend(_prose_to_sentences(rest[cursor:m.start()]))
        out_lines.append(m.group(0).strip("\n"))
        cursor = m.end()
    if cursor < len(rest):
        out_lines.extend(_prose_to_sentences(rest[cursor:]))
    return "\n".join(s for s in out_lines if s)


def _prose_to_sentences(prose: str) -> list[str]:
    masked, holders = mask_inline(prose)
    return [unmask(s, holders) for s in split_sentences(masked)]


def reformat(text: str) -> str:
    blocks = re.split(r"\n[ \t]*\n", text)
    out = [reformat_block(b) for b in blocks]
    out = [b for b in out if b]
    suffix = "\n" if text.endswith("\n") else ""
    return "\n\n".join(out) + suffix


def main():
    ap = argparse.ArgumentParser(
        description="Put each sentence on its own line in LaTeX files.")
    ap.add_argument("files", nargs="+", type=Path,
                    help=".tex files to reformat")
    ap.add_argument("-i", "--in-place", action="store_true",
                    help="rewrite files in place; otherwise print to stdout")
    args = ap.parse_args()

    for path in args.files:
        raw = path.read_bytes()
        for enc in ("utf-8", "latin-1"):
            try:
                original = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            print(f"skipped (cannot decode): {path}", file=sys.stderr)
            continue
        rewritten = reformat(original)
        if args.in_place:
            path.write_bytes(rewritten.encode(enc))
            print(f"reformatted {path}", file=sys.stderr)
        else:
            sys.stdout.write(rewritten)


if __name__ == "__main__":
    main()
