#!/usr/bin/env python3
"""Build an Anki deck (.apkg) from Radiology Cafe anatomy image URLs."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import genanki
import requests

from note_type import BACK, CSS, FIELDS, FRONT, MODEL_ID, REVERSE_BACK, REVERSE_FRONT
from parse_urls import load_cards_from_file

DECK_ID = 1609456789013
REQUEST_TIMEOUT = 60


def build_model(include_reverse: bool) -> genanki.Model:
    templates = [
        {"name": "Image → Structure", "qfmt": FRONT, "afmt": BACK},
    ]
    if include_reverse:
        templates.append(
            {"name": "Structure → Image", "qfmt": REVERSE_FRONT, "afmt": REVERSE_BACK},
        )

    return genanki.Model(
        MODEL_ID,
        "Radiology Cafe Anatomy Image",
        fields=FIELDS,
        templates=templates,
        css=CSS,
    )


def download_image(url: str) -> bytes:
    resp = requests.get(url, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.content


def image_field_html(filename: str) -> str:
    return f'<img src="{filename}" alt="Radiology anatomy image">'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--urls",
        type=Path,
        default=Path(__file__).with_name("urls.txt"),
        help="Text file with one URL per line",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).with_name("Radiology_Cafe_Anatomy.apkg"),
        help="Output .apkg path",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Embed remote URLs in Image field (requires internet while reviewing)",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Add a second card type: structure name → image/modality",
    )
    args = parser.parse_args()

    cards_data = load_cards_from_file(args.urls)
    if not cards_data:
        print("No anatomy slider11 URLs found.", file=sys.stderr)
        return 1

    model = build_model(include_reverse=args.reverse)
    deck = genanki.Deck(DECK_ID, "Radiology Cafe Anatomy (slider11)")

    media_files: list[str] = []
    media_dir = args.output.with_suffix(".media")
    if not args.no_download:
        media_dir.mkdir(exist_ok=True)

    for i, card in enumerate(cards_data, 1):
        if args.no_download:
            image_html = f'<img src="{card.source_url}" alt="Radiology anatomy image">'
        else:
            dest = media_dir / card.media_filename
            if not dest.exists():
                print(f"[{i}/{len(cards_data)}] Downloading {card.structure[:50]}…")
                dest.write_bytes(download_image(card.source_url))
            media_files.append(str(dest))
            image_html = image_field_html(card.media_filename)

        note = genanki.Note(
            model=model,
            fields=[
                image_html,
                card.modality_view,
                card.structure,
                card.source_url,
            ],
            guid=hashlib.md5(card.source_url.encode()).hexdigest(),
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    if media_files:
        package.media_files = media_files
    package.write_to_file(str(args.output))
    print(f"Wrote {len(cards_data)} notes → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
