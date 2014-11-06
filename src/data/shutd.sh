#!/bin/bash
# zkontroluje /run/shm/hlt, pokud obsahuje 1, vypne počítač
# pauze mezi kontrolami
delay="10";
haf="/run/shm/hlt";
cont="";
while [[ 1 ]];do
	if [[ -f "$haf"  && -r "$haf" ]];then
		cont="`cat $haf`";
	else
		cont="";
	fi
	if [[ "$cont" == "1" ]];then
		shutdown -h now;
	fi
	if [[ "$cont" == "2" ]];then
		shutdown -r now;
	fi
	sleep "$delay";
done;