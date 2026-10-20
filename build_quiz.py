#!/usr/bin/env python3
"""Build a standalone browser quiz (no Anki) from urls.txt."""

import json
from pathlib import Path

from parse_urls import load_cards_from_file

TEMPLATE = Path(__file__).with_name("quiz_template.html")
OUT = Path(__file__).with_name("quiz.html")
INDEX = Path(__file__).with_name("index.html")


def main() -> None:
    cards = load_cards_from_file(Path(__file__).with_name("urls.txt"))
    payload = [
        {
            "url": c.source_url,
            "modality": c.modality_view,
            "structure": c.structure,
        }
        for c in cards
    ]
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("/*__CARDS_JSON__*/", json.dumps(payload, ensure_ascii=False))
    OUT.write_text(html, encoding="utf-8")
    INDEX.write_text(html, encoding="utf-8")
    print(f"Wrote {len(payload)} cards → {OUT} and {INDEX}")


if __name__ == "__main__":
    main()
