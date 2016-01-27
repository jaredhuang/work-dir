# run at this way
crontab -e
* * * * * php cron.php cron

### install mail
yum install mailx -y
cat > /etc/mail.rc <<EOF
set hold
set append
set ask
set crt
set dot
set keep
set emptybox
set indentprefix="> "
set quote
set sendcharsets=iso-8859-1,utf-8
set showname
set showto
set newmail=nopoll
set autocollapse
ignore received in-reply-to message-id references
ignore mime-version content-transfer-encoding
fwdretain subject date from to
set bsdcompat
set from=client_***@163.com
set smtp=smtp.163.com
set smtp-auth-user=client_***@163.com
set smtp-auth-password=****
set smtp-auth=login
EOF
