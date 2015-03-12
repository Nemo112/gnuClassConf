#!/bin/bash
mount --bind "/home/ucitel/test" "/NFSROOT/class/class_shares/test";
mount -o remount,rw,bind "/home/ucitel/test" "/NFSROOT/class/class_shares/test";
mount --bind "/home/ucitel/materialy" "/NFSROOT/class/class_shares/materialy";
mount -o remount,ro,bind "/home/ucitel/materialy" "/NFSROOT/class/class_shares/materialy";
exit 0;
