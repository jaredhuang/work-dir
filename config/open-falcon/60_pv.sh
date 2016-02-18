#!/bin/bash
#author: linuxhub.org
#note: only suport sequent format log order by time ,and only suport on time log

#LogFomat 
# 192.168.0.161 - - [26/Mar/2015:14:29:20 +0800] "GET / HTTP/1.1" 200 2126 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36" -


#please modify the log filenme 
#logfile=/data/logs/nginx/admin.kuaiyouxi.com.log
logfile=/data/logs/nginx/nginx_access.log 
isfind=0
start_time=`date -d"$last_minutes minutes ago" +"%H:%M:%S"`
#echo $logfile
#start_time="10:00:00"
stop_time=`date +"%H:%M:%S"`
sys_time=`date "+%s"`
#stop_time="10:01:00" 
pv=0
e_count=0
tac $logfile | awk  -v st="$start_time" -v et="$stop_time" -v stime="$sys_time" ' 
BEGIN{
    pv=0
    status_500=0
    status_502=0
    status_403=0
    status_404=0
    status_400=0
    status_499=0
    status_504=0
    response_gt100ms=0                                                                                                               
    response_gt200ms=0
    response_gt500ms=0
    response_gt1s=0
    response_lt100ms=0
    sumtime=0
    pv_200=1
    print "-------------------------------";
    print "s_time",st;
    print "e_time",et;
    print "-------------------------------";
}
 
{
    split($3,i,":");
    split($NF,j,"\"")
    #t=sprintf("%s:%s:%s",i[2],i[3],i[4]);
    t=substr($3,RSTART+14,21);
    if(t>=st && t<=et)
    {
         if($8=="500"){
           status_500++
         }
         if($8=="502"){
           status_502++
         }
         if($8=="400"){
           status_400++
         }
         if($8=="403"){
           status_403++
         }
         if($8=="404"){
           status_404++
         }
         if($8=="499"){
           status_499++
         }
         if($8=="504"){
           status_504++
         }
         if($8=="200"){
             pv_200++
             if(j[2]>=1)
                 response_gt1s++
             else if(j[2]>=0.5)
                 response_gt500ms++
             else if(j[2]>=0.2)
                 response_gt200ms++
             else if(j[2]>=0.1)
                 response_gt100ms++         
             else 
                 response_lt100ms++  
         }
         sumtime=sumtime+j[2]
         pv++
         e_count=0
         isfind=1
    }
    else 
    {
          if(isfind==1)
          {
             e_count++
             #Because the time is not order by sequent,user a lager number to avoid;
             if(e_count>5000) 
             {
                exit 
             }
          }
    }
}
END{
    if(pv==0)
       pv=1
    res_ms=(sumtime*1000)/pv
    print "pv.1minute.systime",stime
    print "pv.1minute",pv
    print "pv.1minute.500",status_500
    print "pv.1minute.500.percent",(status_500*100)/pv
    print "pv.1minute.502",status_502
    print "pv.1minute.502.percent",(status_502*100)/pv
    print "pv.1minute.400",status_400
    print "pv.1minute.400.percent",(status_400*100)/pv
    print "pv.1minute.403",status_403
    print "pv.1minute.403.percent",(status_403*100)/pv
    print "pv.1minute.404",status_404
    print "pv.1minute.404.percent",(status_404*100)/pv
    print "pv.1minute.499",status_499
    print "pv.1minute.499.percent",(status_499*100)/pv
    print "pv.1minute.504",status_504
    print "pv.1minute.504.percent",(status_504*100)/pv
    print "pv.1minute.responsetime",res_ms
    print "pv.1minute.response_gt1s",response_gt1s
    print "pv.1minute.response_gt1s_percent",(response_gt1s*100)/pv_200
    print "pv.1minute.response_gt500ms",response_gt500ms
    print "pv.1minute.response_gt500ms_percent",(response_gt500ms*100)/pv_200
    print "pv.1minute.response_gt200ms",response_gt200ms
    print "pv.1minute.response_gt200ms_percent",(response_gt200ms*100)/pv_200
    print "pv.1minute.response_gt100ms",response_gt100ms
    print "pv.1minute.response_gt100ms_percent",(response_gt100ms*100)/pv_200
    print "pv.1minute.response_lt100ms",response_lt100ms
    print "pv.1minute.response_lt100ms_percent",(response_lt100ms*100)/pv_200
}
'
