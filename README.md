# Radiology Cafe anatomy flashcards

## No Anki? Use the browser quiz

```bash
python3 build_quiz.py
open quiz.html
```

Double-click **`quiz.html`** in Finder, or open it in Chrome/Safari/Firefox.

- **Space** — show answer  
- **N** / **P** — next / previous  
- **K** — got it (marks known and advances)  
- Shuffle and restart from the header  

You need internet so images can load from radiologycafe.com.

## Optional: Anki

If you install [Anki](https://apps.ankiweb.net/) later:

```bash
pip install -r requirements.txt
python generate_deck.py
```

Import `Radiology_Cafe_Anatomy.apkg`. See `ANKI_NOTE_TYPE.md` for manual note-type setup.
