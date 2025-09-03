import psutil


def get_vfs_name():
    """Возвращает тип файловой системы первого диска."""
    return psutil.disk_partitions()[0].fstype

if __name__ == "__main__":
    vfs_name = get_vfs_name()
    # после ошибки в приглашении к вводу будет крестик
    success_symbol = ":)"
    failure_symbol = ":("
    # success_symbol = "✔️"
    # failure_symbol = "❌"
    status_symbol = success_symbol
    success = True

    while True:
        if success:
            status_symbol = success_symbol
        else:
            status_symbol = failure_symbol

        inp = input(f"[ {vfs_name} ] {status_symbol} >")
        parts = inp.split()
        if not parts:
            continue

        cmd, *args = parts
        match cmd:
            case "ls":
                # имитация проверки аргументов
                success = True
                for arg in args:
                    if arg[0] != "-":
                        print("wrong argument")
                        success = False
                        break
                
                if not success:
                    continue                        
                print(cmd, args)
                success = True
            
            case "cd":
                # имитация проверки аргументов
                success = True
                for arg in args:
                    if arg[0] != "-":
                        print("wrong argument")
                        success = False
                        break
                
                if not success:
                    continue                        
                print(cmd, args)
                success = True

            case "exit":
                exit(0)

            case _:
                print("command not found")
                success = False
            
        

                
    
