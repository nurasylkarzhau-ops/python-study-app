# Study App — Python Flashcards & Timed Quiz

A **terminal-based educational app** written in Python for practising flashcards, answering timed quiz questions, and taking notes. This project began as a coursework assignment and was reconstructed from screenshots of the original code.

> **Important:** The coursework specifies **session-only storage**. Registered users, newly added cards, and notes exist **only in RAM** and disappear when the program closes. There is no database or saved user account.

## Features

- **Session registration and login** with username length validation (4–10 characters), uniqueness checks and alphanumeric password validation (5+ characters).
- **Flashcards** with randomly shuffled questions and answer checking.
- **Timed quiz** with a 30-second deadline per question and score tracking.
- **Create flashcards** with new questions and answers for the current session.
- **Notes**: view, add, edit and delete notes in memory.
- **Starter flashcards** covering the history of Kazakhstan.

## Technologies

`Python 3.9+` · Python standard library (`random`, `time`, `select` / `msvcrt`, `hashlib`, `secrets`) · Terminal / CLI

No third-party packages are needed; there is **no `requirements.txt`**.

## Run locally

1. Install Python 3.9 or newer.
2. Download or clone the repository.
3. Open a terminal in the project folder and run:

```bash
python3 study_app.py
```

On Windows, the command may be `py study_app.py`.

The quiz timer is designed for a **real terminal** on Linux, macOS, or Windows (not a notebook, IDE input widget, or redirected input).

## How it works

```text
Welcome to Study App
  1 — Registration
  2 — Login
  3 — Exit

After login:
  1 — Practice flashcards
  2 — Timed quiz (30 seconds per question)
  3 — Add flashcard
  4 — Notes
  0 — Logout
```

The interface shown during execution is **in Russian**. This README is in English for an international GitHub audience.

## Example use

1. Register a username and password.
2. Log in using the same credentials.
3. Select `1` to practise flashcards in random order.
4. Select `2` to take a timed quiz and see the final score.
5. Add your own flashcard or write a note.
6. Exit: all session data will be discarded.

## Test

```bash
python3 -m unittest discover -s tests -v
```

Unit tests cover username/password validation, answer matching and password hashing. Terminal input timing is best verified manually in a real console.

## Coursework requirements and implementation

| Requirement | Implementation |
| --- | --- |
| Console interface only | Yes |
| Registration and login | Yes |
| Unique username | Yes |
| Password: 5+ Latin letters/digits | Yes |
| Add and practise flashcards | Yes |
| Random question order | Yes |
| Timed quiz: 30 seconds / question | Yes, in a real terminal |
| Count correct answers | Yes |
| Notes (optional) | View, add, edit, delete |
| Keep user data in RAM only | Yes |

## From the original coursework to this version

The implementation keeps the original concept, core menu, Kazakhstan-history question bank, and the `random` / `time` approach. The code was **reconstructed and revised from screenshots**, not recovered byte-for-byte from the original source file.

Changes made to ensure the coursework requirements are met:
- Repaired menu flow and indentation.
- Added uniqueness checks for usernames and validation for Latin alphanumeric passwords.
- Made timed answers expire automatically in a terminal rather than checking only after unlimited `input()` time.
- Moved notes from a disk file to RAM, as required by the assignment.
- Added input validation and unit tests.
- Avoided plaintext password storage by storing temporary salted password hashes.

## Scope and limitations

- This is an **educational CLI project**, not a production authentication service.
- Cards, accounts and notes reset on every run **by design**.
- The answer checker ignores case and leading/trailing whitespace, but does not understand synonyms.
- For terminal timing to work correctly, run the script directly in a normal terminal window.

## Author / acknowledgement

Original project concept and coursework implementation by the student. This repository includes a reconstructed, cleaned-up version based on the student's original screenshots and assignment brief.
