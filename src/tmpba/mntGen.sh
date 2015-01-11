#!/bin/bash
mount --bind "/root/test1" "/NFSROOT/class/class_shares/test1";
mount -o remount,ro,bind "/root/test1" "/NFSROOT/class/class_shares/test1";
mount --bind "/root/test2" "/NFSROOT/class/class_shares/test2";
mount -o remount,rw,bind "/root/test2" "/NFSROOT/class/class_shares/test2";
exit 0;
