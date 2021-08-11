import socket
import threading
import smtplib, ssl
from email.message import EmailMessage
import os
import datetime
import config



PORT = 2001
SERVER = '192.168.200.79'
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")


    while True:
        try:
            message = conn.recv(1024)
            print(f"[{addr}] {message}")
            stringdata = message.decode('ASCII')
            log(stringdata)
            if "OP" in stringdata:
                send_email("System Disarmed")
            elif "CL" in stringdata:
                send_email("System Armed")
            elif "Za" in stringdata:
                if "FRONT DOOR" in stringdata:
                    send_email("Alarm on FRONT DOOR")
                elif "HALLWAY MOTION" in stringdata:
                    send_email("Hallway Motion")
                elif "BACK DOOR" in stringdata:
                    send_email("Alarm on BACK DOOR")
                elif "BASEMENT DOOR" in stringdata:
                    send_email("Alarm on BASEMENT DOOR")
                elif "HALLWAY MOTION" in stringdata:
                    send_email("Alarm on HALLWAY MOTION")
            elif  "Zs" in stringdata:
                if "t 008" in stringdata:
                    send_email("WARNING: AC power failure")
                elif "t 000" in stringdata:
                    send_email("AC power restored")
            conn.sendall(message)
            conn.close()
        except socket.error:
            break


def log(message):
    with open('log.txt', 'a') as file:
        time = datetime.datetime.now()
        file.write(f"{message}-{time}\n")
        file.close()

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


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")


print("[STARTING] Server is starting")
start()
