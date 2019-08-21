#!/bin/sh
cur_dateTime=`date "+%Y-%m-%d %H:%M:%S "`
url="https://www.google.com/"
return_vpn=`curl -o /dev/null -s -w "%{http_code}" "${url}"`
if [ $return_vpn != '200' ];then
unset http_proxy && unset https_proxy && systemctl stop privoxy && pkill sslocal
nohup /usr/local/python3/bin/sslocal -c /etc/shadowsocks.json &>> /var/log/sslocal.log &
export http_proxy=http://127.0.0.1:8118 && export https_proxy=http://127.0.0.1:8118 && systemctl start privoxy
echo "${cur_dateTime}" >> /etc/logrotate.d/check_vpn.log
echo "vpn restart ..." >> /etc/logrotate.d/check_vpn.log
else
echo "vpn is ok ..." >> /etc/logrotate.d/check_vpn.log
fi
