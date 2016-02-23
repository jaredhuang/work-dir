#!/usr/bin/python
#coding=utf-8

import re,sys,os,time,datetime
import pexpect
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

prompt = '[$#>]'
ssh_newkey='Are you sure you want to continue connecting'
rsync_prompt='total size.*'

ip_list=["0.0.0.0","0.0.0.0"]
user="username"
password="password"
local_path="/root/.jenkins/jobs/testtest/workspace/submitinfo.tar.gz"
target_path="/data/www/submitinfo.tar.gz"
log_path="/data/tmplog/devicesubmitInfo/fabu_"
command="md5sum %s" %(target_path)
server_script_exec="sh /data/www/device-sumbit.sh"
cur_time = time.strftime('%Y_%m_%d_%H_%M')
log_file_name = log_path + cur_time + ".log" 

#压缩文件
path = "/root/.jenkins/jobs/testtest/workspace"
tar_name = "submitinfo.tar.gz"
dir_name = "*"
os.system("cd %s && rm submitinfo.tar.gz;tar -czvf %s %s;cd -" %(path, tar_name, dir_name))

recipientas_list=["huang@xxxx.com","li@xxxx.com"]
addresser='xxxxxx@xxxx.com'
itheme= 'testtest的生产环境版本更新发布'
email_server_IP='smtp.xxxx.com'
mail_user="dddddd@xxxx.com"
mail_pass="xxxx.password"

def send_email_succeed(recipientas_list,addresser,itheme,email_server_IP,log_file_name,server_ip,local_file_md5,target_file_md5):
    msg = MIMEMultipart()
    msg['Subject'] = itheme
    msg['From'] = addresser
    msg['To'] = ";".join(recipientas_list)
    html_succeed = """\
        <html>
        <head></head>
        <META http-equiv=Content-Type content="text/html; charset=utf-8">
        <body>
        <p>Hi,各位伙伴<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<font color="green" size=5 ><====服务器IP %s ====> testtest的生产环境版本更新发布成功.</font><br><br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<font size=5 >如发现版本有问题,请及时联系黄工,电话:</font><font color="green" size=5 > **********</font><br><br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<font size=5 >本地版本文件MD5:   </font><font color="green" size=5 >%s</font><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<font size=5 >服务器版本文件MD5: </font><font color="green" size=5 >%s</font></font><br>
        </p>
        </body>
        </html>"""%(server_ip, local_file_md5, target_file_md5)
    part1 = MIMEText(html_succeed, 'html',_charset="utf-8")
    
    #fp = open(log_file_name, 'rb')
    #part2 = MIMEText(fp.read(), 'plain',_charset="utf-8")
    #fp.close()

    msg.attach(part1)
    #msg.attach(part2)

    try:
        s = smtplib.SMTP()
        s.connect(email_server_IP)
        s.login(mail_user,mail_pass)
        s.sendmail(addresser, recipientas_list, msg.as_string())
        s.quit()
    except Exception, e:
        print str(e)
        return False

def send_email_fail(recipientas_list,addresser,itheme,email_server_IP,log_file_name,server_ip,local_file_md5,target_file_md5):

    msg = MIMEMultipart()
    msg['Subject'] = itheme
    msg['From'] = addresser
    msg['To'] = ";".join(recipientas_list)

    html_succeed = """\
        <html>
        <head></head>
        <META http-equiv=Content-Type content="text/html; charset=utf-8">
         <body>
        <p>Hi,各位伙伴<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<font color="red" size=5 ><====服务器IP %s ====> testtest的生产环境版本更新发布失败,</font><font size=5 >附件有详细发布日志,请查看.</font><br><br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<font color="red" size=5 >请及时联系黄工,电话:</font><font color="green" size=5 > dddddddddddd </font><br><br><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<font color="red" size=5 >本地版本文件MD5:   </font><font color="green" size=5 >%s</font><br>
        &nbsp;&nbsp;&nbsp;&nbsp;<font color="red" size=5 >服务器版本文件MD5: </font><font color="green" size=5 >%s</font><br>
        </p>
        </body>
        </html>
        """%(server_ip, local_file_md5, target_file_md5)
    part1 = MIMEText(html_succeed, 'html',_charset="utf-8")

    #fp = open(log_file_name, 'rb')
    #part2 = MIMEText(fp.read(), 'plain',_charset="utf-8")
    #fp.close()

    msg.attach(part1)
    #msg.attach(part2)

    try:
        s = smtplib.SMTP()
        s.connect(email_server_IP)
        s.login(mail_user,mail_pass)
        s.sendmail(addresser, recipientas_list, msg.as_string())
        s.quit()
    except Exception, e:
        print str(e)
        return False
for server_ip in ip_list:
    log_file = open(log_file_name, "a")
    child=pexpect.spawn('/usr/bin/rsync -e "ssh -p 22" -avzcP %s %s@%s:%s' %(local_path, user, server_ip, target_path))
    child.logfile=log_file
    
    index = child.expect([ssh_newkey, 'password: ', pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        child.sendline('yes')
        child.expect ('password: ')
        child.sendline(password)
        child.expect(rsync_prompt,timeout=None)
    elif index == 1:
        child.sendline(password)
        child.expect(rsync_prompt,timeout=None)
    elif index == 2:
        print "%s rsync: %s EOF ERROR %s" %('#'*10, server_ip, '#'*10)
    elif index == 3:
        print "%s rsync: %s TIMEOUT ERROR %s" %('#'*10, server_ip, '#'*10)
        
    log_file.close()
    child.close()
    
    time.sleep(5)
    
    log_file = open(log_file_name, "a")
    child=pexpect.spawn("/usr/bin/ssh -p 22 %s@%s" %(user, server_ip))
    child.logfile=log_file
    
    index = child.expect([ssh_newkey, 'password: ', pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        child.sendline('yes')
        child.expect ('password: ')
        child.sendline(password)
        child.expect (prompt)
        child.sendline(command)
        child.expect (prompt)
        child.sendline('exit')
    elif index == 1:
        child.sendline(password)
        child.expect (prompt)
        child.sendline(command)
        child.expect (prompt)
        child.sendline('exit')
    elif index == 2:
        print "%s ssh: %s EOF ERROR %s" %('#'*10, server_ip, '#'*10)
    elif index == 3:
        print "%s ssh: %s TIMEOUT ERROR %s" %('#'*10, server_ip, '#'*10)
        
    log_file.close()
    child.close()
    
    os.system("md5sum %s | awk '{print $1}' > /data/tmplog/devicesubmitInfo/upload_file_local.log" %(local_path))
    os.system("grep %s %s | awk '{print $1}' | egrep -v 'md5sum|omadmin' | tail -n 1  > /data/tmplog/devicesubmitInfo/upload_file_remote.log" %(target_path, log_file_name))
        
    for localmd5 in open("/data/tmplog/devicesubmitInfo/upload_file_local.log"):
        local_file_md5 = localmd5
    
    for remotemd5 in open("/data/tmplog/devicesubmitInfo/upload_file_remote.log"):
        target_file_md5 = remotemd5
        
    if target_file_md5 == local_file_md5:
        log_file = open(log_file_name, "a")
        child=pexpect.spawn("/usr/bin/ssh -p 22 %s@%s" %(user, server_ip))
        child.logfile=log_file
        
        index = child.expect(['password: ', pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            child.sendline(password)
            child.expect (prompt)
            child.sendline(server_script_exec)
            child.expect (prompt)
            child.sendline('exit')
        elif index == 1: 
            print "%s script exec: %s EOF ERROR %s" %('#'*10, server_ip, '#'*10)
        elif index == 2:
            print "%s script exec: %s TIMEOUT ERROR %s" %('#'*10, server_ip, '#'*10)

        send_email_succeed(recipientas_list,addresser,itheme,email_server_IP,log_file_name,server_ip,local_file_md5,target_file_md5)
    else:
        send_email_fail(recipientas_list,addresser,itheme,email_server_IP,log_file_name,server_ip,local_file_md5,target_file_md5)
