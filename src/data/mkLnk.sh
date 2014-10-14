#!/bin/bash
# najde home složku studenta
hm=`cat /etc/passwd | awk 'BEGIN{ FS=":" }/student/{print $6}'`;
# vloží odkaz do Desktop home složky studenta
[[ -h "$hm/Desktop/sdílení" ]] || {
	ln -s "/class_shares" "$hm/Desktop/sdílení";
}
