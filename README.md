# file-organizer

A desktop file sorter with a tkinter GUI. Point it at a folder and it sorts files into category subfolders (Images, Videos, Music, Documents, Archives, Code, Slides, Spreadsheets, Executables, Others) based on extension.

## Features

- Move or copy mode
- Preview mode — see exactly what would happen before touching any files
- Optional subfolder scanning (one level deep)
- Live progress bar + color-coded log of every action
- Automatic conflict handling — if a destination file already exists, the incoming file is renamed with a `_copy` suffix instead of overwriting
- Runs the sort on a background thread so the UI never freezes

## Setup

```bash
python file_sorting.py
```

No external dependencies — uses only the Python standard library (`tkinter`, `os`, `shutil`, `threading`).

## Usage

1. Browse to or paste a target folder path
2. Choose **move** or **copy**
3. Optionally enable **skip subfolders** or **preview only**
4. Hit **run** — watch the log and progress bar

Preview mode is a good first pass on any folder you haven't sorted before — it shows you the categorization without moving anything.

## Category mapping

Extensions are mapped to categories in a single dict at the top of the script — easy to extend with new file types or categories.

## License

PolyForm Noncommercial 1.0.0 — see [LICENSE](LICENSE). Free for personal, educational, and noncommercial use.
