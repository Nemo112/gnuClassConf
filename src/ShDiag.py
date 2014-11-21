#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file ShDiag.py
## \brief Dialogové okénko volby pro odstranění, změny stavu sdílení složky

from Tkinter import *

class ShDiag:
	""" \brief Dialogové okénko volby pro odstranění, změny stavu sdílení složky
	"""
	def __init__(self,win,nm,rig):
		""" Constructor of window
		\param self Pointer on class
		\param win Ukazatel na okno
		"""
		## Jméno
		self.nm=nm
		## Práva složky
		self.rig=rig
		## Ukazatel na okno
		self.top = Toplevel(win,height=100,width=20000)
		top = self.top
		#self.root=win
		#self.root.title("Odstranit nebo blokovat")
		self.top.geometry(("%dx%d")%(240,80))
		#self.root.wm_iconbitmap('@./gnusk.xbm')
		self.top.resizable(0,0)
		## Rozhodnutí uživatele
		self.des="Nope"
		self.paintLayout()
	def setDer(self):
		""" Setter rozhodnutí
		\param self Ukazatel na třídu
		"""
		self.des="Re"
		self.top.destroy()
	def setDeb(self):
		""" Setter rozhodnutí
		\param self Ukazatel na třídu
		"""
		self.des="Rw"
		self.top.destroy()
	def setDec(self):
		""" Setter rozhodnutí
		\param self Ukazatel na třídu
		"""
		self.des="Del"
		self.top.destroy()
	def paintLayout(self):
		""" Method painting main window
		\param self Ukazatel na třídu
		"""
		Label(self.top,height=3,text="Má být složka ke čtení i zápisu, \n pouze ke čtení \n nebo jí přestat sdílet?",justify=CENTER).pack()
		if self.rig == "rw":
			Button(self.top,height=1, width=10,text="Čtení",command=self.setDer).place(relx=0.01, rely=0.65)
		elif self.rig == "ro":
			Button(self.top,height=1, width=10,text="Čtení i zápis",command=self.setDeb).place(relx=0.01, rely=0.65)
		Button(self.top,height=1, width=10,text="Přestat sdílet",command=self.setDec).place(relx=0.55, rely=0.65)