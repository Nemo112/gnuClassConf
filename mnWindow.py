#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file mnWindow.py
## \brief Hlavní okno aplikace
from Tkinter import *
import ttk
import subprocess
from SysLoad import SysLoad
from iTaHand import iTaHand
import tkMessageBox
import os
import time
import multiprocessing
from DhcpCheck import DhcpCheck
from iTaHand import iTaHand
from Queue import Empty, Full
import signal
from LogWrk import LogWrk
from ProcLs import ProcLs

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
			self.root.title("Ovládací menu učebny")
			self.root.geometry(("%dx%d")%(480,284))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.protocol("WM_DELETE_WINDOW",self.qquit)
			self.root.resizable(0,0)
			## Vstupní fronta
			self.qi=qi
			## Výstupní fronta
			self.qo=qo
			## Logovací třída
			self.log=LogWrk()
			## Procesy
			self.pr=ProcLs()
		def stFoc(self):
			""" Metoda zapínající okno mnFocus.py
			\param self Ukazatel na objekt
			"""
			if self.pr.isRnApp("mnFocus.py")==True:
				print "Already running"
			elif os.path.isfile("/NFSROOT/class/etc/hosts") and os.path.isfile("/NFSROOT/class/etc/resolv.conf"):
				subprocess.Popen("./mnFocus.py", shell=True)
			else:
				tkMessageBox.showinfo("Chyba", "Zdá se, že třída ještě není nastavena. Použijte \"Základní nastavení učebny\"")
		def stRep(self):
			""" Metoda zapínající okno mnRepair.py
			\param self Ukazatel na objekt
			"""
			if self.pr.isRnApp("mnRepair.py")==True:
				print "Already running"
			elif os.path.isfile("/NFSROOT/class/etc/hosts") and os.path.isfile("/NFSROOT/class/etc/resolv.conf"):
				subprocess.Popen("./mnRepair.py", shell=True)
			else:
				tkMessageBox.showinfo("Chyba", "Zdá se, že třída ještě není nastavena. Použijte \"Základní nastavení učebny\"")
		def stCle(self):
			""" Metoda zapínající okno mnClean.py
			\param self Ukazatel na objekt
			"""
			if self.pr.isRnApp("mnClean.py")==True:
				print "Already running"
			elif os.path.isfile("/NFSROOT/class/etc/hosts") and os.path.isfile("/NFSROOT/class/etc/resolv.conf"):
				subprocess.Popen("./mnClean.py", shell=True)
			else:
				tkMessageBox.showinfo("Chyba", "Zdá se, že třída ještě není nastavena. Použijte \"Základní nastavení učebny\"")
		def enSh(self):
			""" Metoda zapínající okno mnShare.py
			\param self Ukazatel na objekt
			"""
			if self.pr.isRnApp("mnShare.py")==True:
				print "Already running"
			elif os.path.isfile("/NFSROOT/class/etc/hosts") and os.path.isfile("/NFSROOT/class/etc/resolv.conf"):
				subprocess.Popen("./mnShare.py", shell=True)
			else:
				tkMessageBox.showinfo("Chyba", "Zdá se, že třída ještě není nastavena. Použijte \"Základní nastavení učebny\"")
		def clSet(self):
			""" Metoda zapínající okno closeSetup.py
			\param self Ukazatel na objekt
			"""
			if self.pr.isRnApp("closeSetup.py")==True:
				print "Already running"
			else:
				subprocess.Popen("./closeSetup.py", shell=True)
		def paintLayout(self):
			""" Metoda vykreslující grafické prvky okna
			Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
			\param self Ukazatel na objekt
			"""
			# test obsahu služby iTalc
			if os.path.isfile("/usr/bin/ica"):
				isIca=False
				p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
				out, err = p.communicate()
				for line in out.splitlines():
					if 'ica' in line:
						isIca=True
				if isIca == False:
					subprocess.Popen("/usr/bin/ica", shell=True)
			# Správa
			gpMan = LabelFrame(self.root, text="Ovládání", padx=5, pady=5)
			gpMan.place(relx=0.01, rely=0)
			Button(gpMan,height=1, width=19,text="iTalc",command=self.iTa).pack()
			Button(gpMan,height=1, width=19,text="Zákazy a povolení",command=self.enDis).pack()
			Button(gpMan,height=1, width=19,text="Sdílení",command=self.enSh).pack()
			# Nastavování
			gpSet = LabelFrame(self.root, text="Nastavení", padx=5, pady=5)
			gpSet.place(relx=0.01, rely=0.4)
			Button(gpSet,height=1, width=19,text="Základní nastavení učebny",command=self.clSet).pack()
			Button(gpSet,height=1, width=19,text="Nastavení účelu učebny",command=self.stFoc).pack()
			# Opravy
			gpRep = LabelFrame(self.root, text="Opravy", padx=5, pady=5)
			gpRep.place(relx=0.01, rely=0.7)
			Button(gpRep,height=1, width=19,text="Oprava systému",command=self.stRep).pack()
			Button(gpRep,height=1, width=19,text="Čištění systému",command=self.stCle).pack()
			# Výpisky
			gpTh = LabelFrame(self.root, text="Noví klienti", padx=5, pady=5)
			gpTh.place(relx=0.48, rely=0.0)
			scrollbar = Scrollbar(self.root)
			## List pro výpis změn v systému
			self.to = Listbox(gpTh,height=13, width=27, bd=0, yscrollcommand=scrollbar.set)
			self.to.pack()
			self.to.insert('end', "Zatím nic...")
			scrollbar.pack(side=RIGHT, fill=Y)
			scrollbar.config(command=self.to.yview)
			# Progres
			Label(self.root,height=1, width=21,text="Zatížení učebny:").place(relx=0.42, rely=0.82)
			## Ukazatel vytížení počítače
			self.progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
			self.progressbar.place(relx=0.5, rely=0.89)
			self.progressbar["value"]=0
			self.progressbar["maximum"]=100
			# načítání progressbaru
			## Obsahuje instanci vytížení systému
			self.sl=SysLoad()
			self.loadProgs(self.qo)
		def loadProgs(self,qc):
			""" Metoda pro načítání progressbaru a vyplování listu
			\param self Ukazatel na objekt
			\param qc Výstupní fronta
			"""
			try:
				st=qc.get(0)
				self.to.insert('end',st)
				self.to.select_clear(self.to.size()-2)
				self.to.yview(END)
			except Empty:
				#self.progressbar["value"]=self.sl.getLoadAvg()
				pass
			finally:			
				self.progressbar["value"]=self.sl.getLoadAvg()
				self.root.after(1000,self.loadProgs,qc)
		def enDis(self):
			""" Metoda pro spuštění povolení a zakázání
			\param self Ukazatel na objekt
			"""
			if self.pr.isRnApp("mnEnDis.py")==True:
				print "Already running"
			elif os.path.isfile("/NFSROOT/class/etc/hosts") and os.path.isfile("/NFSROOT/class/etc/resolv.conf"):
				subprocess.Popen("./mnEnDis.py", shell=True)
			else:
				tkMessageBox.showinfo("Chyba", "Zdá se, že třída ještě není nastavena. Použijte \"Základní nastavení učebny\"")
		def iTa(self):
			""" Metoda pro spuštění iTalcu
			\param self Ukazatel na objekt
			"""
			it=iTaHand()
			if it.tstItalc():
				subprocess.Popen("italc", shell=True)
			else:
				subprocess.Popen("./itWindow.py", shell=True)
		def qquit(self):
			""" Metoda pro ukončení okna
			Je nutné vypnout vlákno, které vykonává příkazy na pozadí okna
			\param self Ukazatel na objekt
			"""
			# ukončuje službu iTalc
			p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
			out, err = p.communicate()
			for line in out.splitlines():
				if os.path.isfile("/usr/bin/ica"):
					if 'ica' in line:
						pid = int(line.split(None, 1)[0])
						os.kill(pid, signal.SIGKILL)
			# ukončuje pracovní vlákno
			self.qi.put("XXX")
			self.root.destroy()
	def genOut(qi,qo):
		""" Funkce vlákna
		\param qi Vstupní fronta
		\param qo Vstupní fronta
		"""
		log=LogWrk()
		dhc=DhcpCheck()
		while True:
			stri = ""
			try:
				stri=qi.get(0)
			except Empty:
				pass
			finally:
				if stri == "XXX":
					break
				n=dhc.chcNew()
				if n is not None:
					for i in n:
						qo.put("Nový host s IP " + i)
						log.write("Nový host s IP " + i)
						qo.put("Přidávám do iTalcu")
						it=iTaHand()
						if it.isInTab(i):
							it.remCli(i)
							it.addCli(i,dhc.getMacByIpDh(i))
							log.write("Odebrán a přidán " + i)
						else:
							it.addCli(i,dhc.getMacByIpDh(i))
							log.write("Přidán " + i)
						qo.put("Přidáno")
						qo.put("Restartujte iTalc")
				time.sleep(1)
	## Vstupní fronta pracovního vlákna
	qi = multiprocessing.Queue()
	qi.cancel_join_thread()
	## Výstupní fronta pracovního vlákna
	qo = multiprocessing.Queue()
	qo.cancel_join_thread()
	## Pracovní vlákno
	t=multiprocessing.Process(target=genOut,args=(qi,qo,))
	t.start()
	## Hlavní instance okna TK
	win = Tk()
	## Instance okna třídy aplikace
	pp = App(win,qi,qo)
	pp.paintLayout()
	win.mainloop()
	t.join()
	