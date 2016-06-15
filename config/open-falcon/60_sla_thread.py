#!/bin/env python
# -*- coding: utf-8 -*-
import httplib
import urllib
import urllib2
import time
import json
import socket
import datetime
import thread
import requests
endpoint = 'sla'
start = 0
p  = []
# method : 0 ---> GET,1 ---->Post
# https:   0 ---> http, 1 --->https
# host :use for connect host and port
# metric: open-falcon metric
# uri: url
# params:post data
# tags: open-falcon tages;
urllist = [
#http Get
#www.51dba.com  weather  
    {
        'method':1,
        'https':0,
        'req':0,
        'host':'www.51dba.com',
        'metric':'www.51dba.com',
        'uri':'/xxxx/xxxx/index.php?_r=weather/weatherAction/getAddress',
        'params':'_s=0.20385dda18780&ws=',
        'tags':'weather/getAddress'
    },
#www.51dba.com  movie     
    {
        'method':1,
        'https':0,
        'req':0,
        'host':'www.51dba.com',
        'metric':'www.51dba.com',
        'uri':'/xxxx/xxxx/index.php?_r=mediaFactory/General/ShowSource',
        'params':'_s=891cb19b%3Ab5&ids=92243238&topCate=0001&factory=voole&fields=&ws=',
        'tags':'mediaFactory/ShowSource'
    },  
    {
        'method':1,
        'https':0,
        'req':0,
        'host':'www.51dba.com',
        'metric':'www.51dba.com',
        'uri':'/xxxxx/xxxx/index.php?_r=mediaFactory/General/ListRelation',
        'params':'_s=803e8573%3A8&resource_type=media&topCate=0001&factory=iqiyi&page=0&key=%7B%rce%22%3A%22voole%2Cv_sohu%2Ciqiyi%22%7D&pagesize=36&ws=',
        'tags':'mediaFactory/ShowSource'
    },
]

def HttpRequestGet(urlhost,metric,uri,tag):
    p = []
    val = 0
    url = urlhost+uri
    url ='http://%s%s' %(urlhost,uri)
    conn = None
    timestamp = int(time.time())
    tags = 'uri=%s' % (tag)
    try:
        response =requests.get(url)
        #print data 
        if response.status_code == 200:
            val = 1
        else:
            val = 0
        i = {
            'Metric': '%s' % (metric),
            'Endpoint': endpoint,
            'Timestamp': timestamp,
            'Step': 60,
            'Value': val,
            'CounterType': "GAUGE",
            'TAGS': tags
        }
        p.append(i)
    except Exception, e:
        val = 0
        i = {
            'Metric': '%s' % (metric),
            'Endpoint': endpoint,
            'Timestamp': timestamp,
            'Step': 60,
            'Value': val,
            'CounterType': "GAUGE",
            'TAGS': tags
        }
        p.append(i)
    try:
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
    except Exception, e:
        print e



def HttpMethodGet(urlhost,metric,uri,tag):
    p = []
    val = 0 
    timestamp = int(time.time())
    conn = None
    tags = 'uri=%s' % (tag)
    try:
        conn = httplib.HTTPConnection(urlhost) 
        conn.request("GET", uri)
        response = conn.getresponse()
        data = response.read()
        #print response.status
        if response.status == 200:
            val = 1
        else:
            val = 0
        i = {
            'Metric': '%s' % (metric),
            'Endpoint': endpoint,
            'Timestamp': timestamp,
            'Step': 60,
            'Value': val,
            'CounterType': "GAUGE",
            'TAGS': tags
        }
        p.append(i)
    except Exception, e:
        val = 0
        i = {
            'Metric': '%s' % (metric),
            'Endpoint': endpoint,
            'Timestamp': timestamp,
            'Step': 60,
            'Value': val,
            'CounterType': "GAUGE",
            'TAGS': tags
        }
        p.append(i)
    finally:
        if conn:
            conn.close()
    
    try:
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
    except Exception, e:
        print e

def HttpMethodPost(urlhost,metric,uri,params,tag):
    p = []
    val = 0 
    values = {
      'coocaa-ops-monitor':'2.96240ff591b241fdbf5caa6bfaa73eea',
    }
    headers = {
        'User-Agent': 'coocaa-ops-monitor',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    values = urllib.urlencode(values)
    timestamp = int(time.time())
    conn = None
    tags = 'uri=%s' % (tag)
    try:
        conn = httplib.HTTPConnection(urlhost)
        #print uri,tags
        conn.request("POST", uri, params,headers)
        response = conn.getresponse()
        data = response.read()
        if response.status == 200:
            val = 1
        else:
            val = 0

        i = {
                'Metric': '%s' % (metric),
                'Endpoint': endpoint,
                'Timestamp': timestamp,
                'Step': 60,
                'Value': val,
                'CounterType': "GAUGE",
                'TAGS': tags
                 }
        p.append(i)

    except Exception, e:
         print e
         i = {
                'Metric': '%s' % (metric),
                'Endpoint': endpoint,
                'Timestamp': timestamp,
                'Step': 60,
                'Value': 0,
                'CounterType': "GAUGE",
                'TAGS': tags
            }
         p.append(i)
    finally:
        if conn:
            conn.close()
    try:
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
    except Exception, e:
        print e


def HttpsMethodPost(urlhost,metric,uri,params,tag):
    p = []
    val = 0 
    headers = {
        'User-Agent': 'coocaa-ops-monitor',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    timestamp = int(time.time())
    conn = None
    tags = 'uri=%s' % (tag)
    try:
        conn = httplib.HTTPSConnection(urlhost)
        #print uri,tags
        conn.request("POST", uri, params,headers)
        response = conn.getresponse()
        data = response.read()
        if response.status == 200:
            val = 1
        else:
            val = 0

        i = {
                'Metric': '%s' % (metric),
                'Endpoint': endpoint,
                'Timestamp': timestamp,
                'Step': 60,
                'Value': val,
                'CounterType': "GAUGE",
                'TAGS': tags
                 }
        p.append(i)

    except Exception, e:
         print e
         i = {
                'Metric': '%s' % (metric),
                'Endpoint': endpoint,
                'Timestamp': timestamp,
                'Step': 60,
                'Value': 0,
                'CounterType': "GAUGE",
                'TAGS': tags
            }
         p.append(i)
    finally:
        if conn:
            conn.close()
    try:
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
    except Exception, e:
        print e

def main():

    now = datetime.datetime.now()
    print  now.strftime("%Y-%m-%d %H:%M:%S")
    for list in urllist:
        str1 = json.dumps(list)
        s = json.loads(str1)
        if s['req'] == 1:
            thread.start_new_thread(HttpRequestGet,(s['host'],s['metric'],s['uri'],s['tags']))
        elif s['method'] == 0:
            if s['https'] == 0: 
                thread.start_new_thread(HttpMethodGet,(s['host'],s['metric'],s['uri'],s['tags']))
        else:
            if s['https'] == 0 :
                thread.start_new_thread(HttpMethodPost,(s['host'],s['metric'],s['uri'],s['params'],s['tags']))
            else :
                thread.start_new_thread(HttpsMethodPost,(s['host'],s['metric'],s['uri'],s['params'],s['tags']))
    time.sleep(20)

if __name__ == '__main__':
    proc = 1 # commands.getoutput(' ps -ef|grep %s|grep -v grep|wc -l ' % os.path.basename(sys.argv[0]))
    if int(proc) < 5:
        main()
    
