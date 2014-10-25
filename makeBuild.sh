#!/bin/bash
name="gnuClassConf";
version="0.001";
desc="Aplikace pro správu síťové učebny v rámci LAN.";
#==================================
# directory structure build
mkdir tmp;
cd tmp;
mkdir DEBIAN;
mkdir usr;
mkdir usr/share;
mkdir usr/share/applications;
mkdir opt;
mkdir opt/${name};
mkdir usr/share/man/;
mkdir usr/share/man/man1/;
mkdir usr/share/pixmaps;
cd ..;
#==================================
# copy icon
cp iconst.png ./tmp/usr/share/pixmaps/$name.png;
#==================================
# copy shortcut
toi=$(cat <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=gnuClassConf
GenericName=GUI konfigurační prostředí třídy
TryExec=gksu
Exec=gksu /opt/${name}/main.py
Terminal=false
Icon=/usr/share/pixmaps/$name.png
Type=Application
Categories=Network
Comment=$desc
EOF
)
printf "%s\n" "$toi" > ./tmp/usr/share/applications/$name.desktop;
#==================================
# copy of files
cp -r ./src/* ./tmp/opt/${name}/;
#==================================
# making control
size=`du -s ./tmp/usr/`;
toi=$(cat <<EOF
Package: $name
Version: $version
Priority: optional
Recommends: python
Depends: python-tk | python (>= 2.7.6) 
Architecture: all
Installed-Size: $size
Maintainer: Martin_Beranek <beranm14@fit.cvut.cz>
Description: $desc
 .
 http://nemor.cz/
EOF
)
printf "%s\n" "$toi" > ./tmp/DEBIAN/control;
#==================================
# making md5 sum
find ./src/* -type f ! -regex '^DEBIAN/.*' -exec md5sum {} \; > ./tmp/DEBIAN/md5sums;
#==================================
# making man page
cp $name.1 bckman;
gzip $name.1;
mv $name.1.gz ./tmp/usr/share/man/man1/;
mv bckman $name.1;
#==================================
# making deb
sudo chown -hR root:root ./tmp;
sudo dpkg-deb -b ./tmp ${name}_${version}_all.deb;
rm -r ./tmp;