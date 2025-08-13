from pathlib import Path
from datetime import datetime
import json
import os
import platform
import subprocess

LOGO = """
 _____  _     _____ _____           _                     
/  __ \| |   |_   _|  ___|         | |                    
| /  \/| |     | | | |____  ___ __ | | ___  _ __ ___ _ __ 
| |    | |     | | |  __\ \/ / '_ \| |/ _ \| '__/ _ \ '__|
| \__/\| |_____| |_| |___>  <| |_) | | (_) | | |  __/ |   
 \____/\_____/\___/\____/_/\_\ .__/|_|\___/|_|  \___|_|   
                             | |                          
                             |_|    v 1.0.1 (beta)           
"""

### Load the icons and descriptions ###

# Path to the JSON file containing file type → icon mappings
icons_path = Path(r"yourpath\icons.json")  # Replace with your path

# Path to the JSON file containing file type → description mappings
discriptions_path = Path(r"yourpath\discriptions.json")  # Replace with your path

# Load icons JSON into a dictionary
with icons_path.open("r", encoding="utf-8") as f:
    icons = json.load(f)

# Load descriptions JSON into a dictionary
with discriptions_path.open("r", encoding="utf-8") as f:
    discriptions = json.load(f)


def parse_sort(sort="snh"):
    """
    Parse the sorting string into parameters.

    Args:
        sort (str, optional): Sorting string with three characters:
                              1. First char: 's' means folders first
                              2. Second char: 'n' (name), 't' (time), 'e' (extension), 's' (size)
                              3. Third char: 'l' for descending, 'h' for ascending
                              Default is "snh".

    Returns:
        tuple:
            sp (bool): True if folders should be listed first.
            so (int): Sorting mode (1=name, 2=time, 3=extension, 4=size).
            hl (bool): True for descending order.
    """
    sp = sort.startswith("s")  # True if 's' means folders first
    so = {"n": 1, "t": 2, "e": 3, "s": 4}.get(sort[1], 1)  # Sorting mode
    hl = sort[2] == "l"  # Descending if last char is 'l'
    return sp, so, hl


def sort_key(f: Path):
    """
    Generate a sorting key for a file or folder.

    Args:
        f (Path): File or folder path.

    Returns:
        tuple: (group, key)
            group (int): Used for folder-first grouping.
            key (Any): Value to sort by depending on the selected sorting mode.
    """
    sp, so, hl = parse_sort()

    # Group ensures folders are listed first if enabled
    group = 1 if (sp and not f.is_file()) else 0

    # Choose sort key based on mode
    if so == 1:
        key = f.stem.lower()  # Sort by name
    elif so == 2:
        key = f.stat().st_mtime  # Sort by modification time
    elif so == 3:
        key = f.suffix.lower().lstrip('.')  # Sort by file extension
    elif so == 4:
        key = f.stat().st_size  # Sort by file size
    else:
        key = f.stem.lower()
    return (group, key)


def sizeof_fmt(num, suffix="B"):
    """
    Convert a file size in bytes to a human-readable string.

    Args:
        num (int or float): File size in bytes.
        suffix (str, optional): Suffix for the size (default "B").

    Returns:
        str: Human-readable size (e.g., "1.23 MB").
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:.2f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.2f} Y{suffix}"

def open_file(path: Path):
    """Open a file or folder with the default application."""
    system = platform.system()
    if system == "Windows":
        os.startfile(str(path))
    elif system == "Darwin":  # macOS
        subprocess.run(["open", str(path)])
    else:  # Linux / Unix
        subprocess.run(["xdg-open", str(path)])

def render(folder: Path):
    """
    Render the file explorer table for a given folder.

    Args:
        folder (Path): Path to the folder to display.

    Side effects:
        Clears the console and prints a formatted table of files and folders.
    """
    files = sorted(folder.iterdir(), key=sort_key, reverse=parse_sort()[2])

    # Determine column widths dynamically
    type_lengths = [len(f.suffix if f.is_file() else 'fld') for f in files]
    type_width = max(max(type_lengths), 4)

    dis_lengths = [
        len(discriptions.get(f.suffix, f"{f.suffix.lstrip('.').upper()} file") if f.is_file() else "File folder")
        for f in files
    ]
    dis_width = max(max(dis_lengths), 11)

    no_width = max(len(str(len(files))), 2)  # Number column width
    name_width = 20  # Max file name display length
    table_width = 46 + no_width + name_width + type_width + dis_width

    # Shorten displayed path if it’s too long
    path = str(folder.absolute())
    if len(path) > table_width - 2:
        path = "..." + path[-(table_width - 5):]

    # Clear terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print table header
    print(f"|{'‾' * table_width}|")
    print(f"| {path:^{table_width - 2}} |")
    print(f"|{' ' * table_width}|")
    print(f"|{'‾' * (no_width+2)}|{'‾' * (name_width+5)}|{'‾' * 18}|{'‾' * 12}|{'‾' * (type_width+2)}|{'‾' * (dis_width+2)}|")
    print(f"|{'No':^{no_width+2}}|{'Name':^{name_width + 5}}|    Last edit     |    Size    |{'Type':^{type_width+2}}| {'Description':^{dis_width}} |")
    print(f"|{'-' * (no_width+2)}|{'-' * (name_width+5)}|{'-' * 18}|{'-' * 12}|{'-' * (type_width+2)}|{'-' * (dis_width+2)}|")

    # Print each file or folder row
    for i, f in enumerate(files, 1):
        icon = icons.get(f.suffix, "📃") if f.is_file() else "📁"
        name = f.name
        if len(name) > name_width:
            name = name[:name_width - 3] + "..."  # Truncate long names
        mtime_str = datetime.fromtimestamp(f.stat().st_mtime).strftime('%d-%m-%Y %H:%M')
        size_str = sizeof_fmt(f.stat().st_size) if f.is_file() else ''
        type_str = f.suffix if f.is_file() else 'fld'
        dis_str = discriptions.get(f.suffix, f"{f.suffix.lstrip('.').upper()} file") if f.is_file() else "File folder"
        print(f"| {i:0>{no_width}} | {icon} {name:<{name_width}} | {mtime_str} | {size_str:<10} | {type_str:<{type_width}} | {dis_str:<{dis_width}} |")

    # Print table footer
    print(f"|{'‾' * table_width}|")
    print(f"|{'CLIExplorer v1.0.1 visit https://github.com/jvs333-new/CLIExplorer for more info.':^{table_width}}|")
    print(f"|{'_' * table_width}|")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to:")
    print(LOGO)
    input("Press Enter to continue.")

    # Starting directory
    folder = Path(r".")

    # Main loop for rendering and user input
    while True:
        render(folder)
        cmd = input(">>> ")
        if cmd == "q":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Thanks for using:")
            print(LOGO)
            raise SystemExit
        # If the command starts with 'o', attempt to open file or change folder
        if cmd.startswith("o "):
            cmd = cmd.lstrip("o ") # Remove 'o' from the command
            if cmd == ".":
                folder = folder.parent  # Go up one directory
            else:
                try:
                    choice = sorted(folder.iterdir(), key=sort_key, reverse=parse_sort()[2])[int(cmd) - 1]
                except ValueError:
                    choice = Path(cmd)  # Allow direct path input
                if choice.is_file():
                    open_file(choice)  # Open file
                else:
                    folder = choice  # Change directory
