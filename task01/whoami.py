import os
import getpass
from typing import Tuple, Dict


def whoami_logic(args: list[str], g: Dict) -> Tuple[bool, str]:
    """Кроссплатформенное получение имени текущего пользователя."""
    try:
        # Способ 1: через getpass (надежнее)
        return True, f"current user: {getpass.getuser()}\n"
    except Exception:
        try:
            # Способ 2: через переменные окружения
            return True, f"current user: {os.getenv('USER') or os.getenv('USERNAME') or os.getenv('LOGNAME')}\n"
        except Exception:
            return False, "can't define the user\n"