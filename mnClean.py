#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file mnClean.py
## \brief Okénko čištění systému
from Tkinter import *
import ttk
from ConsSys import ConsSys
from inFocus import inFocus
from clImaOs import clImaOs
import multiprocessing
from Queue import Empty, Full

if __name__ == "__main__":
	class App:
		""" \brief Třída obsahující metody s prací s oknem
		Hlavní okno aplikace, slouží jako rozcestník
		"""
		def __init__(self,r,qi,qo):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na Tkinker okno
			\param qi Vstupní fronta
			\param qo Výstupní fronta
			"""
			## Ukazatel na okno Tk
			self.root=r
			self.root.title("Čištění systému")
			self.root.geometry(("%dx%d")%(480,230))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.protocol("WM_DELETE_WINDOW",self.qquit)
			self.root.resizable(0,0)
			## Vstupní fronta
			self.qi=qi
			## Výstupní fronta
			self.qo=qo
		def erase(self):
			""" Smaže systém - resp zašle signál vláknu, aby smazal systém
			\param self Ukazatel na objekt
			"""
			self.qi.put("ERASE")
		def clear(self):
			""" Vyčistí systém - resp zašle signál vláknu, aby vyčistil systém
			\param self Ukazatel na objekt
			"""
			self.qi.put("CLEAR")
		def update(self):
			""" Aktualizuje systém - resp zašle signál vláknu, aby aktualizoval systém
			\param self Ukazatel na objekt
			"""
			self.qi.put("UPDATE")
		def paintLayout(self):
			""" Metoda vykreslující grafické prvky okna
			Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
			\param self Ukazatel na objekt
			"""
			 # Správa
			gpMan = LabelFrame(self.root, text="Oprava třídy", padx=5, pady=5)
			gpMan.place(relx=0.01, rely=0)
			Button(gpMan,height=1, width=21,text="Vyčistit balíčky obrazu",command=self.clear).pack()
			Button(gpMan,height=1, width=21,text="Smazat obraz učebny",command=self.erase).pack()
			Button(gpMan,height=1, width=21,text="Aktualizovat třídu",command=self.update).pack()
			# Výpisky
			gpTh = LabelFrame(self.root, text="Průběh", padx=5, pady=5)
			gpTh.place(relx=0.48, rely=0.0)
			scrollbar = Scrollbar(self.root)
			## List pro výpisy
			self.to = Listbox(gpTh,height=13, width=27, bd=0, yscrollcommand=scrollbar.set)
			self.to.pack()
			"""
			VYPSAT VELIKOST OBRAZU a PLNOST DISKU
			"""
			self.to.insert('end', "Zatím nic...")
			scrollbar.pack(side=RIGHT, fill=Y)
			scrollbar.config(command=self.to.yview)
			self.mvBar(qo)
		def mvBar(self,qc):
			""" Metoda pro vypisování obsahu výstupní fronty
			\param self Ukazatel na objekt
			\param qc Výstupní fronta pro výpis do listu
			"""
			try:
				st=qc.get(0)
				self.to.insert('end',st)
				self.to.select_clear(self.to.size()-2)
				self.to.yview(END)	
			except Empty:
				pass
			finally:
				self.root.after(100,self.mvBar,qc)
		def qquit(self):
			""" Metoda pro ukončení okna
			Je nutné vypnout vlákno, které vykonává příkazy na pozadí okna
			\param self Ukazatel na objekt
			"""
			self.qi.put("XXX")
			self.root.destroy()
	def genOut(qi,qo):
		""" Funkce vlákna
		\param qi Vstupní fronta
		\param qo Vstupní fronta
		"""
		while True:
			f=inFocus()
			stri=qi.get(True)
			if stri == "XXX":
				break
			elif stri == "ERASE":
				qo.put("Mažu obraz")
				sy=ConsSys()
				sy.erAll()
				qo.put("Smazáno")
			elif stri == "CLEAR":
				qo.put("Zkouším vyčistit systém")
				f=inFocus()
				f.dpkgConfA()
				c=clImaOs()
				c.cleanImage()
				c.cleanSystem()
				qo.put("Vyčištěno")
			elif stri == "UPDATE":
				qo.put("Aktualizuji")
				sy=ConsSys()
				sy.updateImg()
				sy.updateSys()
				qo.put("Aktualizováno")
	## Vstupní fronta pracovního vlákna
	qi = multiprocessing.Queue()
	qi.cancel_join_thread()
	## Výstupní fronta pracovního vlákna
	qo = multiprocessing.Queue()
	qo.cancel_join_thread()
	## Vlákno procesu pro vykonávání příkazů
	t=multiprocessing.Process(target=genOut,args=(qi,qo,))
	t.start()
	## Hlavní okno
	win = Tk()
	## Vlastní instance okna
	pp = App(win,qi,qo)
	pp.paintLayout()
	win.mainloop()
	t.join()