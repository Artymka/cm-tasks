import xml.etree.ElementTree as ET
from typing import Dict
import json
import hashlib


def read_vfs_form_xml(vfs_path: str) -> Dict:
    """Читает данные о vfs из файла xml и возвращает в виде словаря со структурой:
    'name': str - название файла/директории;
    'type': file или dir;
    'content': str - содержимое файла;
    'children': [] - вложенные папки/файлы;
    """

    tree = ET.parse(vfs_path)
    root = tree.getroot()
    
    vfs_dict = read_step(root)
    return vfs_dict

def read_step(dir_inf: ET.Element) -> Dict:
    """Обработка одной папки фалововой системы."""
    dir_dict = {'name': dir_inf.attrib['name'], 'type': 'dir', 'children': []}

    for dir in dir_inf.findall('dir'):
        # обработка всех папок, должна быть рекурсивной
        dir_dict['children'].append(read_step(dir))

    for file in dir_inf.findall('file'):
        # обработка файлов
        dir_dict['children'].append({
            'name': file.attrib['name'],
            'type': 'file',
            'content': file.attrib['content'],
        })
    
    return dir_dict

def get_vfs_info(vfs_dict: Dict) -> str:
    """Возвращает имя VFS, хеш SHA-256 объека в памяти (предварительно словарь преобразовывается в json с сортировкой ключей)."""
    res = 'VFS info:\n'
    res += 'VFS name: ' + vfs_dict['name'] + '\n'
    dict_str = json.dumps(vfs_dict, sort_keys=True, ensure_ascii=False)
    res += 'SHA-256: ' + hashlib.sha256(dict_str.encode('utf-8')).hexdigest() + '\n'
    return res
    
def get_vfs_structure(vfs_dict: Dict) -> str:
    """Возвращает структуру файлов и папок в vfs."""
    res = ''
    tab_size = 3
    offset = [0]
    stack = [vfs_dict]
    while len(stack):
        curr = stack.pop()
        tabs = offset.pop()

        res += ' ' * tabs * tab_size + curr['name'] + '\n'
        for child in curr['children']:
            if child['type'] == 'dir':
                stack.append(child)
                offset.append(tabs+1)
            else:
                res += ' ' * (tabs+1) * tab_size + child['name'] + ': ' + child['content'] + '\n'
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
        
