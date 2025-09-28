from __future__ import annotations
import xml.etree.ElementTree as ET
from typing import Dict
import json
import hashlib


class Node:
    def __init__(self,
                 name: str,
                 type: str,
                 parent: Node = None,
                 content: str = ""):
        self.name = name
        self.type = type
        self.parent = parent
        self.content = content
        self.children = []

    def add_child(self, node: Node) -> None:
        self.children.append(node)

    def get_child(self, name: str) -> Node | None:
        for child in self.children:
            if child.name == name:
                return child
        return None

    @classmethod
    def read_vfs_form_xml(cls, vfs_path: str) -> Node:
        """Читает данные о vfs из файла xml и возвращает в виде нода."""
        tree = ET.parse(vfs_path)
        root = tree.getroot()
        
        vfs_dict = cls._read_step(root)
        return vfs_dict
    
    @classmethod
    def _read_step(cls, dir_inf: ET.Element, parent: Node = None) -> Node:
        """Обрабатывает одну папку фалововой системы при чтении из файла."""
        dir_node = Node(
            dir_inf.attrib['name'],
            "dir",
            parent,
        )
        
        for dir in dir_inf.findall('dir'):
            # обработка всех папок, должна быть рекурсивной
            dir_node.add_child(Node._read_step(dir, dir_node))

        for file in dir_inf.findall('file'):
            # обработка файлов
            dir_node.add_child(Node(
                file.attrib['name'],
                "file",
                dir_node,
                file.attrib['content']
            ))
        
        return dir_node
    
    def _get_tree_root(self) -> Node:
        """Возвращает корневой элемент дерева VFS."""
        curr = self
        while curr.parent:
            curr = curr.parent
        return curr

    def get_vfs_info(self) -> str:
        """Возвращает имя VFS, хеш SHA-256 дерева в памяти (предварительно объект преобразуется в словарь, словарь преобразуется в json с сортировкой ключей)."""
        root = self._get_tree_root()
        # return root.to_dict()
        res = 'VFS info:\n'
        res += 'VFS name: ' + root.name + '\n'
        dict_str = json.dumps(root.to_dict(), sort_keys=True, ensure_ascii=False)
        res += 'SHA-256: ' + hashlib.sha256(dict_str.encode('utf-8')).hexdigest() + '\n'
        return res
    
    def get_vfs_structure(self) -> str:
        """Возвращает структуру файлов и папок в vfs."""
        root = self._get_tree_root()
        res = ''
        tab_size = 3
        offset = [0]
        stack = [root]
        while len(stack):
            curr = stack.pop()
            tabs = offset.pop()

            res += ' ' * tabs * tab_size + curr.name + '\n'
            for child in curr.children:
                if child.type == 'dir':
                    stack.append(child)
                    offset.append(tabs+1)
                else:
                    res += ' ' * (tabs+1) * tab_size + child.name + ': ' + child.content + '\n'
        return res
    
    def to_dict(self) -> Dict:
        """Возвращает всё дерево в виде словаря."""
        root = self._get_tree_root()
        res = self._to_dict_step(root)
        return res
        
    def _to_dict_step(self, dir: Node) -> Dict:
        """Преобразует одну директорию VFS в словарь."""
        res = dir.__dict__.copy()
        res["children"] = []
        del(res["parent"])
        for node in dir.children:
            if node.type == "dir":
                res['children'].append(self._to_dict_step(node))
            else:
                res['children'].append(node.__dict__.copy())
                del(res['children'][-1]['parent'])
        return res


"""
Структура vfs:
словарь, каждый элемент которого содержит три поля:
"name" - название файла/директории
"type" - file или dir
"content" - содержимое файла
"children" - вложенные папки/файлы

Постановка задачи:
создать переменную-словарь с содержимым vfs
создать функции для:
 - парса xml в словарь
 - вывода информации о vfs
 - вывода структуры vfs

структура xml:
<root name="...">
    <file name="" content=""></file>
    <dir name="">
        ...
    </dir>
</root>

"""
        
