#!/bin/bash
umount -l "/NFSROOT/class/class_shares/test1";
rmdir "/NFSROOT/class/class_shares/test1";
umount -l "/NFSROOT/class/class_shares/test2";
rmdir "/NFSROOT/class/class_shares/test2";
exit 0;
