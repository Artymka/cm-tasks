cd ./task02
Set-PSDebug -Trace 1

# не указаны нужные параметры
py .\main.py -n "net"

# неудачное чтение локального репозитория
py .\main.py -r "neverhood"

# неудачный поиск в интернете
py .\main.py -n "net" -v "neverhood"
py .\main.py -n "neverhood" -v "1.1.1"

# удачное чтение локального репозитория
py .\main.py -r ".\test_repo\clap-master"

# удачное чтение репозитория из интернета
py .\main.py -n "net" -v "0.0.2"