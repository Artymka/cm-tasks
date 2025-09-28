from typing import Dict, Tuple


def ls_logic(args: list[str], g: Dict) -> Tuple[bool, str]:
    """Выводит папки и файлы, находящиеся в рабочей диретории."""

    res = ""
    for child in g["wd"].children:
        if " " in child.name:
            res += '"' + child.name + '" '
        else:
            res += child.name + ' '
    return True, res[:-1] + '\n'
