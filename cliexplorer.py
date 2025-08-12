from pathlib import Path
from datetime import datetime
import json
import os

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:.2f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.2f} Y{suffix}"

icons_path = Path(r"path\icons.json") #replace path with your path to icons.json
types_path = Path(r"path\types.json")  #replace path with your path to types.json

with icons_path.open("r", encoding="utf-8") as f:
    icons = json.load(f)

with types_path.open("r", encoding="utf-8") as f:
    types = json.load(f)

sort = "sth"

sp = sort.startswith("s")
so = {"n": 1, "t": 2, "e": 3, "s": 4}.get(sort[1], 1)
hl = sort[2] == "l"

def sort_key(f: Path):
    group = 1 if (sp and not f.is_file()) else 0
    if so == 1:
        key = f.stem.lower()
    elif so == 2:
        key = f.stat().st_mtime
    elif so == 3:
        key = f.suffix.lower().lstrip('.')
    elif so == 4:
        key = f.stat().st_size
    else:
        key = f.stem.lower()
    return (group, key)

def render(folder: Path):
    files = sorted(folder.iterdir(), key=sort_key, reverse=hl)
    type_lengths = []
    for f in files:
        if f.is_file():
            ext = f.suffix
        else:
            ext = 'fld'
        type_lengths.append(len(ext))
    type_width = max(max(type_lengths), 4)

    dis_lengths = []
    for f in files:
        dis = types.get(f.suffix, f"{f.suffix.lstrip('.').upper()} file") if f.is_file() else "File folder"
        dis_lengths.append(len(dis))
    dis_width = max(max(dis_lengths), 11)

    width = max(len(str(len(files))), 2)
    name_width = 20
    table_width = 46 + width + name_width + type_width + dis_width
    path = str(folder.absolute())
    max_len = table_width - 2
    if len(path) > max_len:
        path = "..." + path[-(max_len - 3):]

    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"|{'‾' * table_width}|")
    print(f"| {path:^{table_width - 2}} |")
    print(f"|{' ' * table_width}|")
    print(f"|{'‾' * (width+2)}|{'‾' * (name_width+5)}|{'‾' * 18}|{'‾' * 12}|{'‾' * (type_width+2)}|{'‾' * (dis_width+2)}|")
    print(f"|{'No':^{width+2}}|{'Name':^{name_width + 5}}|    Last edit     |    Size    |{'Type':^{type_width+2}}| {'Discription':^{dis_width}} |")
    print(f"|{'-' * (width+2)}|{'-' * (name_width+5)}|{'-' * 18}|{'-' * 12}|{'-' * (type_width+2)}|{'-' * (dis_width+2)}|")

    for i, f in enumerate(files, 1):
        icon = icons.get(f.suffix, "📃") if f.is_file() else "📁"
        name = f.name
        if len(name) > name_width:
            name = name[:name_width - 3] + "..."
        mtime_str = datetime.fromtimestamp(f.stat().st_mtime).strftime('%d-%m-%Y %H:%M')
        size_str = sizeof_fmt(f.stat().st_size) if f.is_file() else ''
        type_str = f.suffix if f.is_file() else 'fld'
        dis_str = types.get(f.suffix, f"{f.suffix.lstrip('.').upper()} file") if f.is_file() else "File folder"
        print(f"| {i:0>{width}} | {icon} {name:<{name_width}} | {mtime_str} | {size_str:<10} | {type_str:<{type_width}} | {dis_str:<{dis_width}} |")

    print(f"|{'_' * (width+2)}|{'_' * (name_width+5)}|{'_' * 18}|{'_' * 12}|{'_' * (type_width+2)}|{'_' * (dis_width+2)}|")

if __name__ == "__main__":
    folder = Path(r".")
    while True:
        render(folder)
        cmd = input(">>> ")
        if cmd.startswith("o"):
            cmd = " ".join(cmd.split(" ")[1:])
            print(cmd)
            if cmd == " .":
                folder = folder.parent
            else:
                try:choice = sorted(folder.iterdir(), key=sort_key, reverse=hl)[int(cmd) - 1]
                except ValueError:choice = Path(cmd)
                if choice.is_file():
                    os.startfile(str(choice))
                else:
                    folder = choice
