import psutil
import sys
import platform
import os
from typing import Tuple, Generator, Callable, Dict

from vfs import Node
from cd import cd_logic
from ls import ls_logic
from whoami import whoami_logic


# """
# Глобальный словарь с состоянием выполнения команд.
# ['vfs'] - корень VFS
# ['wd'] - node текущей директории
# ['path'] - строка пути текущей директории
# """
# g = {}


def get_vfs_name() -> str:
    """Возвращает тип файловой системы первого диска."""
    return psutil.disk_partitions()[0].fstype

def simple_cmd_logic(cmd: str, args: list[str]) -> Tuple[bool, str]:
    """Тестовая проверка аргументов команды и вывод."""
    for arg in args:
        if arg[0] != "-":
            return False, "wrong argument\n"
                                
    return True, f"{cmd} {args}\n"


def exec(cmd: str, args: list[str], g: Dict) -> Tuple[bool, str]:
    """Выполняет команду и выводит результат."""
    match cmd:
        case "ls":
           return ls_logic(args, g)
        
        case "cd":
            return cd_logic(args, g)
        
        case "vfs-info":
            return True, g['vfs'].get_vfs_info()
        
        case "vfs-structure":
            return True, g['vfs'].get_vfs_structure()
        
        case "whoami":
            return whoami_logic(args, g)
        
        case "clear":
            return True, "clear"

        case "exit":
            exit(0)

        case _:
            return False, "command not found\n"


def command_str_split(inp: str) -> list[str]:
    """Возвращает сипсок с командой и аргументами, учитывает двойные кавычки."""
    res = []
    quote = False
    curr = ""
    for i in range(len(inp)):
        ch = inp[i]
        match ch:
            case '"':
                quote = not quote
            case ' ':
                if quote:
                    curr += ch
                elif curr:
                    res.append(curr)
                    curr = ""
            case '\n':
                pass
            case _:
                curr += ch
    if curr: res.append(curr)
    # print(">>>", res)
    return res


def serve(inp_gen: Generator[str],
          out_func: Callable[[str], None],
          vfs_path: str,
          show_input: bool = False) -> None:
    """Запускает выполнение команд, посутпающих из генератора inp_gen, выводя результат через out_func."""
    
    """
    ['vfs'] - корень VFS
    ['wd'] - node текущей директории
    ['path'] - строка пути текущей директории
    """
    g = {}

    # загрузка vfs
    try:
        g['vfs'] = Node.read_vfs_form_xml(vfs_path)
    except Exception as e:
        out_func(f"Error while reading xml: {e}\n")
        exit(0)
    
    # установка значений для работы с файловой системой
    g["wd"] = g["vfs"]
    g["path"] = "/"

    # символы для отображеня успешности выполненя команды 
    success_symbol = "✓"
    failure_symbol = "✗"
    status_symbol = success_symbol
    success = True

    # цикл ввода-вывода
    while True:
        if success: status_symbol = success_symbol
        else: status_symbol = failure_symbol

        out_func(f"[ {g["path"]} ] {status_symbol} > ")
        inp = next(inp_gen)
        if show_input:
            out_func(inp)

        parts = command_str_split(inp)
        if not parts:
            continue

        cmd, *args = parts
        success, res = exec(cmd, args, g)
        out_func(res)

def script_input(script_path: str) -> Generator[str]:
    """Генерирует строки ввода, читая из из файла скрипта."""
    with open(script_path) as fin:
        for ln in fin.readlines():
            yield ln
    yield "exit"

def std_output(s: str) -> None:
    """Обычный print, только с одинм параметром и без переноса строки."""
    # очистка консоли
    if s == "clear":
        system = platform.system().lower()
        if system == 'windows':
            os.system('cls')
        else:  # linux, darwin (mac), etc.
            os.system('clear')
        return
    
    print(s, end="")
 

def main():
    vfs_path = sys.argv[1]
    script_path = sys.argv[2]

    serve(script_input(script_path), std_output, vfs_path, True)
            

if __name__ == "__main__":
    main()
                
    



"""
Формулировка задачи:
исполнение определённой команды
возврат результата команды куда-то
изменение вида приглашения к вводу

вывод в консоль результата выполнения команды
получение ввода из файла или консоли
вывод приглашения к вводу

приглашение к вводу:
название vfs
успешность выполнения команды

блоки программы:
функция для выполнения команды:
 ввод - команда с аргументами,
 вывод - успешность выполнения, строка сообщения
функция взаимодействия с пользователем через данный интерфейс:
 ввод - функция для ввода, функция для вывода,
 вывод - ничего, вызывает выполнение команды, выводит результат, меняет приглашение
точка входа в программу:
 сначала работает с командами из файла
 потом включает интерактивный режим (не особо нужно)





Для реализации ls и cd будет использоваться глобальный объект
в нем будет загруженная vfs и текущая директория
текущая директория будет отражена строкой пути и объектом директории

команда ls будет получать информацию из объекта текущей директории

команда cd будет парсить путь
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

!!!
нужно правильно обрабатывать переход в родительскую директорию
либо иметь массив с ссылками на все словари до текущего
либо разрабатывать какие-нибудь функции для ориентации в vfs
возможно ввобще стоит организовать всё через класс, а не через словарь


"""
