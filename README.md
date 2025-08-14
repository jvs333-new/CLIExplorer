```
 _____  _     _____ _____           _                     
/  __ \| |   |_   _|  ___|         | |                    
| /  \/| |     | | | |____  ___ __ | | ___  _ __ ___ _ __ 
| |    | |     | | |  __\ \/ / '_ \| |/ _ \| '__/ _ \ '__|
| \__/\| |_____| |_| |___>  <| |_) | | (_) | | |  __/ |   
 \____/\_____/\___/\____/_/\_\ .__/|_|\___/|_|  \___|_|   
                             | |                          
                             |_|    v 1.0.1 (beta)           
```

CLIExplorer is a lightweight terminal-based file browser for quick navigation and viewing file details directly from the command line.

## Version
**1.0.1** (beta)  
Released: 2025-08-13  
Type: Patch update (small fixes and improvements)

## Features
- Browse files and folders in a clean table format
- Sort by name, date, extension, or size
- Show file icons and descriptions via JSON configuration
- Open files or navigate folders directly from the CLI

## Requirements
- Python 3.6+

## Usage
1. Download the files
2. Edit `icons_path = Path(r"yourpath\icons.json")` and `icons_path = Path(r"yourpath\icons.json")` with your paths
3. Run:
```bash
python cliexplorer.py
```

- `o <number>` – Open the selected file/folder
- `o .` – Go up one folder level
- `q` – Stop the program

![demo](.README/demo.gif)

## License
MIT License.
