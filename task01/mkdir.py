from typing import Dict, Tuple

from vfs import Node


def mkdir_logic(args: list[str], g: Dict) -> Tuple[bool, str]:
    """Создаёт новую директорию."""

    path = args[0]
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
    if not path_queue[-1]:
        path_queue.pop()
    new_dir = path_queue.pop()

    for part in path_queue:
        try:
            if part == ".":
                continue
            elif part == "..":
                curr = curr.parent
                assert curr
            else:
                curr = curr.get_child(part)
                assert curr
        except Exception as e:
            return False, "error: wrong path\n"
    
    if curr.type == "file":
        return False, "error: can`t create new directory there\n"
    if new_dir in curr.children:
        return False, "error: directory with this name already exists\n"
    
    new_dir_node = Node(
        name = new_dir,
        type = "dir",
        parent = curr,
    )
    curr.add_child(new_dir_node)

    return True, ""
