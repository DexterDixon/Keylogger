import platform
import subprocess
#WMIC CSPRODUCT
import os
import socket

date = subprocess.check_output(["date"]).decode('utf-8')
f = open("log.txt", "a")
f.write(date)
f.close()
