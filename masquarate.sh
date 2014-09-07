#!/bin/bash
#testování vstupů
[[ "$1" == ""  ]] && {
	echo "Použití ./$0 <vnitřní eth rozhraní> <vnější eth rozhraní>"
	exit 3;
}
[[ $1 =~ ^eth[0-9]*$ ]] || { exit 1; }
[[ $2 =~ ^eth[0-9]*$ ]] || { exit 1; }
[[ "$1" == "$2" ]] && { exit 2; }
[[ -f "/etc/init.d/iptables-persistent" ]] || {
	export DEBIAN_FRONTEND=noninteractive
	apt-get install iptables-persistent -y
}
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
	[[ $line  =~ net.ipv4.ip_forward ]] && {
		echo "net.ipv4.ip_forward = 1" >> "$tm";
		ins=1;
	} || {
		echo "$line" >> "$tm";
	}
done < "/etc/sysctl.conf";
[[ "$ins" == "0" ]] && {
	echo "net.ipv4.ip_forward = 1" >> "$tm";
}
rm "/etc/sysctl.conf";
mv "$tm" "/etc/sysctl.conf";
# ukládání iptables
iptables-save > /etc/iptables/rules.v4
