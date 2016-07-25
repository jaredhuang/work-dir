#!/usr/bin/python
#coding:utf-8
import smtplib
import sys
from email.mime.text import MIMEText
from email.header import Header
from email.Utils import COMMASPACE
receiver = sys.argv[1]
subject = sys.argv[2]
mailbody = sys.argv[3]
smtpserver = 'mail.xxx.com'
username = 'xxx@xxx.com'
password = 'xxx'
sender = username
msg = MIMEText(sys.argv[3],'html','utf-8')
msg['Subject'] = Header(subject,'utf-8')
msg['From'] = username
msg['To'] = receiver
smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username,password)
smtp.starttls()
smtp.sendmail(msg['From'],msg['To'],msg.as_string())
smtp.quit()
