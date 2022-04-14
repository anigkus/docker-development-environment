# 1.Create crontab folder
```
➜  mkdir -p /opt/crontab/script
```
# 2.Create script
```
➜  cd /opt/crontab/script
➜  vi del_es_by_day.sh
#!/bin/bash
#
#author Anigkus
#delete the specified date index
#

#delete logs older than 15 days
date=`date -d "-15 days" "+%Y.%m.%d"`

#instance host
eth0="$(ip addr | grep 'eth0' | grep inet | awk '{print $2}' | awk -F/ '{print $1}')". #localhost
/usr/bin/curl -w '\n' -XDELETE "http://$eth0:9200/service-java-logs-$date"
/usr/bin/curl -w '\n' -XDELETE "http://$eth0:9200/k8s-pods-default-logs-$date"
/usr/bin/curl -w '\n'  -XDELETE "http://$eth0:9200/k8s-pods-systerm-logs-$date
```

# 3.Grant permission
```
➜  chmod -R 755 /opt/crontab/script
```

# 4.Configuration scheduling period
```
➜  crontab -e
#every minute
#01 00 * * * /opt/crontab/script/del_es_by_day.sh
#every day on one o'clock
00 01 * * * /opt/crontab/script/del_es_by_day.sh
```

# 5.Restart system crond service(Only edit script content not restart)
```
➜  systemctl restart crond
```

# 6. Delete the index for the specified between data
```
#!/bin/bash 
# 
#author Anigkus 
#delete the specified date interval index 
# 

start=$1
end=$2
start=${start//./-}
end=${end//./-}

startDate=`date -d "${start}" +%s`
endDate=`date -d "${end}" +%s`

stampDiff=`expr $endDate - $startDate`
dayDiff=`expr $stampDiff / 86400`

for((i=0;i<$dayDiff;i++))
do
    process_date=`date -d "${start} $i day" +'%Y.%m.%d'`
    #echo $process_date
    ##eureke instance host
    eth0="$(ip addr | grep 'eth0' | grep inet | awk '{print $2}' | awk -F/ '{print $1}')" #localhost
    /usr/bin/curl -w '\n' -XDELETE "http://$eth0:9201/service-java-logs-$process_date"
    /usr/bin/curl -w '\n' -XDELETE "http://$eth0:9201/k8s-pods-default-logs-$process_date"
    /usr/bin/curl -w '\n'  -XDELETE "http://$eth0:9201/k8s-pods-systerm-logs-$process_date"


done
```

