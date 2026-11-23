# Smart File Organizer

A clean, cross-platform, command-line Python project that sorts files by extension, detects exact duplicate content using SHA-256, previews changes, and supports undo via local operation journals.

**Author:** Krushna Kale | [GitHub](https://github.com/krushnakaale) | [LinkedIn](https://www.linkedin.com/in/krushnakaale/) | [Instagram](https://www.instagram.com/krushnakaale/)

## Features

- Organize into Images, Documents, Spreadsheets, Presentations, Videos, Audio, Archives, Code and Others.
- Preview planned changes with `--dry-run`.
- Avoid overwriting existing files: use `_1`, `_2`, etc. for name collisions.
- Optional recursive organization; category folders and state files are excluded.
- Find duplicate file contents (SHA-256, grouped by size first); **never automatically delete duplicates**.
- Undo the most recent operation, refusing to overwrite occupied original paths.
- Record moves in `.sfo_state/operation-*.json`; use `--verbose` for terminal logs.
- Uses only the Python standard library (Python 3.10+).

## Folder structure

```text
Smart-File-Organizer/
├── main.py
├── smart_file_organizer/
│   ├── __init__.py
│   ├── cli.py
│   └── core.py
├── tests/
│   └── test_core.py
├── examples/
│   └── sample-output.txt
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Quick start — Windows (PowerShell)

```powershell
py --version
cd Smart-File-Organizer
py main.py --help
py main.py organize "$env:USERPROFILE\Downloads" --dry-run
py main.py organize "$env:USERPROFILE\Downloads"
py main.py duplicates "$env:USERPROFILE\Downloads" --recursive
py main.py undo "$env:USERPROFILE\Downloads" --dry-run
py main.py undo "$env:USERPROFILE\Downloads"
py -m unittest discover -s tests -v
```

If `py` is unavailable, try `python` instead.

## Quick start — Kali Linux / Ubuntu

```bash
python3 --version
cd Smart-File-Organizer
python3 main.py --help
python3 main.py organize "$HOME/Downloads" --dry-run
python3 main.py organize "$HOME/Downloads"
python3 main.py duplicates "$HOME/Downloads" --recursive
python3 main.py undo "$HOME/Downloads" --dry-run
python3 main.py undo "$HOME/Downloads"
python3 -m unittest discover -s tests -v
```

> **Safety:** Always run `--dry-run` first and test on a copy of a small folder before touching important files. Do not run against system directories or shared folders. Recursive mode collects files from nested folders and moves them into top-level category folders, leaving empty original directories in place.

## CLI commands

```text
python main.py organize PATH [--dry-run] [--recursive]
python main.py duplicates PATH [--recursive]
python main.py undo PATH [--dry-run]
python main.py --verbose organize PATH
```

Global `--verbose` must appear **before** the subcommand.

## Example

Given `demo/report.pdf`, `demo/photo.jpg`, `demo/song.mp3`, `demo/script.py`:

```bash
python main.py organize demo --dry-run
```

```text
PREVIEW (no files changed)
  photo.jpg -> Images/photo.jpg
  report.pdf -> Documents/report.pdf
  script.py -> Code/script.py
  song.mp3 -> Audio/song.mp3
Total: 4 file(s)
```

After a real run:

```text
demo/
├── Audio/song.mp3
├── Code/script.py
├── Documents/report.pdf
├── Images/photo.jpg
└── .sfo_state/operation-....json
```

## Design notes and limitations

- File categorization is based on filename extensions, **not file content**.
- Duplicates are reported, not removed; identical content with different names is still a duplicate.
- Undo restores the latest operation only, in reverse order; journal files are retained for audit. Undo does not delete empty category folders.
- Journal updates are atomic, but file moves and journal updates are not a single filesystem transaction; a sudden crash between them can require manual recovery.
- Files changed or removed by another program after organization can prevent safe undo.
- Symlinked files are skipped. Do not use this tool on folders that untrusted users can modify concurrently.
- Recursive mode intentionally skips directories named after categories at the root.
- No external API, network access, or third-party packages.

## Testing

```bash
python -m unittest discover -s tests -v
```

## License

MIT — see [LICENSE](LICENSE).
