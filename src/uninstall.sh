#!/bin/bash
# Uninstalace aplikace
#
# Cílová složka
TDIR="/opt/gnuClassConf";
rm -r $TDIR;
# odstranění spouštěče
rm /usr/share/applications/gnuClassConf.desktop;
# vrácení zálohy interfaces
# optání se, zdali je má vrátit do původního stavu
bck="/etc/network/interfaces_ducked_back";
if [[ -r "$bck" ]];then
	echo "Konfigurační prostředí zálohovalo soubor";
	echo "/etc/network/interfaces, má se vrátit";
	echo "do původního stavu?"
	read -p "Zvolte (a) pro vrácení, (n) pro smazání: " y
	y=${y:-n}
	if [[ "$y" == "a" ]];then
		cat /etc/network/interfaces_ducked_back > /etc/network/interfaces;
	fi
fi
# Odstranění balíčků
echo "Odstraňuji balíčky, které prostředí nainstalovalo";
# optání se, zdali se maj purgnout
echo "Konfigurační prostředí nainstalovalo služby, které potřebuje pro svou činnost.";
echo "Mají se také s odinstalací odsranit?";
read -p "Zvolte (a) pro odstranění (p) pro odstranění i s konfiguračními soubory, (n) pro nic: " y
y=${y:-n}
if [[ "$y" == "a" ]];then
	apt-get remove isc-dhcp-server tftpd-hpa apache2 nfs-kernel-server tftpd-hpa syslinux debootstrap expect;
elif [[ "$y" == "p" ]];then
	apt-get remove --purge isc-dhcp-server tftpd-hpa apache2 nfs-kernel-server tftpd-hpa syslinux debootstrap expect;
fi
# Mazání obrazu
if [[ -d "/NFSROOT/" ]]; then
	echo "Při správě učebny bylo potřeba pracovat se složkou obsahující soubory pro třídu";
	echo "Mají se také s odinstalací odstranit?";
	read -p "Zvolte (a) pro odstranění, (n) pro nic: " y
	if [[ "$y" == "a" ]];then
		rm -r "/NFSROOT";
	fi
fi
