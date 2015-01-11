#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file EnDisDiag.py
# \brief Dialogové okénko volby pro odstranění nebo povolení domény

from Tkinter import *


class EnDisDiag:

    """ \brief Dialogové okénko volby pro odstranění nebo povolení domény
    """

    def __init__(self, win):
        """ Constructor of window
        \param self Pointer on class
        \param win Ukazatel na okno
        """
        # Ukazatel na okno
        self.top = Toplevel(win, height=100, width=20000)
        top = self.top
        # self.root=win
        #self.root.title("Odstranit nebo blokovat")
        self.top.geometry(("%dx%d") % (280, 80))
        # self.root.wm_iconbitmap('@./gnusk.xbm')
        self.top.resizable(0, 0)
        # Rozhodnutí uživatele
        self.des = "Nope"
        self.paintLayout()

    def setDer(self):
        """ Setter rozhodnutí
        \param self Ukazatel na třídu
        """
        self.des = "Errase"
        self.top.destroy()

    def setDeb(self):
        """ Setter rozhodnutí
        \param self Ukazatel na třídu
        """
        self.des = "Block"
        self.top.destroy()

    def setDec(self):
        """ Setter rozhodnutí
        \param self Ukazatel na třídu
        """
        self.des = "Nope"
        self.top.destroy()

    def paintLayout(self):
        """ Method painting main window
        \param self Ukazatel na třídu
        """
        Label(
            self.top,
            height=2,
            text="Má se doména odstranit z \n tabulky nebo blokovat?",
            justify=CENTER).pack()
        Button(
            self.top,
            height=1,
            width=7,
            text="Odstranit",
            command=self.setDer).place(
            relx=0.01,
            rely=0.5)
        Button(
            self.top,
            height=1,
            width=7,
            text="Blokovat",
            command=self.setDeb).place(
            relx=0.34,
            rely=0.5)
        Button(
            self.top,
            height=1,
            width=7,
            text="Nedělat nic",
            command=self.setDec).place(
            relx=0.65,
            rely=0.5)
