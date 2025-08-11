# CLIExplorer

CLIExplorer is a lightweight terminal-based file browser for quick navigation and viewing file details directly from the command line.

## Version
**1.0.0** – Initial release with table-based file listing, sorting, and basic navigation.

More coming soon.

## Features
- Browse files and folders in a clean table format
- Sort by name, date, extension, or size
- Show file icons and descriptions via JSON configuration
- Open files or navigate folders directly from the CLI

## Requirements
- Python 3.6+

## Usage
Run:
```bash
python cliexplorer.py
```

- `o <number>` – Open the selected file/folder
- `o .` – Go up one folder level

## OS Compatibility
- **Fully supported**: Windows  
  Uses `os.startfile()` to open files and `cls` to clear the console.
- **Partial support**: Linux & macOS  
  Replace:
  - `os.startfile()` → `subprocess.run(["xdg-open", path])` (Linux) or `subprocess.run(["open", path])` (macOS)
  - `cls` → `clear` (already handled in code via `os.name`)


## License
MIT License.
