#!/bin/bash
name="gnuClassConf";
version="0.01.`git rev-list --count HEAD`";
desc="Aplikace pro správu síťové učebny v rámci LAN.";
rel="pxelinux.0";
if [[ "$1" == "vb" ]];then
	name="gnuClassConf";
	rel="virtualbox";
	desc="Aplikace pro správu síťové učebny v rámci LAN - VB verze.";
fi
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
# create install scripts
touch tmp/DEBIAN/preinst;
cat ./src/preinst > tmp/DEBIAN/preinst;
chmod +x tmp/DEBIAN/preinst;

touch tmp/DEBIAN/postinst;
cat ./src/postinst > tmp/DEBIAN/postinst;
chmod +x tmp/DEBIAN/postinst;

touch tmp/DEBIAN/postrm;
cat ./src/postrm > tmp/DEBIAN/postrm;
chmod +x tmp/DEBIAN/postrm;
#==================================
# copy icon
cp iconst.png ./tmp/usr/share/pixmaps/$name.png;
#==================================
# copy shortcut
toi=$(cat <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=$name
GenericName=GUI konfigurační prostředí třídy
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
rm -r ./tmp/opt/${name}/*\.pyc;
echo "# List sdílených složek" > ./tmp/opt/${name}/configuration/shared;
int=$(cat <<EOF
### Konfigurační soubor pro rozhraní učebny
### Neupravujte pokud nebudete vysloveně muset
### Obsah se přepisuje podle volby v "Základní nastavení učebny"

### in je rozhraní pro učebnu
in=

### out je rozhraní pro vnější síť
out=
EOF
)
printf "%s\n" "$int" > ./tmp/opt/${name}/configuration/interfaces;
echo "" > ./tmp/opt/${name}/data/work_logs.log;
#==================================
#rewriting tftp path in class.conf setup
toi=$(cat <<EOF
# Cesta k PXE souboru, které je popsán v DCHP konfiguračním souboru.
# Pokud je path nastavena na virtualbox, prostředí vyplní parametry PXE
# pro testování ve virtualboxu.
path=$rel
EOF
)
printf "%s\n" "$toi" > ./tmp/opt/${name}/configuration/tftpath;
#==================================
# making control
size=`du -s ./tmp/usr/`;
toi=$(cat <<EOF
Package: $name
Version: $version
Priority: optional
Recommends: python
Depends: python-tk | python (>= 2.7.6) | gksu 
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
if [[ "$1" == "vb" ]];then
	sudo dpkg-deb -b ./tmp ${name}_${version}_all_vb.deb 1>/dev/null;
	echo ${name}_${version}_all_vb.deb;
else
	sudo dpkg-deb -b ./tmp ${name}_${version}_all.deb 1>/dev/null;
	echo ${name}_${version}_all.deb;
fi
rm -r ./tmp;
