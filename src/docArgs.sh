#!/bin/bash
if [[ "$1" == "-h" ]];then
	echo "Projde všechny spustitelné skripty a vypíše jejich -h";
	exit 0;
fi
for i in `ls ./*.py ./*.sh`;do
	if [[ ! $i =~ mn.*\.py && ! $i =~ "install.sh" && ! $i =~ "uninstall.sh" \
		 && ! $i =~ test.*\.py && ! $i =~ "itWindow.py" && ! $i =~ "./closeSetup.py" \
		 && -x $i && ! $i =~ "main.py" && ! $i =~ "starter.sh" ]];then
		echo "Spustitelný skript $i"
		eval "$i -h";
		echo "===================================================="
	fi
done;
