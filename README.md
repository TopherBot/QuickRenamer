# QuickRenamer 🚀

**One‑liner, zero‑dependency Python tool** to rename files in bulk.

## Features
- **Pattern‑based renaming** – `{{index}}` auto‑increments, `{{name}}` injects the original stem.
- **Safe preview** – run with `--dry-run` to see the changes before they happen.
- **Collision‑aware** – automatically skips or appends a suffix when a target name already exists.
- **Cross‑platform** – works on Windows, macOS, Linux (requires Python 3.7+).

## Installation
Just copy the single file `quickrenamer.py` into a folder on your `$PATH` (or run it via `python -m`). No pip install needed.
```bash
curl -O https://raw.githubusercontent.com/your‑user/QuickRenamer/main/quickrenamer.py
chmod +x quickrenamer.py
mv quickrenamer.py ~/bin/quickrenamer
```

## Usage
```bash
# Rename all .txt files to "doc_001.txt", "doc_002.txt", …
quickrenamer *.txt --pattern "doc_{{index:03}}.txt"

# Replace "IMG_" prefix with "Photo_" and preview only
quickrenamer IMG_*.jpg --pattern "Photo_{{name}}.jpg" --dry-run
```

### Pattern syntax
| Token | Description |
|-------|-------------|
| `{{index}}` | Auto‑incrementing integer starting at 1 |
| `{{index:N}}` | Pad with zeros to *N* digits (e.g. `{{index:04}}` → `0001`) |
| `{{name}}` | Original filename without extension |
| `{{ext}}` | Original extension (including the dot) |

## Contributing
Feel free to fork, add new tokens, or improve the preview UI. See `CONTRIBUTING.md` in the repo for guidelines.

## License
MIT – see `LICENSE` file.
