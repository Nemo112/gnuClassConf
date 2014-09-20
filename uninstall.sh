#!/bin/bash
# Uninstalace aplikace
# Cílová složka
TDIR="/opt/gnuClassConf";
rm -r $TDIR;
rm /usr/share/applications/gnuClassConf.desktop;
cat /etc/network/interfaces_ducked_back > /etc/network/interfaces;
echo "Odstraňuji balíčky, které prostředí nainstalovalo";
apt-get remove isc-dhcp-server tftpd-hpa apache2 nfs-kernel-server tftpd-hpa syslinux debootstrap expect;
