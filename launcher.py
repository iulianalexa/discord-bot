import subprocess
import sys

lc = (sys.executable, "main.py")

while True:
    try:
        code = subprocess.call(lc)
    except KeyboardInterrupt:
        code = 0
        break
    else:
        if code == 0:
            break
        else:
            print("An error occured. Restarting...")

