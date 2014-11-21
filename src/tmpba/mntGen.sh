#!/bin/bash
mount -o rw,rbind "/root/dataXorg" "/NFSROOT/class/class_shares/dataXorg";
mount -o r,rbind "/root/doc" "/NFSROOT/class/class_shares/doc";
mount -o rw,rbind "/root/test" "/NFSROOT/class/class_shares/test";
exit 0;
