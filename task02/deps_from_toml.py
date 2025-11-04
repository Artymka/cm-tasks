import re
from typing import List, Tuple


def extract_dependencies_from_cargo_toml(content: str) -> List[Tuple[str, str]]:
    """
    Извлекает зависимости из содержимого Cargo.toml с помощью регулярных выражений.
    Возвращает список кортежей (имя_пакета, версия).
    """
    dependencies = []
    
    # Регулярное выражение для поиска зависимостей в формате [dependencies]
    # dep_pattern = r"\[dev-dependencies\]\s*(.*?)(?=\n\s*\[|\Z)"
    dep_pattern = r"\[dependencies\]\s*(.*?)(?=\n\s*\[|\Z)"
    dep_section_match = re.search(dep_pattern, content, re.DOTALL)
    
    if dep_section_match:
        dep_section = dep_section_match.group(1)
        
        # Регулярное выражение для извлечения имени пакета и версии
        # Формат:
        # clap_builder = { path = "./clap_builder", version = "=4.5.51", default-features = false }
        # clap_builder = "4.5.51"
        package_pattern1 = r'^([a-zA-Z0-9_-]+)\s*=\s*"([^"]+)"'
        package_pattern2 = r'^([a-zA-Z0-9_-]+)\s*=\s*\{.*?version\s*=\s*"([^"]+)"'
        matches = re.findall(package_pattern1, dep_section, re.MULTILINE) + \
                  re.findall(package_pattern2, dep_section, re.MULTILINE)
        
        for package_name, version in matches:            
            dependencies.append((package_name, version))
    
    return dependencies