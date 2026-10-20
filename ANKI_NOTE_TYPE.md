# Radiology Cafe Anatomy Image — Anki note type

Manual setup in **Tools → Manage Note Types → Add → Add: Cloze** (then rename) or duplicate **Basic** and edit.

## Fields (in order)

| Field | Purpose |
|-------|---------|
| `Image` | HTML `<img>` tag or plain media filename |
| `ModalityView` | e.g. `mri knee sagittal` |
| `Structure` | Answer, e.g. `posterior horn of lateral meniscus` |
| `SourceURL` | Original Radiology Cafe URL (optional on front) |

## Card 1 — Image → Structure

**Front template** — copy from `templates/front.html`

**Back template** — copy from `templates/back.html`

## Card 2 (optional) — Structure → Image

**Front** — copy from `templates/reverse_front.html`

**Back** — copy from `templates/reverse_back.html`

## Styling

Paste `templates/style.css` into the note type **Styling** box.

## CSV import

Use `radiology_cafe_anatomy.csv` with this note type. Map columns to fields; put full `<img src="filename.jpg">` in the `Image` column after copying media into Anki's collection.media folder.

## Generate .apkg

```bash
pip install -r requirements.txt
python generate_deck.py
```

Images are downloaded into `Radiology_Cafe_Anatomy.media/` and embedded for offline review.

**Copyright:** Images are © Radiology Cafe. Use for personal study only; do not redistribute the deck publicly without permission.
