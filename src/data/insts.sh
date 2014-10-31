#!/bin/bash
export DEBIAN_FRONTEND=noninteractive;
apt-get install isc-dhcp-server iptables-persistent nfs-kernel-server tftpd-hpa syslinux debootstrap expect apache2 -y;
