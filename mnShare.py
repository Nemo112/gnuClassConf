#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file mnShare.py
## \brief Okno pro vytváření sdílení

from Tkinter import *
from ShrFol import ShrFol
import tkMessageBox
import tkFileDialog
import os

if __name__ == "__main__":
	class App:
		""" \brief Třída obsahující metody s prací s oknem
		Okno pro vytváření a spravování sdílení s klienty
		"""
		def __init__(self,r):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na Tkinker okno
			"""
			## Objekt sdílení
			self.shr=ShrFol()
			## Ukazatel na okno Tk
			self.root=r
			self.root.title("Sdílení")
			self.root.geometry(("%dx%d")%(236,320))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.protocol("WM_DELETE_WINDOW",self.qquit)
			self.root.resizable(0,0)
			# test, jestli je v rc.local odkaz na sdílení
			g=False
			fl=open("/etc/rc.local","r")
			cn=fl.read()
			fl.close()
			for l in cn.split("\n"):
				if l == "/opt/gnuClassConf/tmpba/mntGen.sh;":
					g=True
			if g == False:
				self.shr.addShRc()
			# přidá do rc.local
		def getNewDir(self):
			""" Metoda pro výběr složky pro sdílení
			\param self Ukazatel na objekt
			"""
			home=os.path.expanduser("~")
			dirname = tkFileDialog.askdirectory(parent=self.root,initialdir=home,title='Vyberte složku pro sdílení')
			if dirname == "/":
				return
			self.shr.addToList(dirname)
			self.shr.genListSh()
			self.shr.expShrs()
			self.loadItems()
		def paintLayout(self):
			""" Metoda vykreslující grafické prvky okna
			Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
			\param self Ukazatel na objekt
			"""
			# přidání sdílené složky
			Button(self.root,height=1, width=24,text="Přidat složku k sdílení",command=self.getNewDir).place(relx=0.02, rely=0.04)
			# sdílené složky
			gpTh = LabelFrame(self.root, text="Sdílené složky", padx=5, pady=5)
			gpTh.place(relx=0.03, rely=0.16)
			Label(gpTh,height=1, width=24,text="Klepnutím složku odeberete").pack()
			scrollbar = Scrollbar(gpTh)
			## Listbox ovladatelný z ostatních metod
			self.to = Listbox(gpTh,height=14, width=24, bd=0, yscrollcommand=scrollbar.set)
			self.to.bind('<<ListboxSelect>>', self.onSelect)
			self.to.pack(side=LEFT)
			ls=self.shr.shList()
			for it in ls:
				self.to.insert('end',it)
			scrollbar.pack(side=RIGHT, fill=Y)
			scrollbar.config(command=self.to.yview)
		def onSelect(self,evt):
			""" Metoda pro odebrání položky z listu sdílení
			\param self Ukazatel na objekt
			\param evt Ukazatel na widget a jeho reakci na klik
			"""
			w = evt.widget
			try:
				index = int(w.curselection()[0])
			except:
				return
			value = w.get(index)
			value=value.encode('utf-8') 
			result = tkMessageBox.askquestion("Odebrání", "Odebrat sdílení " + value + "?", icon='question')
			if result == "yes":
				self.shr.remFrList(value)
				self.shr.uMntLst(value)
				self.shr.genListSh()
				self.loadItems()
		def loadItems(self):
			""" Metoda pro generování listu sdílení
			\param self Ukazatel na objekt
			"""
			self.to.delete(0, END)
			ls=self.shr.shList()
			for it in ls:
				self.to.insert('end',it)
		def qquit(self):
			""" Metoda pro ukončení okna
			Je nutné vypnout vlákno, které vykonává příkazy na pozadí okna
			\param self Ukazatel na objekt
			"""
			self.root.destroy()
	## Hlavní instance okna
	win = Tk()
	## Vlastní instance objektu pro práci s oknem
	pp = App(win)
	pp.paintLayout()
	win.mainloop()