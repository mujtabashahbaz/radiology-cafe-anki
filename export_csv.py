#!/usr/bin/env python3
"""Export parsed cards to Anki-importable CSV (media filenames only)."""

from pathlib import Path

from parse_urls import load_cards_from_file


def main() -> None:
    urls = Path(__file__).with_name("urls.txt")
    out = Path(__file__).with_name("radiology_cafe_anatomy.csv")
    cards = load_cards_from_file(urls)

    lines = [
        "Image,ModalityView,Structure,SourceURL",
    ]
    for c in cards:
        img = f'<img src="{c.media_filename}">'
        row = [
            img.replace('"', '""'),
            c.modality_view.replace('"', '""'),
            c.structure.replace('"', '""'),
            c.source_url.replace('"', '""'),
        ]
        lines.append(",".join(f'"{col}"' for col in row))

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(cards)} rows → {out}")


if __name__ == "__main__":
    main()
