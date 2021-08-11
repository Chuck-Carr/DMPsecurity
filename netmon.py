import os
import config
import smtplib, ssl
from email.message import EmailMessage

security_panel = "192.168.200.250"

def send_email(message):
    smtp_server = "smtp.gmail.com"
    port = 465
    sender_email = config.dmp_email
    password = config.dmp_password

    msg = EmailMessage()
    msg['Subject'] = "Activity on Home Security Panel."
    msg['From'] = 'HOME SECURITY'
    msg['TO'] = config.phone
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

def check_system(host):
    response = os.system("ping -n 1 " + host)
    print(response)
    if response != 0:
        send_email("Network Failure")

check_system(security_panel)

