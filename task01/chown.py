from typing import Dict, Tuple


def chown_logic(args: list[str], g: Dict) -> Tuple[bool, str]:
    """Меняет владельца файла/папки."""

    if len(args) != 2:
        return False, "error: expected 2 arguments: <owner> <path>"
    
    owner = args[0]
    path = args[1]
    curr = None
    relative = False

    if path == "/":
        g["wd"] = g["vfs"]
        g["path"] = path
        return True, ""
    # абсолютный путь или относительный
    elif path[0] == "/":
        curr = g["vfs"]
        path = path[1:]
    else:
        curr = g["wd"]
        relative = True
    
    # разбиение и обработка пути
    path_queue = path.split("/")
    final_path_parts = [s for s in g["path"][1:].split("/") if s]
    if not path_queue[-1]:
        path_queue.pop()
    for part in path_queue:
        try:
            if part == ".":
                continue
            elif part == "..":
                curr = curr.parent
                assert curr
                final_path_parts.pop()
            else:
                curr = curr.get_child(part)
                assert curr
                final_path_parts.append(part)
        except Exception as e:
            return False, "error: wrong path\n"
    
    curr.owner = owner

    return True, ""
