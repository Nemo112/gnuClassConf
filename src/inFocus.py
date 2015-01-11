#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# \file inFocus.py
# \brief Řeší instalaci a odinstalaci balíčků

from ConsSys import ConsSys
from LogWrk import LogWrk
import os
from optparse import OptionParser
import subprocess


class inFocus:

    """ \brief Třída obsahující metody pro instalaci programů do obrazu
    """

    def __init__(self, path="/NFSROOT/class/addons/instFoc/"):
        """ Konstruktor třídy okna
        \param self Ukazatel na objekt
        \param path Cesta k instalačním skriptů
        """
        # Instance systémových nástrojů
        self.sy = ConsSys()
        # Cesta k instalačním skriptům
        self.path = path
        self.sy.makeDir(path)
        # Logovací třída
        self.log = LogWrk()

    def exCom(self, comm):
        """ Vykonej příkaz z comm
        \param comm Příkaz k vychování
        \param self Ukazatel na objekt
        """
        if "install" in comm.split():
            appNm = self.getApNmFrCom(comm)
            ts = self.getIfInst(appNm)
            # aplikace je přítomna, není potřeba instalovat
            if ts:
                return
        if "remove" in comm.split():
            appNm = self.getApNmFrCom(comm)
            ts = self.getIfInst(appNm)
            # aplikace je nepřítomna, není potřeba odstraňovat
            if not ts:
                return
        name = comm.replace(" ", "")
        nm = self.path + name + ".sh"
        self.sy.removeFl(nm)
        tar = open(nm, 'a')
        tar.write("#!/bin/bash\n")
        tar.write("export DEBIAN_FRONTEND=noninteractive\n")
        tar.write(comm + "\n")
        tar.close()
        os.chmod(nm, 0o755)
        tos = "chroot /NFSROOT/class /bin/bash -c ./addons/instFoc/" + \
            name + ".sh"
        for line in self.sy.runProcess(tos):
            print line,
            self.log.write(line)

    def dpkgConfA(self):
        """ Oprav konfigurace balíčků
        \param self Ukazatel na objekt
        """
        mn = False
        if os.path.isdir("/NFSROOT/class/proc") and len(os.listdir("/NFSROOT/class/proc")) <= 1:
            mn = True
            # mount proc /NFSROOT/class/proc -t proc
            tos = 'mount proc /NFSROOT/class/proc -t proc'
            for line in self.sy.runProcess(tos):
                print line,
                self.log.write(line)
            # mount sysfs /NFSROOT/class/sys -t sysfs
            tos = 'mount sysfs /NFSROOT/class/sys -t sysfs'
            for line in self.sy.runProcess(tos):
                print line,
                self.log.write(line)
        nm = self.path + "/clearConf.sh"
        self.sy.removeFl(nm)
        tar = open(nm, 'a')
        tar.write("#!/bin/bash\n")
        tar.write("export DEBIAN_FRONTEND=noninteractive\n")
        tar.write("dpkg --configure -a\n")
        tar.write("apt-get autoclean\n")
        tar.write("apt-get install -f\n")
        tar.close()
        os.chmod(nm, 0o755)
        tos = "chroot /NFSROOT/class /bin/bash -c ./addons/instFoc/clearConf.sh"
        for line in self.sy.runProcess(tos):
            print line,
            self.log.write(line)
        if mn:
            tos = 'umount -l /NFSROOT/class/proc'
            for line in self.sy.runProcess(tos):
                print line,
                self.log.write(line)
            tos = 'umount -l /NFSROOT/class/sys'
            for line in self.sy.runProcess(tos):
                print line,
                self.log.write(line)

    def aptAutorem(self):
        """ Autoremove balíčků z obrazu
        \param self Ukazatel na objekt
        """
        mn = False
        if os.path.isdir("/NFSROOT/class/proc") and len(os.listdir("/NFSROOT/class/proc")) <= 1:
            mn = True
            # mount proc /NFSROOT/class/proc -t proc
            tos = 'mount proc /NFSROOT/class/proc -t proc'
            for line in self.sy.runProcess(tos):
                print line,
                self.log.write(line)
            # mount sysfs /NFSROOT/class/sys -t sysfs
            tos = 'mount sysfs /NFSROOT/class/sys -t sysfs'
            for line in self.sy.runProcess(tos):
                print line,
                self.log.write(line)
        nm = self.path + "/autorem.sh"
        self.sy.removeFl(nm)
        tar = open(nm, 'a')
        tar.write("#!/bin/bash\n")
        tar.write("export DEBIAN_FRONTEND=noninteractive\n")
        tar.write("apt-get autoremove -y\n")
        tar.close()
        os.chmod(nm, 0o755)
        tos = "chroot /NFSROOT/class /bin/bash -c ./addons/instFoc/autorem.sh"
        for line in self.sy.runProcess(tos):
            print line,
            self.log.write(line)
        if mn:
            tos = 'umount -l /NFSROOT/class/proc'
            for line in self.sy.runProcess(tos):
                print line,
                self.log.write(line)
            tos = 'umount -l /NFSROOT/class/sys'
            for line in self.sy.runProcess(tos):
                print line,
                self.log.write(line)

    def uniXmlCo(self, name):
        """ Upravení installed souboru, kde jsou zapsány instalované účely
        \param self Ukazatel na objekt
        \param name Jméno odinstalovaného účelu
        """
        ts = ""
        for line in open("./focus/installed.cfg"):
            inm = line.replace("\n", "")
            if inm == name:
                continue
            else:
                ts = ts + line
        tar = open("./focus/installed.cfg", 'w')
        tar.write(ts)
        tar.close()

    def instXmlCo(self, name):
        """ Upravení installed souboru, kde jsou zapsány instalované účely
        \param self Ukazatel na objekt
        \param name Jméno instalovaného účelu
        """
        ts = ""
        for line in open("./focus/installed.cfg"):
            inm = line.replace("\n", "")
            if inm == name:
                return
            else:
                ts = ts + line
        ts = ts + "\n" + name
        tar = open("./focus/installed.cfg", 'w')
        tar.write(ts)
        tar.close()

    def getLstInst(self):
        """ Přečtení listu instalovaných účelů
        \param self Ukazatel na objekt
        """
        ts = []
        for line in open("./focus/installed.cfg"):
            ln = line.replace("\n", "").replace(" ", "")
            if ln == "":
                continue
            if ln.split(".")[1] == "gml":
                ts.append(ln)
        return ts

    def getApNmFrCom(self, com):
        """ Vyparsuje jméno aplikace z instalačního příkazu
        \param self Ukazatel na objekt
        \param com Příkaz pro instalaci aplikace
        \return String obsahující jméno aplikace
        """
        comm = com.replace(
            "install",
            "").replace(
            "--force-yes",
            "").replace(
            "apt-get",
            "").replace(
                "-y",
                "").replace(
                    "remove",
                    "").replace(
                        "autoremove",
            "")
        return comm.replace("--allow-unauthenticated", "").replace(" ", "")

    def getIfInst(self, nm):
        """ Přečtení listu instalovaných účelů
        \param self Ukazatel na objekt
        \param nm Name of package
        \return True pakliže je balíček nainstalovaný, false pokud ne
        """
        tos = "chroot /NFSROOT/class dpkg --get-selections"

        process = subprocess.Popen(tos.split(), stdout=subprocess.PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        for line in output.split("\n"):
            # print line.split()[0]
            if len(line.split()) >= 2:
                if nm in line.split()[0] and line.split()[1] == "install":
                    return True
        return False
if __name__ == "__main__":
    # Parser argumentů a parametrů
    parser = OptionParser(
        usage="usage: %prog [args]\n Work with focuses in client filesystem")
    parser.add_option(
        "-l",
        "--installed-list",
        action="store_true",
        dest="lst",
        default=False,
        help="Give a list of installed focuses")
    parser.add_option(
        "-c",
        "--clean-dpkg",
        action="store_true",
        dest="cle",
        default=False,
        help="Clean dpkg, apt and force install apt-get packages which failed")
    parser.add_option(
        "-r",
        "--auto-rem",
        action="store_true",
        dest="rem",
        default=False,
        help="Clean image by apt-get autoremove")
    # Argumenty a parametry z parseru
    (args, opts) = parser.parse_args()
    # Instance objektu
    f = inFocus()
    if args.lst:
        for i in f.getLstInst():
            print i
    if args.cle:
        f.dpkgConfA()
    if args.rem:
        f.aptAutorem()
