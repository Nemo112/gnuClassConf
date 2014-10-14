#!/bin/bash
[[ $1 != "" ]] && exit 0;
export DEBIAN_FRONTEND=noninteractive;
apt-get install italc-master -y
