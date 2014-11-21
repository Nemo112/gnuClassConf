#!/bin/bash
mount -o ro,rbind "/root/doc" "/NFSROOT/class/class_shares/doc";
mount -o rw,rbind "/root/dataXorg" "/NFSROOT/class/class_shares/dataXorg";
exit 0;
