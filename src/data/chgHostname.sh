#!/bin/bash
##
## Dávka pro změnu hostname
## Nové jméno je vybíráno z posledního oktetu IP a slova student
##
ip=`hostname --all-ip-addresses | awk '{print $(NF)}' `;
echo $ip
so=`hostname --all-ip-addresses | awk '{print $(NF)}'   | cut -d '.' -f 4`;
hs="student${so}";
echo $hs
## změna v /etc/hosts
while read -r line; do
	ts=`echo $line | grep ${ip} | grep ${hs}`
	[[ "$ts" != "" ]]  && {
		ins="1"
	}
done < "/etc/hosts"
[[ "$ins" != "1" ]] && {
	echo "${ip}	${hs}" >> "/etc/hosts";
}
## vytváření lokální kopie /etc/hostname
touch "/run/shm/hostname";
rm "/etc/hostname";
ln -s "/run/shm/hostname" "/etc/hostname";
## změna v /etc/hostname
echo "$hs" > "/etc/hostname"
hostname "$hs"
