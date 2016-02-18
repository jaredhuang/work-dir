#!/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import commands
import socket
import urllib2, base64
import json
import string
def main():
    hostname = socket.gethostname()
    p = []
    data = []
    dist = {}
    ctime = 0
    for line in open("var/app.log"):
       data.append(line.strip('\n'))
    for k,v in enumerate(data):
        j = v.split(" ")
        print j
        for i in range(len(j)):
            if(j[i]=="pv.1minute.systime"):
                ctime = j[i+1]
            if(j[i].startswith("pv.")  and 0!=cmp(j[i],"pv.1minute.systime")):
                m = {
                    'Metric': '%s' % (j[i]),
                    'Endpoint': hostname,
                    'Timestamp':  string.atoi(ctime),
                    'Step': 60,
                    'Value':  string.atof(j[i+1]),
                    'CounterType': "GAUGE",
                    'TAGS': ''
                }
                p.append(m)
 
    if(len(p)<1):
        return 
    hostname = socket.gethostname()
    print json.dumps(p, sort_keys=True,indent=4)
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)
    url = 'http://127.0.0.1:1988/v1/push'
    request = urllib2.Request(url, data=json.dumps(p) )
    request.add_header("Content-Type",'application/json')
    request.get_method = lambda: method
    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e

    # check. Substitute with appropriate HTTP code.
    if connection.code == 200:
        print connection.read()
    else:
        print '{"err":1,"msg":"%s"}' % connection


if __name__ == '__main__':
    proc = commands.getoutput(' ps -ef|grep %s|grep -v grep|wc -l ' % os.path.basename(sys.argv[0]))
    if int(proc) < 5:
        main()
