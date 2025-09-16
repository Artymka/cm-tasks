import psutil
import sys


def get_vfs_name():
    """Возвращает тип файловой системы первого диска."""
    return psutil.disk_partitions()[0].fstype

def simple_cmd_logic(cmd, args):
    """Тестовая проверка аргументов команды и вывод."""
    for arg in args:
        if arg[0] != "-":
            return False, "wrong argument\n"
                                
    return True, f"{cmd} {args}\n"

def exec(cmd, args):
    """Выполняет команду и выводит результат."""
    match cmd:
        case "ls":
           return simple_cmd_logic(cmd, args)
        
        case "cd":
            return simple_cmd_logic(cmd, args)

        case "exit":
            exit(0)

        case _:
            return False, "command not found\n"


def serve(inp_gen, out_func, vfs_path, show_input=False):
    """Запускает выполнение команд, посутпающих из генератора inp_gen, выводя результат в out_func."""
    # vfs_name = get_vfs_name()
    success_symbol = "✓"
    failure_symbol = "✗"
    status_symbol = success_symbol
    success = True

    while True:
        if success: status_symbol = success_symbol
        else: status_symbol = failure_symbol

        out_func(f"[ {vfs_path} ] {status_symbol} > ")
        inp = next(inp_gen)
        if show_input:
            out_func(inp)

        parts = inp.split()
        if not parts:
            continue

        cmd, *args = parts
        success, res = exec(cmd, args)
        out_func(res)

def script_input(script_path):
    """Генерирует строки ввода, читая из из файла скрипта."""
    with open(script_path) as fin:
        for ln in fin.readlines():
            yield ln
    yield "exit"

def std_output(s):
    """Обычный print, только с одинм параметром и без переноса строки."""
    print(s, end="")


def main():
    # print(sys.argv)
    path = sys.argv[0]
    work_dir = sys.argv[1]
    script_path = sys.argv[2]

    serve(script_input(script_path), std_output, work_dir, True)
            

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
"""
