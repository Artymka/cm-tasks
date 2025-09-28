from typing import Dict, Tuple


def cd_logic(args: list[str], g: Dict) -> Tuple[bool, str]:
    """Меняет текущую директорию."""

    """
    Команда cd будет парсить путь
    / - корневая директория
    /... - абсолютный путь (искать из объекта vfs)
    ... - относительный путь (искать из объекта текущей директории)

    разделить строку пути по слешам
    полученные части кинуть в очередь
    брать части из очереди и последовательно пытаться
    менять ссылку на текущий объект
    *ссылку на родительский словарь тоже иметь
    **предварительно сохранить предыдущий объект пути
    в отдельную переменную, чтобы при ошибки считывания пути
    вернуться к нему

    . - текущая директория
    .. - родительская директория
    """

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
    
    if curr.type == "file":
        return False, "error: the path must point to a directory, not a file\n"
    
    g["wd"] = curr
    g["path"] = "/" + "/".join(final_path_parts)

    return True, ""
