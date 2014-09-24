#!/bin/bash
#testování vstupů
if [[ "$1" == ""  ]];then
	echo "Použití ./$0 <vnitřní eth rozhraní> <vnější eth rozhraní>";
	exit 3;
fi

eths=(`ip link | awk 'BEGIN{FS=" "}{print $2}' | grep ".*:$" | tr -d ':'`);
ff=0;
sf=0;

for i in ${eths[@]};do
	[[ "$1" == "$i" ]] && { ff=1; }
	[[ "$2" == "$i" ]] && { sf=1; }
done;

[[ "$ff" == "0" ]] && { exit 1; }
[[ "$sf" == "0" ]] && { exit 1; }

[[ "$1" == "$2" ]] && { exit 2; }
if [[ -f "/etc/init.d/iptables-persistent" ]];then
	export DEBIAN_FRONTEND=noninteractive
	apt-get install iptables-persistent -y
fi
# nastavení iptables
/sbin/iptables -t nat -A POSTROUTING -o "$2" -j MASQUERADE
/sbin/iptables -A FORWARD -i "$2" -o "$1" -m state --state RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -A FORWARD -i "$1" -o "$2" -j ACCEPT
# nastavení routování
echo 1 > /proc/sys/net/ipv4/ip_forward
tm=`mktemp`;
ins=0;
# nastavení routování napořád
while read line;do
	if [[ $line  =~ net.ipv4.ip_forward ]];then
		echo "net.ipv4.ip_forward = 1" >> "$tm";
		ins=1;
	else
		echo "$line" >> "$tm";
	fi
done < "/etc/sysctl.conf";
if [[ "$ins" == "0" ]];then
	echo "net.ipv4.ip_forward = 1" >> "$tm";
fi
rm "/etc/sysctl.conf";
mv "$tm" "/etc/sysctl.conf";
# ukládání iptables
iptables-save > /etc/iptables/rules.v4
