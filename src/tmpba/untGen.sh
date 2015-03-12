#!/bin/bash
umount -l "/NFSROOT/class/class_shares/test";
rmdir "/NFSROOT/class/class_shares/test";
umount -l "/NFSROOT/class/class_shares/materialy";
rmdir "/NFSROOT/class/class_shares/materialy";
exit 0;
