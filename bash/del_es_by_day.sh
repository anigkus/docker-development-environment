#1.#把脚本部署到ES所在的机器上


#新建crontab文件夹
[root@dev ~]# mkdir -p /opt/crontab/script
[root@dev ~]# cd /opt/crontab/script
[root@dev ~]# vi del_es_by_day.sh
#!/bin/bash
#
#author chunping
#delete the specified date index
#


#delete logs older than 15 days
date=`date -d "-15 days" "+%Y.%m.%d"`


#instance host
eth0="$(ip addr | grep 'eth0' | grep inet | awk '{print $2}' | awk -F/ '{print $1}')"
/usr/bin/curl -w '\n' -XDELETE "http://$eth0:9200/service-java-logs-$date"
/usr/bin/curl -w '\n' -XDELETE "http://$eth0:9200/k8s-pods-default-logs-$date"
/usr/bin/curl -w '\n'  -XDELETE "http://$eth0:9200/k8s-pods-systerm-logs-$date

#授权执行权限
[root@dev ~]# chmod -R 755 /opt/crontab/script


#2.做定时任务
[root@dev ~]#  crontab -e
#(每一分钟执行)
01 00 * * * /opt/crontab/script/del_es_by_day.sh
#(每天凌晨1点执行)
00 01 * * * /opt/crontab/script/del_es_by_day.sh

#启动或者重启定时任务服务(如果只是修改无需重启的)
[root@dev ~]# systemctl start crond

//删除指定日期间的索引

#!/bin/bash 
# 
#author chunping 
#delete the specified date interval index 
# 

start=$1
end=$2
start=${start//./-}
end=${end//./-}
##将输入的日期转为的时间戳格式
startDate=`date -d "${start}" +%s`
endDate=`date -d "${end}" +%s`
##计算两个时间戳的差值除于每天86400s即为天数差
stampDiff=`expr $endDate - $startDate`
dayDiff=`expr $stampDiff / 86400`
##根据天数差循环输出日期
for((i=0;i<$dayDiff;i++))
do
    process_date=`date -d "${start} $i day" +'%Y.%m.%d'`
    #echo $process_date
    ##eureke instance host
    eth0="$(ip addr | grep 'eth0' | grep inet | awk '{print $2}' | awk -F/ '{print $1}')"
    /usr/bin/curl -w '\n' -XDELETE "http://$eth0:9201/service-java-logs-$process_date"
    /usr/bin/curl -w '\n' -XDELETE "http://$eth0:9201/k8s-pods-default-logs-$process_date"
    /usr/bin/curl -w '\n'  -XDELETE "http://$eth0:9201/k8s-pods-systerm-logs-$process_date"


done
