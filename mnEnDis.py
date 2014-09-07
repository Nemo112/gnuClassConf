#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file mnEnDis.py
## \brief Oknénko povolení a zakázání přístupů
from Tkinter import *
import ttk
import subprocess
from SysLoad import SysLoad
from iTaHand import iTaHand
import tkMessageBox
from fwSetUp import fwSetUp

if __name__ == "__main__":
	class App:
		""" \brief Třída obsahující metody s prací s oknem
		Hlavní okno aplikace, slouží jako rozcestník
		"""
		def __init__(self,r):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na Tkinker okno
			"""
			## Instance třídy pro úpravy etc hosts a etc resolv conf
			self.fw=fwSetUp()
			## Ukazatel na okno Tk
			self.root=r
			self.root.title("Zákazy a povolení")
			self.root.geometry(("%dx%d")%(450,270))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.protocol("WM_DELETE_WINDOW",self.qquit)
			self.root.resizable(0,0)
		def clSet(self):
			""" Metoda zapínající okno closeSetup.py
			\param self Ukazatel na objekt
			"""
			subprocess.Popen("./closeSetup.py", shell=True)
		def paintLayout(self):
			""" Metoda vykreslující grafické prvky okna
			Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
			\param self Ukazatel na objekt
			"""
			# povolení a zakázání domén
			gpMan = LabelFrame(self.root, text="Zákaz domény", padx=5, pady=5)
			gpMan.place(relx=0.01, rely=0.08)
			Label(gpMan,text="Jméno domény:").grid(padx=4, pady=1)
			## Vstup pro přidání domény k blokování
			self.ew=StringVar()
			en=Entry(gpMan,width=20,textvariable=self.ew)
			en.grid(padx=4, pady=4)
			en.bind("<Return>", self.keyEn)
			Button(gpMan,height=1, width=19,text="Zakázat",command=self.setN).grid(padx=3, pady=3)
			# povolení a zakázání internetu
			gpManI = LabelFrame(self.root, text="Zákaz internetu", padx=15, pady=5)
			gpManI.place(relx=0.01, rely=0.6)
			Label(gpManI,height=1, width=20,text="Stav blokování internetu").pack()
			## Proměnná pro výsledek volby uživatele
			self.v = IntVar()
			if self.fw.isNet() == False:
				self.v.set(1)
			else:
				self.v.set(2)				
			languages = [
				("Povolit",1),
				("Zakázat",2)
			]
			for txt, val in languages:
				Radiobutton(gpManI, text=txt, padx = 20, variable=self.v, value=val,command=self.swBN).pack(anchor=W)
			# blokované domény
			gpTh = LabelFrame(self.root, text="Blokované domény", padx=5, pady=5)
			gpTh.place(relx=0.5, rely=0.0)
			Label(gpTh,height=1, width=24,text="Klepnutím doménu odblokujete").pack()
			scrollbar = Scrollbar(gpTh)
			## Listbox ovladatelný z ostatních metod
			self.to = Listbox(gpTh,height=14, width=24, bd=0, yscrollcommand=scrollbar.set)
			self.to.bind('<<ListboxSelect>>', self.onSelect)
			self.to.pack(side=LEFT)
			self.loadItems()
			scrollbar.pack(side=RIGHT, fill=Y)
			scrollbar.config(command=self.to.yview)
		def loadItems(self):
			""" Metoda pro generování listu v blokování
			\param self Ukazatel na objekt
			"""
			self.to.delete(0, END)
			dc=self.fw.getLstBl()
			for it in dc.items():
				self.to.insert('end',it[1]['hostname'])
		def onSelect(self,evt):
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
			result = tkMessageBox.askquestion("Povolení", "Odblokovat " + value + "?", icon='warning')
			if result == "yes":
				self.to.delete(index)
				self.fw.unDom(value)
				self.loadItems()
		def keyEn(self,evt):
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
	## Hlavní instance okna
	win = Tk()
	## Vlastní instance objektu pro práci s oknem
	pp = App(win)
	pp.paintLayout()
	win.mainloop()