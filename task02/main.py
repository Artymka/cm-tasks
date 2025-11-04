import argparse
import urllib.request
import urllib.error
import json
import os
from urllib.parse import urljoin
from typing import List, Optional, Tuple

from deps_from_api import get_crate_dependencies_from_api
from deps_from_toml import extract_dependencies_from_cargo_toml


def get_args() -> Optional[argparse.Namespace]:
    """Получает параметры из командной строки."""
    parser = argparse.ArgumentParser(description='Инстурумент визуализации графа зависимостей. Введите либо путь к локальному репозиторию пакета, либо имя и версию пакета для поиска в интернете.')
    
    parser.add_argument('--name', '-n', type=str, help='Имя анализируемого пакета')
    parser.add_argument('--repo', '-r', type=str, help='URL-адрес репозитория или путь к файлу тестового репозитория')
    parser.add_argument('--version', '-v', type=str, help='Версия пакета')
    parser.add_argument('--mode', '-m', type=str, default="default", help='Режим работы с тестовым репозиторием')
    parser.add_argument('--graph', '-g', type=str, default="./output.png", help='Имя сгенерированного файла с изображением графа')
    parser.add_argument('--ascii', '-a', action='store_true', help='Режим вывода зависимостей в формате ASCII-дерева')

    args = parser.parse_args()
    if not args.repo and (not args.version or not args.name):
        print("Должны быть указаны либо аргументы name и version, либо аргумент repo.")
        return None

    return args

def print_args(args: argparse.Namespace) -> None:
    """Выводит параметры командной строки в консоль."""
    print("Значения аргументов:")
    print("name:", args.name)
    print("repo:", args.repo)
    print("version:", args.version)
    print("mode:", args.mode)
    print("graph:", args.graph)
    print("ascii:", args.ascii)

def get_crate_dependencies_from_repo(crate_name: str, version: str, repo_url: str) -> List[Tuple[str, str]]:
    """Получает прямые зависимости пакета из репозитория."""
    dependencies = []
    
    try:
        # repo_url указывает на локальный файл
        if repo_url and os.path.exists(repo_url):
            with open(os.path.join(repo_url, "Cargo.toml"), 'r', encoding='utf-8') as file:
                content = file.read()
                dependencies = extract_dependencies_from_cargo_toml(content)
        
        # по name и version можно прочитать зависимости по api
        else:
            dependencies = get_crate_dependencies_from_api(crate_name, version)
            
    except Exception as e:
        print(f"Ошибка при получении зависимостей: {e}")
    
    return dependencies

def print_dependencies(dependencies: List[Tuple[str, str]]) -> None:
    """Выводит список зависимостей в удобочитаемом формате."""
    if not dependencies:
        print(f"Прямые зависимости для пакета не найдены.")
        return
    
    print(f"Прямые зависимости пакета:")
    for i, (dep_name, dep_version) in enumerate(dependencies, 1):
        print(f"{i}. {dep_name}: {dep_version}")


def main():
    args = get_args()
    if args == None:
        return
    
    print_args(args)
    
    # получение зависимостей
    dependencies = get_crate_dependencies_from_repo(args.name, args.version, args.repo)
    
    # вывод результата
    print_dependencies(dependencies)


if __name__ == "__main__":
    main()
