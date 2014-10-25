#!/bin/bash
# zkontroluje /addons/rules, při změně aplikuje změnu
# pauze mezi kontrolami
delay="10";
haf="/addons/harsh";
ncont="";
cont="";
while [ 1 ];do
	if [[ -f "$haf"  && -r "$haf" ]];then
		ncont="`cat $haf`";
	else
		ncont="";
	fi
	if [[ "$cont" != "$ncont" ]];then
		[[ -f /tmp/rules.sh ]] && { rm /tmp/rules.sh; };
		if [[ -f "/addons/rules.sh" && -r "/addons/rules.sh" ]];then
			cp /addons/rules.sh /tmp/rules.sh;
			chmod 755 /tmp/rules.sh;
			/tmp/rules.sh;
		fi
	fi
	if [[ -f "$haf"  && -r "$haf" ]];then 
		cont="`cat $haf`";
	else
		cont="";
	fi
	sleep "$delay";
done;
