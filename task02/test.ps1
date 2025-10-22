cd ./task02
Set-PSDebug -Trace 1
# $DebugPreference = "Continue"

py .\main.py

py .\main.py --help

py .\main.py -n smth -r smth -v 0.0.1

py .\main.py -n smth -r smth -v 123 -a

py .\main.py -n smth -r smth -v 123 -a extra

py .\main.py --n "my repo" -r smth -v 1.0.1 -mode unusual

py .\main.py --name "my repo" --repo "my path" --version 1.0.1 --mode unusual