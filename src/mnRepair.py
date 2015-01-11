#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file mnClean.py
# \brief Okénko opravování připojení
from Tkinter import *
import ttk
from SysLoad import SysLoad
import multiprocessing
from Queue import Empty, Full
from ConsSys import ConsSys
from ConfSys import ConfSys
from ParConfFl import ParConfFl
from inFocus import inFocus
from xmlFocPar import xmlFocPar
from iTaHand import iTaHand
from ShrFol import ShrFol
import os
from UError import UError

if __name__ == "__main__":
    class App:

        """ \brief Třída obsahující metody s prací s oknem
        Hlavní okno aplikace, slouží jako rozcestník
        """

        def __init__(self, r, qi, qo):
            """ Konstruktor třídy okna
            \param self Ukazatel na objekt
            \param qi Vstupní fronta
            \param qo Výstupní fronta
            \param r Ukazatel na Tkinker okno
            """
            # Ukazatel na okno Tk
            self.root = r
            self.root.title("Oprava systému")
            self.root.geometry(("%dx%d") % (480, 280))
            self.root.wm_iconbitmap('@./gnusk.xbm')
            self.root.protocol("WM_DELETE_WINDOW", self.qquit)
            self.root.resizable(0, 0)
            # Výstupní fronta
            self.qo = qo
            # Vstupní fronta
            self.qi = qi

        def net(self):
            """Zasílá signál k opravě připojení
            \param self Ukazatel na objekt
            """
            self.qi.put("NET")

        def fat(self):
            """Zasílá signál k opravě fatalní chyby
            \param self Ukazatel na objekt
            """
            self.qi.put("FAT")

        def gra(self):
            """Zasílá signál k opravě grafického prostředí
            \param self Ukazatel na objekt
            """
            self.qi.put("GRA")

        def stu(self):
            """Zasílá signál k opravě přihlašování
            \param self Ukazatel na objekt
            """
            self.qi.put("STU")

        def pac(self):
            """Zasílá signál k opravě balíčků
            \param self Ukazatel na objekt
            """
            self.qi.put("PAC")

        def paintLayout(self):
            """ Metoda vykreslující grafické prvky okna
            Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
            \param self Ukazatel na objekt
            """
            # Správa
            gpMan = LabelFrame(self.root, text="Oprava třídy", padx=5, pady=5)
            gpMan.place(relx=0.01, rely=0)
            """
                        Obnovit maškarádu
                        Vyresetovat net
                        Znova nastavit síťování
                        DHCP obnovit
                        """
            Button(
                gpMan,
                height=1,
                width=21,
                text="Nefunguje internet",
                command=self.net).pack()
            """
                        Pročistit
                        """
            Button(
                gpMan,
                height=1,
                width=21,
                text="Balíčky se neinstalují",
                command=self.pac).pack()
            """
                        Udělat studenta
                        """
            Button(
                gpMan,
                height=1,
                width=21,
                text="Student se nemůže přihlásit",
                command=self.stu).pack()
            """
                        installXFCE a lightDm
                        """
            Button(
                gpMan,
                height=1,
                width=21,
                text="Nefunguje grafické prostředí",
                command=self.gra).pack()
            """
                        Odkázat na začátek a přemazat celou třídu
                        """
            Button(
                gpMan,
                height=1,
                width=21,
                text="Stanice hlásí fatální chybu",
                command=self.fat).pack()
            # Výpisky
            gpTh = LabelFrame(self.root, text="Průběh", padx=5, pady=5)
            gpTh.place(relx=0.48, rely=0.0)
            scrollbar = Scrollbar(self.root)
            # List pro výpisy
            self.to = Listbox(
                gpTh,
                height=13,
                width=27,
                bd=0,
                yscrollcommand=scrollbar.set)
            self.to.pack()
            self.to.insert('end', "Zatím nic...")
            scrollbar.pack(side=RIGHT, fill=Y)
            scrollbar.config(command=self.to.yview)
            # Progres
            Label(
                self.root,
                height=1,
                width=21,
                text="Průběh opravy:").place(
                relx=0.42,
                rely=0.82)
            # Ukazatel vytížení počítače
            self.progressbar = ttk.Progressbar(
                orient=HORIZONTAL,
                length=200,
                mode='determinate')
            self.progressbar.place(relx=0.5, rely=0.89)
            self.progressbar["value"] = 0
            self.progressbar["maximum"] = 100
            # načítání progressbaru
            # Obsahuje instanci vytížení systému
            self.sl = SysLoad()
            self.loadProgs()
            # Výstupní fronta
            self.qo = qo

        def loadProgs(self):
            """ Metoda pro načítání progressbaru a výpisu stavu aplikace
            \param self Ukazatel na objekt
            """
            try:
                st = self.qo.get(0)
                toSay = st.split(":")[1]
                if st.split(":")[0]:
                    self.progressbar["value"] = int(st.split(":")[0])
                self.to.insert('end', toSay)
                self.to.select_clear(self.to.size() - 2)
                self.to.yview(END)
            except Empty:
                pass
            finally:
                self.root.after(100, self.loadProgs)

        def qquit(self):
            """ Metoda pro ukončení okna
            Je nutné vypnout vlákno, které vykonává příkazy na pozadí okna
            \param self Ukazatel na objekt
            """
            qi.put("XXX")
            self.root.destroy()

    def genOut(qi, qo):
        """ Funkce vlákna
        \param qi Vstupní fronta
        \param qo Vstupní fronta
        """
        while True:
            stri = qi.get(True)
            if stri == "XXX":
                break
            elif stri == "NET":
                qo.put("2:Testuji konektivitu")
                sysq = ConsSys()
                if sysq.isCnt():
                    qo.put("30:Konektivita přítomna")
                    qo.put("30:Pokud chyba zůstane")
                    qo.put("30:zkuste znovu projít")
                    qo.put("30:\"Základní nastavení učebny\".")
                else:
                    qo.put("30:Konektivita nepřítomna")
                    qo.put("30:Testuji přítomnost brány")
                    cf = ConfSys()
                    co = ParConfFl()
                    inti = co.getInterfaces()
                    if inti['outi'] != cf.getDefGtw():
                        qo.put("50:Vnější rozhraní se")
                        qo.put("50:neshoduje s rozhraním")
                        qo.put("50:zaneseným v aplikaci.")
                        qo.put("60:Zkuste znovu projít")
                        qo.put("60:\"Základní nastavení učebny\"")
                        qo.put("60:a nastavit síť znovu.")
                    else:
                        qo.put("50:Zdá se, že nastavení")
                        qo.put("50:aplikace je v pořádku.")
                        qo.put("50:Zkontrolujte kabel, ")
                        qo.put("50:kontaktujte administrátora,")
                        qo.put("50:a tak dále ...")
                qo.put("100:Končím s opravou")
                qo.put("100:")
            elif stri == "FAT":
                qo.put("0:Testuji obraz stanic")
                if os.path.isdir("/NFSROOT/") is False:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                elif os.path.isdir("/NFSROOT/class") is False:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                elif len(os.listdir("/NFSROOT/class")) < 20:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz. Instalace je ")
                    qo.put("50:možná nedokončená.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                else:
                    qo.put("50:Vše se zdá být v pořádku.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                qo.put("100:Končím s opravou")
                qo.put("100:")
            elif stri == "STU":
                qo.put("0:Testuji přihlašování")
                co = ParConfFl()
                inti = co.getInterfaces()
                setUNt = ConfSys(inti['inti'])
                sy = ConsSys()
                if os.path.isdir("/NFSROOT/") is False:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                elif os.path.isdir("/NFSROOT/class") is False:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                elif len(os.listdir("/NFSROOT/class")) < 20:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz. Instalace je ")
                    qo.put("50:možná nedokončená.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                else:
                    qo.put("50:Zkouším znovu nastavit")
                    qo.put("50:uživatele.")
                    sy.chgPasswd(
                        "/NFSROOT/class/etc/shadow",
                        'root',
                        'teacher')
                    setUNt.createStudent()
                    qo.put("60:Edituji rc.local")
                    setUNt.setUpHsn()
                    setUNt.setUpFw()
                    setUNt.setUpXh()
                    setUNt.installDm()
                    i = iTaHand()
                    i.setUpIcaS()
                    s = ShrFol()
                    s.addShRc()
                    qo.put("80:Provedeno")
                    qo.put("80:Pokud pořád nefunguje,")
                    qo.put("80:zkuste znovu projít")
                    qo.put("90:\"Základní nastavení učebny\".")
                qo.put("100:Končím s opravou")
                qo.put("100:")
            elif stri == "GRA":
                qo.put("0:Testuji grafické prostředí")
                if os.path.isdir("/NFSROOT/") is False:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                elif os.path.isdir("/NFSROOT/class") is False:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                elif len(os.listdir("/NFSROOT/class")) < 20:
                    qo.put("50:Zdá se, že chybí celý")
                    qo.put("50:obraz. Instalace je ")
                    qo.put("50:možná nedokončená.")
                    qo.put("60:Zkuste znovu projít")
                    qo.put("60:\"Základní nastavení učebny\".")
                else:
                    qo.put("50:Zkouším přeinstalovat")
                    qo.put("50:grafické rozhraní.")
                    qo.put("50:Tato operace trvá dlouho.")
                    co = ParConfFl()
                    inti = co.getInterfaces()
                    setUNt = ConfSys(inti['inti'])
                    qo.put("60:Odebírám grafické rozhraní")
                    setUNt.unstallXfce()
                    qo.put("70:Přidávám grafické rozhraní")
                    setUNt.copyXorgCo()
                    # instalace XFCE
                    setUNt.installXfce()
                    # nastavení klávesnice
                    setUNt.setUpKey()
                    # instaluji login screen
                    setUNt.installDm(qo)
                    setUNt.copyXBac()
                    qo.put("80:Provedeno")
                    qo.put("80:Pokud pořád nefunguje,")
                    qo.put("80:zkuste znovu projít")
                    qo.put("90:\"Základní nastavení učebny\".")
                qo.put("100:Končím s opravou")
                qo.put("100:")
            elif stri == "PAC":
                qo.put("0:Testuji balíčkový systém")
                f = inFocus()
                qo.put("10:Čistím pomocí autoremove")
                try:
                        f.aptAutorem()
                except UError as e:
                        qo.put("20:Obraz není nainstalován")
                qo.put("20:Čistím pomocí apt clean")
                try:
                        f.dpkgConfA()
                except UError as e:
                       qo.put("20:Obraz není nainstalován")
                qo.put("20:Pokouším se instalovat")
                qo.put("20:balíčky dle listu")
                qo.put("20:zaměření.")
                qo.put("20:Tato operace trvá dlouho.")
                lst = xmlFocPar()
                nt = lst.getFoc()
                rms = [x for x in range(0, len(nt.items()))]
                idxs = f.getLstInst()
                # print rms
                tr = []
                for i in idxs:
                    k = 0
                    for j in nt.items():
                        if j[0] == i:
                            tr.append(k)
                        k += 1
                # print tr
                qo.put("40:Odstraňuji balíčky")
                try:
                        for i in tr:
                            rms.remove(int(i))
                            f.instXmlCo(lst.getFoc().items()[int(i)][0])
                            for it in lst.getFoc().items()[int(i)][1]['apps'].items():
                                f.exCom(it[1]['comm'])
                        qo.put("70:Instaluji balíčky")
                        for i in rms:
                            f.uniXmlCo(lst.getFoc().items()[int(i)][0])
                            for it in lst.getFoc().items()[int(i)][1]['apps'].items():
                                f.exCom(it[1]['uni'])
                except UError as e:
                        qo.put("80:Obraz není nainstalován")
                qo.put("80:Pokud obraz stále")
                qo.put("80:nefunguje, prosím,")
                qo.put("80:přeinstalujte obraz")
                qo.put("80:pomocí")
                qo.put("80:\"Základní nastavení učebny\".")
                qo.put("100:Končím s opravou")
                qo.put("100:")
    # Vstupní fronta pracovního vlákna
    qi = multiprocessing.Queue()
    qi.cancel_join_thread()
    # Výstupní fronta pracovního vlákna
    qo = multiprocessing.Queue()
    qo.cancel_join_thread()
    # Vlákno procesu pro vykonávání příkazů
    t = multiprocessing.Process(target=genOut, args=(qi, qo,))
    t.start()
    # Hlavní okno
    win = Tk()
    # Vlastní instance okna
    pp = App(win, qi, qo)
    pp.paintLayout()
    win.mainloop()
