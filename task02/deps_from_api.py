import json
from typing import List, Optional, Tuple
import urllib
import urllib.request


def get_crate_dependencies_from_api(crate_name: str, version: str) -> List[Tuple[str, str]]:
    """Получает зависимости пакета с crates.io через API"""
    url = f"https://crates.io/api/v1/crates/{crate_name}/{version}/dependencies"
    
    try:
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            res = []
            for dep in data["dependencies"]:
                res.append((dep["crate_id"], dep["req"]))
            return res
            
    except Exception as e:
        print(f"Ошибка при получении зависимостей через API: {e}")
        return []