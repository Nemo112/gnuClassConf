#!/bin/bash
nm="/usr/share/applications/gnuClassConf.desktop";
touch  $nm;
chmod 755  $nm;
echo "[Desktop Entry]" > $nm;
echo "Encoding=UTF-8" >> $nm;
echo "Name=gnuClassConf" >> $nm;
echo "GenericName=GUI konfigurační prostředí třídy" >> $nm;
echo "TryExec=su-to-root" >> $nm;
echo "Exec=su-to-root -X -c /opt/gnuClassConf/main.py" >> $nm;
echo "Terminal=false" >> $nm;
echo "Icon=/opt/gnuClassConf/iconst.png" >> $nm; 
echo "Type=Application" >> $nm;
echo "Categories=Application;Network;Security;" >> $nm;
echo "Comment=Rozhraní pro nastavení klientských stanic v rámci lokální sítě" >> $nm;

