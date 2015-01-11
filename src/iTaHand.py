#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file iTaHand.py
# \brief Třída zajišťuje instalaci a spuštění služby iTalc v systému
import os
from ConsSys import ConsSys
import subprocess
import socket
from UError import UError


class iTaHand:

    """
    \brief Třída zajišťuje instalaci a spuštění služby iTalc v systému
    """

    def __init__(self):
        """ Konstruktor třídy iTalcu
        \param self Ukazatel na objekt
        """
        # Domácí složka
        self.home = os.path.expanduser("~")
        # Instance systémové třídy pro práci se systémem
        self.sy = ConsSys()

    def instServ(self):
        """ Metoda pro instalaci iTalcu na serveru
        \param self Ukazatel na objekt
        """
        #subprocess.Popen("./instItalcMa.sh", shell=True)
        for line in self.sy.runProcess("./instItalcMa.sh"):
            print line,
        self.sy.makeDir(self.home + "/.italc/")
        self.sy.removeFl(self.home + "/.italc/globalconfig.xml")
        self.sy.copyLargeFile(
            "./data/emptyConfITa",
            self.home +
            "/.italc/globalconfig.xml")

    def instClie(self):
        """ Metoda pro instalaci iTalcu na klientu
        \param self Ukazatel na objekt
        """
        self.sy.removeFl("/NFSROOT/class/addons/installIta.sh")
        tar = open("/NFSROOT/class/addons/installIta.sh", 'a')
        tar.write("#!/bin/bash\n")
        tar.write("export LC_ALL=C\n")
        tar.write("apt-get install --allow-unauthenticated italc-client -y\n")
        tar.close()
        os.chmod("/NFSROOT/class/addons/installIta.sh", 0o755)
        tos = 'chroot /NFSROOT/class /bin/bash -c ./addons/installIta.sh'
        for line in self.sy.runProcess(tos):
            print line,

    def setUpIcaS(self):
        """ Nastavení ICA jako služby při startu
        \param self Ukazatel na objekt
        """
        # úprava obrazového rc.local
        with open("/NFSROOT/class/etc/rc.local", 'r') as cont:
            cnl = cont.read()
        obs = ""
        for line in cnl.split("\n"):
            if "/usr/bin/ica &" in line:
                return
            if "exit 0" == line:
                break
            obs = obs + line + "\n"
        obs = obs + "/usr/bin/ica &\n"
        obs = obs + "exit 0\n"
        tar = open("/NFSROOT/class/etc/rc.local", 'w')
        tar.write(obs)
        tar.close()
        # úprava icastart pro xfce, aby se ica zapl po startu
        self.sy.copyLargeFile(
            "./data/stIca.sh",
            "/NFSROOT/class/addons/stIca.sh")
        os.chmod("/NFSROOT/class/addons/stIca.sh", 0o755)
        self.sy.removeFl(
            "/NFSROOT/class/home/student/.config/autostart/icastart.desktop")
        tar = open(
            "/NFSROOT/class/home/student/.config/autostart/icastart.desktop",
            'a')
        tar.write("[Desktop Entry]\n")
        tar.write("Type=Application\n")
        tar.write("Name=My Script]\n")
        tar.write("Exec=/addons/stIca.sh\n")
        tar.write("Icon=system-run\n")
        tar.write("X-GNOME-Autostart-enabled=true\n")
        tar.close()
        os.chmod(
            "/NFSROOT/class/home/student/.config/autostart/icastart.desktop",
            0o777)
        # úprava lokálního rc.local
        """
		with open("/etc/rc.local",'r') as cont:
			cnl=cont.read()
		obs=""
		for line in cnl.split("\n"):
			if "/usr/bin/ica &" in line:
				return
			if "exit 0" == line:
				break
			obs = obs + line  + "\n"
		obs = obs + "/usr/bin/ica &\n"
		obs = obs + "exit 0\n"
		tar = open ("/etc/rc.local", 'w')
		tar.write(obs)
		tar.close()
		"""

    def runIca(self):
        """ Spouští ica jako službu
        \param self Ukazatel na objekt
        """
        # test obsahu služby iTalc
        if os.path.isfile("/usr/bin/ica"):
            isIca = False
            p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
            out, err = p.communicate()
            for line in out.splitlines():
                if 'ica' in line:
                    isIca = True
            if not isIca:
                subprocess.Popen("/usr/bin/ica", shell=True)

    def isIdInTab(self, id):
        """ Otestuje id zdali je v tabulce iTalcu
        \param self Ukazatel na objekt
        \param id String obsahující id v tabulce
        """
        if os.path.isfile(self.home + "/.italc/globalconfig.xml") is False:
            return False
        fl = open(self.home + "/.italc/globalconfig.xml", "r").read()
        for ln in fl.split("\n"):
            if id in ln:
                return True
        return False

    def idCli(self, ip):
        """ Vrací id klienta, které je šesti místné číslo takové, které nikdo v tabulce nemá
        \param self Ukazatel na objekt
        \param ip String obsahující ip adresu klienta
        \return Int s šesti ciframa
        """
        i = 0
        sip = ip.replace(".", "")
        ts = sip[-6:]
        while self.isIdInTab(ts):
            ts = str(int(ts) + 1)
        return ts

    def nameCli(self, ip):
        """ Vrací jméno do tabulky podle ip v podobě "student" + poslední oktet ip
        \param self Ukazatel na objekt
        \param ip String obsahující ip adresu klienta
        \return String obsahující hostname, jméno do tabulky
        """
        return "student" + ip.split(".")[3]

    def addCli(self, ip, mac):
        """ Přidá klienta do tabulky iTalcu
        \param self Ukazatel na objekt
        \param ip String obsahující ip adresu klienta
        \param mac String obsahující mac adresu klienta
        """
        # přidání do italc
        if ip is None or mac is None:
            return False
        if os.path.isfile(self.home + "/.italc/globalconfig.xml") is False:
            return False
        if self.isInTab(ip):
            return False
        fl = open(self.home + "/.italc/globalconfig.xml", "r")
        fg = fl.read()
        fl.close()
        # Test, zdali je konfig uplně prazdný
        for line in fg.split("\n"):
            if "<classroom name=\"ducks\"/>" in line:
                print "yep"
                self.sy.removeFl(self.home + "/.italc/globalconfig.xml")
                self.sy.copyLargeFile(
                    "./data/emptyConfITa",
                    self.home +
                    "/.italc/globalconfig.xml")
                break
        # Přidání IP
        fl = open(self.home + "/.italc/globalconfig.xml", "r")
        fg = fl.read()
        fl.close()
        twr = ""
        for ln in fg.split("\n"):
            if "<classroom name=\"ducks\">" in ln:
                twr = twr + ln + "\n<client hostname=\"" + ip + "\" mac=\"" + mac + \
                    "\" type=\"0\" id=\"" + self.idCli(ip) + "\" name=\"" + self.nameCli(ip) + "\"/> \n"
            else:
                twr = twr + ln + "\n"
        wr = open(self.home + "/.italc/globalconfig.xml", "w")
        wr.write(twr)
        wr.close()
        # přidání do /etc/hosts
        f = open("/etc/hosts", "r")
        o = f.read()
        f.close()
        for i in o.split("\n"):
            if len(i.split()) > 0:
                if i.split()[0] == ip:
                    return True
        f = open("/etc/hosts", "a")
        f.write("\n" + ip + " " + self.nameCli(ip))
        f.close()
        return True

    def tesCliITlc(self, ip):
        """ Otestuje IP klienta, zdali je na ní iTalc (podle portu iTalc služby)
        \param self Ukazatel na objekt
        \param ip String obsahující ip adresu klienta
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, 5800))
            t.connect((ip, 5900))
            s.shutdown(1)
            t.shutdown(1)
            return True
        except:
            return False

    def remCli(self, ip):
        """ Odebere podle IP klienta z tabulky iTalcu
        \param self Ukazatel na objekt
        \param ip String obsahující ip adresu klienta
        """
        if os.path.isfile(self.home + "/.italc/globalconfig.xml") is False:
            return False
        twr = ""
        fl = open(self.home + "/.italc/globalconfig.xml", "r")
        fg = fl.read()
        for ln in fg.split("\n"):
            if ip not in ln:
                twr = twr + ln + "\n"
        wr = open(self.home + "/.italc/globalconfig.xml", "w")
        wr.write(twr)
        wr.close()
        return True

    def isInTab(self, ip):
        """ Otestuje IP zdali je v tabulce iTalcu
        \param self Ukazatel na objekt
        \param ip String obsahující ip adresu klienta
        """
        if os.path.isfile(self.home + "/.italc/globalconfig.xml") is False:
            return False
        fl = open(self.home + "/.italc/globalconfig.xml", "r").read()
        for ln in fl.split("\n"):
            if ip in ln:
                return True
        return False

    def genKeys(self):
        """ Metoda pro generování klíčů
        \param self Ukazatel na objekt
        """
        try:
            for line in self.sy.runProcess("addgroup italc"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess("adduser italc"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess("usermod -a -G italc ucitel"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess("usermod -a -G italc root"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess("ica -role teacher -createkeypair"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess("chgrp -R italc /etc/italc/keys"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess(
                    "chmod -R 640 /etc/italc/keys/private"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess(
                    "chmod -R ug+x /etc/italc/keys/private"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess("mkdir /NFSROOT/class/etc/italc"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess(
                    "mkdir /NFSROOT/class/etc/italc/keys"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess(
                    "cp -r /etc/italc/keys/public /NFSROOT/class/etc/italc/keys"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        try:
            for line in self.sy.runProcess(
                    "chmod 444 " +
                    self.home +
                    "/.italc/globalconfig.xml"):
                print line,
        except UError as e:
            print(str(e.args) + " ERROR!")
        self.setUpIcaS()

    def setCliSc(self):
        """ Metoda pro generování skriptu na klientu
        \param self Ukazatel na objekt
        """
        self.sy.removeFl("/NFSROOT/class/etc/rcS.d/S20-ica-launcher")
        tar = open("/NFSROOT/class/etc/rcS.d/S20-ica-launcher", 'a')
        tar.write("#!/bin/sh\n")
        tar.write("/usr/bin/ica &\n")
        tar.write("true\n")
        tar.close()
        os.chmod("/NFSROOT/class/etc/rcS.d/S20-ica-launcher", 0o757)

    def staWin(self):
        """ Metoda pro spuštění okna iTalcu
        \param self Ukazatel na objekt
        """
        subprocess.Popen("/usr/bin/italc", shell=True)

    def tstItalc(self):
        """ Metoda pro testování přítomnosti iTalcu v systému
        \param self Ukazatel na objekt
        \return True pokud iTalc je na klientu i serveru
        """
        if os.path.isfile(
                "/usr/bin/italc") and os.path.isfile("/NFSROOT/class/usr/bin/ica"):
            return True
        else:
            return False
if __name__ == "__main__":
    print("Jen pro import")
    # it=iTaHand()
    # print it.isInTab("192.168.111.12")
    # it.instServ()
    # it.addCli("192.168.111.14","FF:FF:FF:FF:FF:FF")
    # print it.idCli("192.168.111.14")
    # print it.nameCli("192.168.111.12")
    # print it.tesCliITlc("192.168.111.12")
