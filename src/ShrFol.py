#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file ShrFol.py
# \brief Třída s metodami pro sdílení souborů do obrazu klientských počítačů

import os
import shutil
import subprocess
from optparse import OptionParser
from ConsSys import ConsSys
from LogWrk import LogWrk


class ShrFol:

    """ \brief Třída s metodami pro sdílení souborů do obrazu klientských počítačů
    """

    def __init__(self, pth="./configuration/shared"):
        """ Konstruktor třídy okna
        \param self Ukazatel na objekt
        \param pth Cesta k souboru listu sdílených složek
        """
        # Cesta ke konfiguračnímu souboru
        self.path = pth
        # Logovací třída
        self.log = LogWrk()
        # Instance třídy pro práci se systémem
        self.sy = ConsSys()

    def shList(self):
        """ Vrací list sdílených složek
        \param self Ukazatel na objekt
        \return List sdílených složek
        """
        toR = []
        if os.path.isfile(self.path):
            fl = open(self.path, "r")
            cnt = fl.read()
            for line in cnt.split("\n"):
                tl = line.find("#")
                if tl == -1:
                    tr = line
                else:
                    tr = line[0:tl]
                if tr.replace(" ", "") != "":
                    spl = tr.split(";")
                    toa = {}
                    toa['path'] = spl[0]
                    if len(spl) > 1:
                        toa['righ'] = spl[1]
                    else:
                        toa['righ'] = "rw"
                    toR.append(toa)
            fl.close()
        else:
            return
        return toR

    def addToList(self, add, righ="rw"):
        """ Přidá na list sdílení složku
        \param self Ukazatel na objekt
        \param add String obsahující cestu ke složce
        \param righ String obsahující jaká práva se použijí
        \return True pokud složka existuje a je přidána, jinak False
        """
        if add in self.shList():
            return
        if os.path.isfile(self.path):
            if os.path.isdir(add):
                fl = open(self.path, "a")
                fl.write(add + ";" + righ + "\n")
                fl.close()
        else:
            return
        # nasdílí složku
        self.mntByPa(add, righ)

    def mntByPa(self, it, ri):
        """ Připojí složku
        \param it Cesta ke složce
        \param ri Práva ke složce
        \param self Ukazatel na objekt
        """
        nm = it.split("/")[-1]
        if not os.path.isdir("/NFSROOT/class/class_shares/" + nm):
            os.makedirs("/NFSROOT/class/class_shares/" + nm)
            shutil.copymode(it, "/NFSROOT/class/class_shares/" + nm)
        else:
            self.uMntLst(it)
            os.makedirs("/NFSROOT/class/class_shares/" + nm)
            shutil.copymode(it, "/NFSROOT/class/class_shares/" + nm)

        exs = ["mount", "--bind", it, "/NFSROOT/class/class_shares/" + nm]
        exd = [
            "mount",
            "-o",
            "remount," +
            ri +
            ",bind",
            it,
            "/NFSROOT/class/class_shares/" +
            nm]

        for line in self.sy.runProcess("mount"):
            if len(line.split()) > 2:
                if line.split()[2] == "/NFSROOT/class/class_shares/" + nm:
                    umt = ["umount", "-l", "/NFSROOT/class/class_shares/" + nm]
                    p = subprocess.call(umt)

        p = subprocess.call(
            exs,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        p = subprocess.call(
            exd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

    def uMntAll(self):
        """ Odebere mount složky a smaže všechny složky
        \param self Ukazatel na objekt
        """
        exe = ["./tmpba/untGen.sh"]
        p = subprocess.call(
            exe,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

    def uMntLst(self, dele):
        """ Odebere mount složky a smaže jí
        \param self Ukazatel na objekt
        \param dele String obsahující jméno složky k odstranění
        """
        nm = dele.split("/")[-1]
        if os.path.isdir("/NFSROOT/class/class_shares/" + nm):
            for line in self.sy.runProcess("mount"):
                if len(line.split()) > 2:
                    if line.split()[2] == "/NFSROOT/class/class_shares/" + nm:
                        exe = [
                            "umount",
                            "-l",
                            "/NFSROOT/class/class_shares/" +
                            nm]
                        p = subprocess.Popen(
                            exe,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
                        val, err = p.communicate()
                        print val
                        print "/NFSROOT/class/class_shares/" + nm, " umounted"
            exe = ["rm", "-r", "/NFSROOT/class/class_shares/" + nm]
            p = subprocess.call(
                exe,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

    def remFrList(self, dele):
        """ Odebere z listu sdílených složek
        \param self Ukazatel na objekt
        \param dele String obsahující jméno složky k odstranění
        """
        if os.path.isfile(self.path):
            fl = open(self.path, "r")
            cnt = fl.read()
            fl.close()
            ts = ""
            for ln in cnt.split("\n"):
                if ln.replace(" ", "") == "":
                    continue
                line = ""
                if "#" in ln:
                    line = ln[0:ln.find("#")]
                else:
                    line = ln
                if dele != line.split(";")[0]:
                    ts = ts + ln + "\n"
            fl = open(self.path, "w")
            cnt = fl.write(ts)
            fl.close()

    def genListSh(self):
        """ Vygeneruje dávky pro sdílení složek do obrazu
        První v  ./tmpba/mntGen.sh vegeneruje mount složek
        První v  ./tmpba/untGen.sh vegeneruje umount složek
        \param self Ukazatel na objekt
        """
        # mount
        lst = self.shList()
        if not os.path.isdir("/NFSROOT/class/class_shares"):
            os.makedirs("/NFSROOT/class/class_shares")
        tos = "#!/bin/bash\n"
        for it in lst:
            nm = it['path'].split("/")[-1]
            if not os.path.isdir("/NFSROOT/class/class_shares/" + nm):
                os.makedirs("/NFSROOT/class/class_shares/" + nm)
                shutil.copymode(
                    it['path'],
                    "/NFSROOT/class/class_shares/" +
                    nm)
                tos = tos + "mount --bind \"" + \
                    it['path'] + "\" \"/NFSROOT/class/class_shares/" + nm + "\"" + ";\n"
                tos = tos + "mount -o remount," + \
                    it['righ'] + ",bind \"" + it['path'] + "\" \"/NFSROOT/class/class_shares/" + nm + "\"" + ";\n"
            else:
                tos = tos + "mount --bind \"" + \
                    it['path'] + "\" \"/NFSROOT/class/class_shares/" + nm + "\"" + ";\n"
                tos = tos + "mount -o remount," + \
                    it['righ'] + ",bind \"" + it['path'] + "\" \"/NFSROOT/class/class_shares/" + nm + "\"" + ";\n"
        tos = tos + "exit 0;\n"
        fl = open("./tmpba/mntGen.sh", "w")
        fl.write(tos)
        fl.close()
        os.chmod("./tmpba/mntGen.sh", 0o755)
        # umount
        tos = "#!/bin/bash\n"
        for it in lst:
            nm = it['path'].split("/")[-1]
            tos = tos + "umount -l \"/NFSROOT/class/class_shares/" + \
                nm + "\"" + ";\n"
            if os.path.isdir("/NFSROOT/class/class_shares/" + nm):
                tos = tos + "rmdir \"/NFSROOT/class/class_shares/" + \
                    nm + "\";\n"
        tos = tos + "exit 0;\n"
        fl = open("./tmpba/untGen.sh", "w")
        fl.write(tos)
        fl.close()
        os.chmod("./tmpba/untGen.sh", 0o755)

    def addShRc(self):
        """ Přidá odkaz na skript sdílející složky do rc.local hostovské stanice
        \param self Ukazatel na objekt
        """
        with open("/etc/rc.local", 'r') as cont:
            cnl = cont.read()
        obs = ""
        for line in cnl.split("\n"):
            if "/opt/gnuClassConf/tmpba/mntGen.sh;" in line:
                return
            if "exit 0" == line:
                break
            obs = obs + line + "\n"
        obs = obs + "/opt/gnuClassConf/tmpba/mntGen.sh;\n"
        obs = obs + "exit 0\n"
        tar = open("/etc/rc.local", 'w')
        tar.write(obs)
        tar.close()

    def expShrs(self):
        """ Nasdílí složky z ./tmpba/mntGen.sh
        \param self Ukazatel na objekt
        """
        for line in self.sy.runProcess("./tmpba/mntGen.sh"):
            print line,
            self.log.write(line)

    def intrCli(self):
        """ Připraví klienta pro práci se sdílením
        \param self Ukazatel na objekt
        """
        # vytvoří složku sdílení pokud neexistuje
        if not os.path.isdir("/NFSROOT/class/class_shares"):
            os.makedirs("/NFSROOT/class/class_shares")
            os.chmod("/NFSROOT/class/class_shares", 0o755)
        # zkopíruje dávku přidávající odkaz na složku sdílení na plochu
        self.sy.removeFl("/NFSROOT/class/addons/mkLnk.sh")
        self.sy.copyLargeFile(
            "./data/mkLnk.sh",
            "/NFSROOT/class/addons/mkLnk.sh")
        os.chmod("/NFSROOT/class/addons/mkLnk.sh", 0o755)
        # přidá na ní odkaz do rc.local
        with open("/NFSROOT/class/etc/rc.local", 'r') as cont:
            cnl = cont.read()
        obs = ""
        for line in cnl.split("\n"):
            if "/addons/mkLnk.sh;" in line:
                return
            if "exit 0" == line:
                break
            obs = obs + line + "\n"
        obs = obs + "/addons/mkLnk.sh;\n"
        obs = obs + "exit 0\n"
        tar = open("/NFSROOT/class/etc/rc.local", 'w')
        tar.write(obs)
        tar.close()
if __name__ == "__main__":
    # Parser argumentů a parametrů
    parser = OptionParser(
        usage="usage: %prog [args]\n Serve for setting up shares in client filesystem")
    parser.add_option(
        "-l",
        "--shared-list",
        action="store_true",
        dest="lst",
        default=False,
        help="Give a list of shared files")
    parser.add_option(
        "-s",
        "--share-new",
        action="store",
        type="string",
        dest="nfo",
        default="",
        help="Share new folder")
    parser.add_option(
        "-u",
        "--unshare-folder",
        action="store",
        type="string",
        dest="ufo",
        default="",
        help="Unshare folder")
    # Argumenty a parametry z parseru
    (args, opts) = parser.parse_args()
    # Instance objektu
    sh = ShrFol()
    if args.lst:
        for i in sh.shList():
            print i
    if args.nfo != "":
        if os.path.isdir(args.nfo) and args.nfo != "/":
            sh.addToList(args.nfo)
            sh.genListSh()
            sh.expShrs()
    if args.ufo != "":
        sh.remFrList(args.ufo)
        sh.uMntLst(args.ufo)
        sh.genListSh()
