import argparse

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Инстурумент визуализации графа')
    
    parser.add_argument('--name', '-n', type=str, required=True, help='Имя анализируемого пакета')
    parser.add_argument('--repo', '-r', type=str, required=True, help='URL-адрес репозитория или путь к файлу тестового репозитория')
    parser.add_argument('--version', '-v', type=str, required=True, help='Версия пакета')
    parser.add_argument('--mode', '-m', type=str, default="default", help='Режим работы с тестовым репозиторием')
    parser.add_argument('--graph', '-g', type=str, default="./output.png", help='Имя сгенерированного файла с изображением графа')
    parser.add_argument('--ascii', '-a', action='store_true', help='Режим вывода зависимостей в формате ASCII-дерева')

    return parser.parse_args()

def print_args(args: argparse.Namespace) -> None:
    print("Значения аргументов:")
    print("name:", args.name)
    print("repo:", args.repo)
    print("version:", args.version)
    print("mode:", args.mode)
    print("graph:", args.graph)
    print("ascii:", args.ascii)

def main():
    print_args(get_args())


if __name__ == "__main__":
    main()