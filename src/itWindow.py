#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file mnWindow.py
# \brief Hlavní okno aplikace
from Tkinter import *
import ttk
import subprocess
import multiprocessing
from Queue import Empty, Full
from iTaHand import iTaHand
from ConsSys import ConsSys
import os
from UError import UError
from DhcpCheck import DhcpCheck

if __name__ == "__main__":
    class App:

        """ \brief Třída obsahující metody s prací s oknem
        Okénko obsluhující instalaci a přípravu iTalc
        """

        def __init__(self, r, qi, qo):
            """ Konstruktor třídy okna
            \param self Ukazatel na objekt
            \param r Ukazatel na Tkinker okno
            \param qi Vstupní fronta
            \param qo Výstupní fronta
            """
            # Ukazatel na okno Tk
            self.root = r
            # Ukazatel na iTalc třídu
            self.it = iTaHand()
            self.root.title("iTalc nastavení")
            self.root.geometry(("%dx%d") % (200, 200))
            self.root.wm_iconbitmap('@./gnusk.xbm')
            self.root.protocol("WM_DELETE_WINDOW", self.qquit)
            self.root.resizable(0, 0)
            # Vstupní fronta
            self.qi = qi
            # Výstupní fronta
            self.qo = qo

        def paintLayout(self):
            """ Metoda vykreslující grafické prvky okna
            Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
            \param self Ukazatel na objekt
            """
            group = LabelFrame(
                self.root,
                text="iTalc nastavení",
                padx=5,
                pady=5)
            group.pack(padx=10, pady=10)
            # Label hláška pro uživatele
            self.vd = StringVar()
            ni = True
            if self.it.tstItalc():
                # Label oznamující uživateli stav
                self.ld = Label(
                    group,
                    textvariable=self.vd,
                    relief=RAISED,
                    bg="green",
                    font="Verdana 10 bold")
                self.vd.set(" iTalc je v systému ")
            else:
                self.ld = Label(
                    group,
                    textvariable=self.vd,
                    relief=RAISED,
                    bg="red",
                    font="Verdana 10 bold")
                self.vd.set(" iTalc není v systému ")
            if not os.path.isdir("/NFSROOT/class"):
                ni = False
            self.ld.pack()
            if self.it.tstItalc():
                # Install/run buttonek
                self.bti = Button(
                    self.root,
                    height=1,
                    width=19,
                    text="Spustit",
                    command=self.iTl)
                self.bti.pack()
            else:
                self.bti = Button(
                    group,
                    height=1,
                    width=19,
                    text="Instalovat",
                    command=self.ins)
                self.bti.pack()
            tx = StringVar()
            if not ni:
                tx.set(
                    "Zdá se, že chybí nejen \n iTalc. Spustě nejdřív \n \"Základní nastavení učebny\".")
            else:
                tx.set(
                    "Zdá se, že je základní \n systém nainstalován. \n Zkuste spustit instalaci \n pomocí tlačítka \"Instalovat\"")
            en = Label(self.root, textvariable=tx, font="Verdana 10").pack()
            self.mvBar(qo)

        def mvBar(self, qc):
            """ Metoda pro vypisování obsahu výstupní fronty
            \param self Ukazatel na objekt
            \param qc Výstupní fronta pro výpis do listu
            """
            try:
                st = qc.get(0)
                if st == "DONE":
                    self.vd.set(" iTalc je v systému ")
                    self.bti.config(state='disabled')
                    self.ld.config(bg="green")
                    Button(
                        self.root,
                        height=1,
                        width=19,
                        text="Spustit",
                        command=self.iTl).pack()
                elif st == "ERROR":
                    self.vd.set(
                        "Nastala chyba\npři instalaci\nzkontrolujte\n připojení!")
                    self.bti.config(state='normal')
            except Empty:
                pass
            finally:
                self.root.after(100, self.mvBar, qc)

        def ins(self):
            """ Metoda instalující iTalc
            Instaluje službu, nastaví klienta, připraví klíče a nakopíruje je do klientských stanic
            \param self Ukazatel na objekt
            """
            self.vd.set("Instaluji, vyčkejte!")
            self.bti.config(state='disabled')
            self.qi.put("INS")

        def iTl(self):
            """ Metoda spouštějící iTalc
            \param self Ukazatel na objekt
            """
            subprocess.Popen("italc", shell=True)

        def qquit(self):
            """ Metoda pro ukončení okna
            \param self Ukazatel na objekt
            """
            self.qi.put("XXX")
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
            elif stri == "INS":
                it = iTaHand()
                try:
                    # instalace
                    it.instServ()
                    it.instClie()
                    it.genKeys()
                    it.setCliSc()
                    # přidání klientů
                    dhc = DhcpCheck()
                    n = dhc.chcNew()
                    if n is not None:
                        for i in n:
                            if it.tstItalc():
                                if it.isInTab(i) is False:
                                    it.addCli(i, dhc.getMacByIpDh(i))
                    # spuštění
                    it.runIca()
                except UError as e:
                    print(str(e.args) + " ERROR!")
                    qo.put("ERROR")
                else:
                    qo.put("DONE")
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
    t.join()
