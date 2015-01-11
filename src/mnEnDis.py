#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file mnEnDis.py
# \brief Oknénko povolení a zakázání přístupů
from Tkinter import *
import ttk
import subprocess
from SysLoad import SysLoad
from iTaHand import iTaHand
import tkMessageBox
import re
from fwSetUp import fwSetUp
from EnDisDiag import EnDisDiag

if __name__ == "__main__":
    class App:

        """ \brief Třída obsahující metody s prací s oknem
        Hlavní okno aplikace, slouží jako rozcestník
        """

        def __init__(self, r):
            """ Konstruktor třídy okna
            \param self Ukazatel na objekt
            \param r Ukazatel na Tkinker okno
            """
            # Instance třídy pro úpravy etc hosts a etc resolv conf
            self.fw = fwSetUp()
            # Ukazatel na okno Tk
            self.root = r
            self.root.title("Zákazy a povolení")
            self.root.geometry(("%dx%d") % (450, 310))
            self.root.wm_iconbitmap('@./gnusk.xbm')
            self.root.protocol("WM_DELETE_WINDOW", self.qquit)
            self.root.resizable(0, 0)

        def keySe(self, evt):
            """ Metoda reagující na vyhledávání v entry boxu
            \param self Ukazatel na objekt
            \param evt Event, který se ale nepoužije
            """
            if self.ens.get() == "":
                return
            self.listRes(self.ens.get())

        def listRes(self, reg="*"):
            """Metoda pro třídění pole domén podle regulárního výrazu
            \param self Ukazatel na třídu
            \param reg Regulární výraz pro vyhledáváné
            """
            self.to.delete(0, END)
            # list domén
            ls = self.fw.getLstBl()
            for i in ls:
                try:
                    m = re.search(reg, ls[i]['hostname'], re.IGNORECASE)
                except:
                    m = "A"
                if m is not None:
                    self.to.insert('end', ls[i]['hostname'])
                    # zabarvení položek blokování
                    if ls[i]['blocking']:
                        self.to.itemconfig(END, {'bg': 'orange red'})
                    else:
                        self.to.itemconfig(END, {'bg': 'dark sea green'})

        def paintLayout(self):
            """ Metoda vykreslující grafické prvky okna
            Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
            \param self Ukazatel na objekt
            """
            # entry pro vyhledávání
            Label(self.root, text="Hledat: ").place(relx=0.02, rely=0.07)
            # String obsahující regulární výraz pro hledání
            self.ens = StringVar()
            self.ens.set("*")
            ens = Entry(self.root, width=17, textvariable=self.ens)
            ens.bind("<KeyPress>", self.keySe)
            ens.place(relx=0.14, rely=0.07)
            # povolení a zakázání domén
            gpMan = LabelFrame(self.root, text="Zákaz domény", padx=5, pady=5)
            gpMan.place(relx=0.01, rely=0.17)
            Label(gpMan, text="Jméno domény:").grid(padx=4, pady=1)
            # Vstup pro přidání domény k blokování
            self.ew = StringVar()
            en = Entry(gpMan, width=20, textvariable=self.ew)
            en.grid(padx=4, pady=4)
            en.bind("<Return>", self.keyEn)
            Button(
                gpMan,
                height=1,
                width=19,
                text="Zakázat",
                command=self.setN).grid(
                padx=3,
                pady=3)
            # povolení a zakázání internetu
            gpManI = LabelFrame(
                self.root,
                text="Zákaz internetu",
                padx=15,
                pady=5)
            gpManI.place(relx=0.01, rely=0.57)
            Label(
                gpManI,
                height=1,
                width=20,
                text="Stav blokování internetu").pack()
            # Proměnná pro výsledek volby uživatele
            self.v = IntVar()
            if self.fw.isNet() is False:
                self.v.set(1)
            else:
                self.v.set(2)
            languages = [
                ("Povolit", 1),
                ("Zakázat", 2)
            ]
            for txt, val in languages:
                Radiobutton(
                    gpManI,
                    text=txt,
                    padx=20,
                    variable=self.v,
                    value=val,
                    command=self.swBN).pack(
                    anchor=W)
            # blokované domény
            gpTh = LabelFrame(
                self.root,
                text="Blokované domény",
                padx=5,
                pady=5)
            gpTh.place(relx=0.5, rely=0.0)
            Label(
                gpTh,
                height=1,
                width=24,
                text="Klepnutím doménu odblokujete").pack()
            scrollbar = Scrollbar(gpTh)
            # Listbox ovladatelný z ostatních metod
            self.to = Listbox(
                gpTh,
                height=14,
                width=24,
                bd=0,
                yscrollcommand=scrollbar.set)
            self.to.bind('<<ListboxSelect>>', self.onSelect)
            self.to.pack(side=LEFT)
            self.loadItems()
            # Label oznamující funkci barev
            Label(
                self.root,
                text="Červená barva označuje domény, které jsou blokovány.\nZelené jsou připraveny pro blokování a uschovány pro použití.").place(
                relx=0.07,
                rely=0.88)
            scrollbar.pack(side=RIGHT, fill=Y)
            scrollbar.config(command=self.to.yview)

        def loadItems(self):
            """ Metoda pro generování listu v blokování
            \param self Ukazatel na objekt
            """
            self.to.delete(0, END)
            dc = self.fw.getLstBl()
            for it in dc.items():
                self.to.insert('end', it[1]['hostname'])
                if it[1]['blocking']:
                    self.to.itemconfig(END, {'bg': 'orange red'})
                else:
                    self.to.itemconfig(END, {'bg': 'dark sea green'})

        def onSelect(self, evt):
            """ Metoda pro odebrání položky z blokovacího okénka
            \param self Ukazatel na objekt
            \param evt Ukazatel na widget a jeho reakci na klik
            """
            w = evt.widget
            try:
                index = int(w.curselection()[0])
            except:
                return
            value = w.get(index)
            ls = self.fw.getLstBl()
            bl = False
            for i in ls:
                if value == ls[i]['hostname']:
                    if ls[i]['blocking']:
                        bl = True
                        break
            if bl:
                result = tkMessageBox.askquestion(
                    "Odblokovat",
                    "Odblokovat " +
                    value.encode("utf-8") +
                    "? \nPoložka zůstane v tabulce pro pozdější použití.",
                    icon='warning')
                if result == "yes":
                    self.to.delete(index)
                    self.fw.relBlDom(value)
                    self.loadItems()
            elif bl is False:
                # Rozhodnutí uživatele
                di = EnDisDiag(self.root)
                self.root.wait_window(di.top)
                result = di.des
                # print di.des
                if result == "Block":
                    self.to.delete(index)
                    self.fw.unDom(value)
                    self.fw.blDom(value)
                    self.loadItems()
                if result == "Errase":
                    self.to.delete(index)
                    self.fw.unDom(value)
                    self.loadItems()

        def keyEn(self, evt):
            """ Metoda pro přidání blokované domény
            \param self Ukazatel na objekt
            \param evt Event, který se ale nepoužije
            """
            if self.ew.get() == "":
                return
            self.fw.blDom(self.ew.get())
            self.loadItems()
            self.ew.set("")

        def setN(self):
            """ Metoda pro přidání blokované domény
            \param self Ukazatel na objekt
            """
            if self.ew.get() == "":
                return
            self.fw.blDom(self.ew.get())
            self.loadItems()
            self.ew.set("")

        def swBN(self):
            """ Metoda pro přepnutí zákazu internetu klientům
            \param self Ukazatel na objekt
            """
            # zákaz
            if self.v.get() == 2:
                self.fw.blNet()
                # povolit
            elif self.v.get() == 1:
                self.fw.unBlNet()

        def qquit(self):
            """ Metoda pro ukončení okna
            Je nutné vypnout vlákno, které vykonává příkazy na pozadí okna
            \param self Ukazatel na objekt
            """
            self.root.destroy()
    # Hlavní instance okna
    win = Tk()
    # Vlastní instance objektu pro práci s oknem
    pp = App(win)
    pp.paintLayout()
    win.mainloop()
