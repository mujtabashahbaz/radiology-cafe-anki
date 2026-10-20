"""Parse Radiology Cafe image URLs into flashcard fields."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse


@dataclass(frozen=True)
class AnatomyCard:
    source_url: str
    media_filename: str
    modality_view: str
    structure: str
    is_anatomy: bool


_SLIDER11 = re.compile(r"/slider11/(\d+)_(.+)\.(jpg|jpeg|png)$", re.I)
_NON_ANATOMY_PARTS = (
    "/slider/cache/",
    "radiology_cafe",
    "Radiology-Cafe-logo",
    "mock-exam",
    "memberpress",
    "frcr2b_rr_bg",
    "physics_atom",
    "lexisnexis",
    "elementor/thumbs",
)


def _parse_slider11_filename(basename: str) -> tuple[str, str] | None:
    m = _SLIDER11.search(basename)
    if not m:
        return None
    rest = unquote(m.group(2))
    if " - " not in rest:
        return None
    modality_view, structure = rest.split(" - ", 1)
    structure = re.sub(r"\s+\d+$", "", structure.strip())
    structure = re.sub(r"\s+na$", "", structure, flags=re.I).strip()
    return modality_view.strip(), structure


def parse_url(url: str) -> AnatomyCard | None:
    url = url.strip()
    if not url or url.startswith("#"):
        return None
    if any(part in url for part in _NON_ANATOMY_PARTS):
        return None

    path = unquote(urlparse(url).path)
    basename = Path(path).name
    parsed = _parse_slider11_filename(path)
    if not parsed:
        return None
    modality_view, structure = parsed
    card_id = _SLIDER11.search(path).group(1)
    safe_name = re.sub(r"[^\w\-]+", "_", basename)[:120]
    media_filename = f"rc_{card_id}_{safe_name}"

    return AnatomyCard(
        source_url=url,
        media_filename=media_filename,
        modality_view=modality_view,
        structure=structure,
        is_anatomy=True,
    )


def load_cards_from_file(path: Path) -> list[AnatomyCard]:
    seen: set[str] = set()
    cards: list[AnatomyCard] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        card = parse_url(line)
        if card and card.source_url not in seen:
            seen.add(card.source_url)
            cards.append(card)
    return cards
