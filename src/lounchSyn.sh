#!/bin/bash
# Skript pro spuštění Synaptic nad obrazem klientských stanic
# test, zdali je synaptic instalován
isi=$(chroot /NFSROOT/class/ dpkg -l | grep ' synaptic ' | cut -d' ' -f1);
if [[ "$isi" != "ii" ]];then
	chroot /NFSROOT/class/ apt-get install --allow-unauthenticated synaptic -y --force-yes
fi
# test python-gtk2
isi=$(chroot /NFSROOT/class/ dpkg -l | grep ' python-gtk2 ' | cut -d' ' -f1);
if [[ "$isi" != "ii" ]];then
	chroot /NFSROOT/class/ apt-get install --allow-unauthenticated python-gtk2 -y --force-yes
fi
# test python-glade2
isi=$(chroot /NFSROOT/class/ dpkg -l | grep ' python-glade2 ' | cut -d' ' -f1);
if [[ "$isi" != "ii" ]];then
	chroot /NFSROOT/class/ apt-get install --allow-unauthenticated python-glade2 -y --force-yes
fi
# spuštění synaptic
if [[ ! -f "/NFSROOT/class/addons/synaL.sh" ]];then
	toi=$(cat <<EOF
#!/bin/bash
[[ "\$1" == "" ]] && exit 1;
export DISPLAY=\$1;
synaptic;
EOF
)
	printf "%s\n" "$toi" > "/NFSROOT/class/addons/synaL.sh";
	chmod 755 "/NFSROOT/class/addons/synaL.sh";
	xhost +;
	chroot /NFSROOT/class/ /addons/synaL.sh $DISPLAY;
else
	xhost +;
	chroot /NFSROOT/class/ /addons/synaL.sh $DISPLAY;
fi