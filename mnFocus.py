#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file mnFocus.py
## \brief Okno pro volbu účelu učebny

from Tkinter import *
import webbrowser
import tkFileDialog
import tkMessageBox
from xmlFocPar import xmlFocPar
import tkFont
from inFocus import inFocus
import multiprocessing
from Queue import Empty, Full
import ttk
import os
import shutil
from ConsSys import ConsSys
from LogWrk import LogWrk

if __name__ == "__main__":
	class App:
		""" \brief Třída obsahující metody s prací s oknem
		Hlavní okno aplikace, slouží jako rozcestník
		"""
		def __init__(self,r,qoi):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na Tkinker okno
			\param qoi Vstupní fronta
			"""
			## Ukazatel na okno Tk
			self.root=r
			## List účelů s aplikacami
			self.lst=xmlFocPar()
			self.root.title("Nastavení účelu učebny")
			self.root.geometry(("%dx%d")%(440,340))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.protocol("WM_DELETE_WINDOW",self.qquit)
			self.root.resizable(0,0)
			## Vstupní fronta
			self.qoi=qoi
			## Logovací třída
			self.log=LogWrk()
			## Instance objektu spravující systémové nástroje
			self.sy=ConsSys()
			if os.path.isfile("/NFSROOT/class/proc/mounts"):
				self.log.write("/proc/mounts already there")
			else:
				open("/NFSROOT/class/proc/mounts","w")
			# mount proc /NFSROOT/class/proc -t proc
			tos='mount proc /NFSROOT/class/proc -t proc'
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
			# mount sysfs /NFSROOT/class/sys -t sysfs
			tos='mount sysfs /NFSROOT/class/sys -t sysfs'
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
		def __del__(self):
			""" Destruktor třídy okna
			Pročistí mounty a t.d.
			\param self Ukazatel na objekt
			"""
			tos='umount /NFSROOT/class/proc'
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
			tos='umount /NFSROOT/class/sys'
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
		def loadNXml(self):
			""" Načítání vnějších xml v podobě gml pomocí dialogového okna tkFileDialog
			\param self Ukazatel na objekt
			"""
			home=os.path.expanduser("~")
			fname=tkFileDialog.askopenfilename(filetypes=[("GnuŠkola list účelu","*.gml")],initialdir=home)
			ts=xmlFocPar()
			sy=ConsSys()
			try:
				ts.ldFoc(fname)
			except:
				tkMessageBox.showerror("Chyba","Zdá se, že soubor není list účelů pro učebnu.")
				return
			print(fname)
			nm=fname.split("/")[-1]
			if nm != "" and os.path.isfile("./focus/"+nm):
				sy.removeFl("./focus/"+nm)
			shutil.move(fname,"./focus/")
			f=inFocus()
			self.lst.relFoc()
			its=self.lst.getFoc().items()
			self.to.delete(0, END)
			sl=f.getLstInst()
			i=0
			for it in its:
				self.to.insert(i, it[1]['name'])
				if it[0] in sl:
					self.to.selection_set(first=i)
				i += 1
		def onSelect(self,evt):
			""" Metoda pro generování obsahu okýnka aplikací
			\param self Ukazatel na objekt
			\param evt Ukazatel na widget a jeho reakci na klik
			"""
			f=inFocus()
			w = evt.widget
			if w.curselection():
				index = w.curselection()
				self.tl.config(state=NORMAL)
				self.tl.delete(0, END)
				for i in index:
					self.tl.insert('end',self.lst.getFoc().items()[int(i)][1]['name'].upper())
					for it in self.lst.getFoc().items()[int(i)][1]['apps'].items():
						appNm=f.getApNmFrCom(it[1]['comm'])
						ts=f.getIfInst(appNm)
						self.tl.insert('end',it[1]['name'])
						if ts == False:
							self.tl.itemconfig(END, {'bg':'orange red'}) 
					self.tl.insert('end',"")
				#self.tl.config(state=DISABLED)
			else:
				self.tl.config(state=NORMAL)
				self.tl.delete(0, END)
				self.tl.config(state=DISABLED)
		def repLfLisb(self):
			""" Metoda pro překreslení okna instalací aplikací
			\param self Ukazatel na objekt
			"""
			f=inFocus()
			index = self.to.curselection()
			self.tl.delete(0, END)
			for i in index:
				self.tl.insert('end',self.lst.getFoc().items()[int(i)][1]['name'].upper())
				for it in self.lst.getFoc().items()[int(i)][1]['apps'].items():
					# Kontrola, zdali jsou aplikace nainstalované
					appNm=f.getApNmFrCom(it[1]['comm'])
					ts=f.getIfInst(appNm)
					self.tl.insert('end',it[1]['name'])
					if ts == False:
						self.tl.itemconfig(END, {'bg':'orange red'}) 
				self.tl.insert('end',"")
		def paintLayout(self):
			""" Metoda vykreslující grafické prvky okna
			Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
			\param self Ukazatel na objekt
			"""
			f=inFocus()
			
			Button(self.root,height=1, width=19,text="Přidat účel",command=self.loadNXml).place(relx=0.03, rely=0.02)
			
			gpTh = LabelFrame(self.root, text="Účel", padx=5, pady=5)
			gpTh.place(relx=0.01, rely=0.12)
			scrollbar = Scrollbar(gpTh)
			## Účely
			self.to = Listbox(gpTh,height=13, width=20, bd=0, yscrollcommand=scrollbar.set,selectmode="multiple")
			self.to.bind('<<ListboxSelect>>', self.onSelect)
			self.to.pack(side=LEFT)
			its=self.lst.getFoc().items()
			sl=f.getLstInst()
			i=0
			for it in its:
				self.to.insert(i, it[1]['name'])
				if it[0] in sl:
					self.to.selection_set(first=i)
				i += 1
			scrollbar.pack(side=RIGHT, fill=Y)
			scrollbar.config(command=self.to.yview)
			gpTh = LabelFrame(self.root, text="Aplikace", padx=5, pady=5)
			gpTh.place(relx=0.45, rely=0.129)
			scrollbar = Scrollbar(gpTh)
			## Informační text
			self.inl=Label(self.root,text="Červeně jsou označené aplikace,\nkteré nejsou nainstalovány")
			self.inl.place(relx=0.48, rely=0.02)
			## List aplikací
			self.tl = Listbox(gpTh,height=13, width=26, bd=0, yscrollcommand=scrollbar.set,disabledforeground="black")
			self.tl.pack(side=LEFT)
			
			if self.to.curselection():
				index = self.to.curselection()
				self.tl.config(state=NORMAL)
				self.tl.delete(0, END)
				for i in index:
					self.tl.insert('end',self.lst.getFoc().items()[int(i)][1]['name'].upper())
					for it in self.lst.getFoc().items()[int(i)][1]['apps'].items():
						# Kontrola, zdali jsou aplikace nainstalované
						appNm=f.getApNmFrCom(it[1]['comm'])
						ts=f.getIfInst(appNm)
						self.tl.insert('end',it[1]['name'])
						if ts == False:
							self.tl.itemconfig(END, {'bg':'orange red'}) 
					self.tl.insert('end',"")
				
			#self.tl.config(state=DISABLED)
			
			scrollbar.pack(side=RIGHT, fill=Y)
			scrollbar.config(command=self.tl.yview)

			l=Label(self.root,text="Pokud chybí účel, který \n potřebuje, můžete použít",cursor="hand2")
			l.place(relx=0.01, rely=0.8)
			l=Label(self.root,text="stránku účelů učeben.",fg="Blue",cursor="hand2")
			l.place(relx=0.02, rely=0.89)
			l.bind("<Button-1>",self.callPage)
			## Tlačíko spouštějící instalace
			self.b=Button(self.root,height=1, width=19,text="Připravit vybrané",command=self.insSet)
			self.b.place(relx=0.51, rely=0.8)
			## Ukazatel vyhotovení instalace
			self.progressbar = ttk.Progressbar(orient=HORIZONTAL, length=196, mode='determinate')
			self.progressbar.place(relx=0.49, rely=0.9)
			self.progressbar["value"]=0
			self.progressbar["maximum"]=100
			
			self.root.after(100,self.mvBar,self.qoi)
		def mvBar(self,qc):
			""" Metoda pro změnu průběhového ukazatele
			\param self Ukazatel na objekt
			\param qc Výstupní fronta vlákna
			"""
			try:
				st=qc.get(0)
				self.h += 1
				self.progressbar["maximum"]=self.cn
				self.progressbar["value"]=self.h
				if self.h != self.cn:
					self.b['state']='disabled'
					self.b['text']="Vyčkejte prosím"
				else:
					self.inl.configure(text="Červeně jsou označené aplikace,\nkteré nejsou nainstalovány")
					self.repLfLisb()
					self.b['state']='normal'
					self.b['text']="Připravit vybrané"
				#print(stri)
			except Empty:
				pass
			finally:
				self.root.after(100,self.mvBar,qc)
		def callPage(self,event):
			""" Metoda pro spuštění stránky s účelama učebny
			\param self Ukazatel na objekt
			\param event Ukazatel na akci
			"""
			webbrowser.open_new(r"http://www.nemor.cz/gnuClassConf/focus")
		def insSet(self):
			""" Metoda spuští instalaci balíčků v systému
			\param self Ukazatel na objekt
			"""
			f=inFocus()
			idxs = self.to.curselection()
			nt=self.lst.getFoc()
			rms=[x for x in range(0,len(nt.items()))]
			self.b['state']='disabled'
			self.inl.configure(text="VYČKEJTE, NEŽ SE UKONČÍ\nINSTALACE!")
			print "Add"
			## Počet načtených balíčků
			self.h=0
			self.progressbar["value"]=self.h
			## Celkový počet instalovaných balíčků
			self.cn=0
			qi.put("RCA")
			for i in idxs:
				rms.remove(int(i))
				f.instXmlCo(self.lst.getFoc().items()[int(i)][0])
				for it in self.lst.getFoc().items()[int(i)][1]['apps'].items():
					qi.put("INST:" + str(i) + ":" + it[1]['comm'])
					print it[1]['name']
					self.cn += 1
			print "Remove"
			qi.put("RCA")
			for i in rms:
				f.uniXmlCo(self.lst.getFoc().items()[int(i)][0])
				for it in self.lst.getFoc().items()[int(i)][1]['apps'].items():
					qi.put("REMO:" + str(i) + ":" + it[1]['uni'])
					print it[1]['name']
					self.cn += 1
		def qquit(self):
			""" Metoda pro ukončení okna
			Je nutné vypnout vlákno, které vykonává příkazy na pozadí okna
			\param self Ukazatel na objekt
			"""
			qi.put("XXX")
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
			elif stri == "RCA":
				f.dpkgConfA()
			elif stri.split(":")[0] == "INST":
				print(stri.split(":")[2])
				f.exCom(stri.split(":")[2])
				qo.put("IN:"+stri.split(":")[1])
			elif stri.split(":")[0] == "REMO":
				print(stri.split(":")[2])
				f.exCom(stri.split(":")[2])
				qo.put("RN:"+stri.split(":")[1])
	## Hlavní instance okna TK
	win = Tk()
	## Vstupní fronta pracovního vlákna
	qi = multiprocessing.Queue()
	qi.cancel_join_thread()
	## Výstupní fronta pracovního vlákna
	qo = multiprocessing.Queue()
	qo.cancel_join_thread()
	## Vlákna pracovního vlákna
	t=multiprocessing.Process(target=genOut,args=(qi,qo,))
	t.start()
	## Instance okna
	pp = App(win,qo)
	pp.paintLayout()
	win.mainloop()
	t.join()