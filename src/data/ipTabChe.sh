#!/bin/bash
# zkontroluje /addons/rules, při změně aplikuje změnu
# pauze mezi kontrolami
delay="5";

cont="";
while [ 1 ];do
	if [[ -f "/addons/rules.sh"  && -r "/addons/rules.sh" ]];then
		ncont="`cat /addons/rules.sh`";
	else
		ncont="";
	fi
	if [[ "$cont" != "$ncont" ]];then
		/addons/rules.sh;
	fi
	if [[ -f "/addons/rules.sh"  && -r "/addons/rules.sh" ]];then 
		cont="`cat /addons/rules.sh`";
	else
		cont="";
	fi
	sleep "$delay";
done;
