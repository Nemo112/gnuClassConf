#!/bin/bash
nm="/usr/share/applications/gnuClassConf.desktop";
touch  $nm;
chmod 755  $nm;

toi=$(cat <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=gnuClassConf
GenericName=GUI konfigurační prostředí třídy
TryExec=gksu
Exec=gksu /opt/gnuClassConf/main.py
Terminal=false
Icon=/opt/gnuClassConf/iconst.png
Type=Application
Categories=Application;Network;Security;
Comment=Rozhraní pro nastavení klientských stanic v rámci lokální sítě
EOF
)
printf "%s\n" "$toi" > $nm;
