#!/bin/bash
umount "/NFSROOT/class/class_shares/dataXorg";
rmdir "/NFSROOT/class/class_shares/dataXorg";
umount "/NFSROOT/class/class_shares/doc";
rmdir "/NFSROOT/class/class_shares/doc";
umount "/NFSROOT/class/class_shares/test";
rmdir "/NFSROOT/class/class_shares/test";
exit 0;
