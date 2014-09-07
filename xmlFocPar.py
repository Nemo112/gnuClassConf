#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
## \file xmlFocPar.py
## \brief Třída parsující složku xml souborů ./focus/

import os
import xml.dom.minidom


class xmlFocPar:
	"""
	\brief Třída pro parsování souborů xml se zaměřením pro třídy
	"""
	def __init__(self,path="./focus/"):
		""" Konstruktor třídy sestavující seznam účelů
		\param self Ukazatel na objekt
		\param path Cesta k souborům obsahujícím popis účel učebny
		"""
		## Cesta k souborům
		self.pth=path
		## Seznam zaměření
		self.foc=self.getLstFoc()
	def relFoc(self):
		""" Reloadne zaměření
		\param self Ukazatel na objekt
		"""
		self.foc=self.getLstFoc()
	def getFoc(self):
		""" Vrací zaměření
		\param self Ukazatel na objekt
		\return Seznam zaměření
		"""
		return self.foc
	def getText(self,nodelist):
		""" Vrací text nodu
		\param self Ukazatel na objekt
		\param nodelist Ukazatel na
		\return Text s obsahem listu nodu
		"""
		rc = []
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc.append(node.data)
		return ''.join(rc)
	def getLstFoc(self):
		""" Vrací list všech účelů
		\param self Ukazatel na objekt
		\return List všech účelů ve složce
		"""
		lst={}
		for fl in os.listdir(self.pth):
			if fl.split(".")[-1] == "gml":
				lst[fl]=self.parFoc(fl)
		return lst
	def ldFoc(self,path):
		""" Vrací list obsahující vlastnosti účelu
		\param self Ukazatel na objekt
		\param path Cesta k účelu
		\return List všech vlastností účelu
		"""
		if path.split(".")[-1] == "gml":
			fl=file(path,'r')
			r=fl.read()
			dom = xml.dom.minidom.parseString(r)
			lst={}
			lst['name']=self.getText(dom.getElementsByTagName("name")[0].childNodes)
			lst['author']=self.getText(dom.getElementsByTagName("author")[0].childNodes)
			lst['note']=self.getText(dom.getElementsByTagName("note")[0].childNodes)
			lst['apps']=self.apps(dom.getElementsByTagName("app"))
			return lst
		else:
			return None
	def parFoc(self,path):
		""" Vrací list obsahující vlastnosti účelu
		\param self Ukazatel na objekt
		\param path Cesta k účelu
		\return List všech vlastností účelu
		"""
		if path.split(".")[-1] == "gml":
			fl=file(self.pth + path,'r')
			r=fl.read()
			dom = xml.dom.minidom.parseString(r)
			lst={}
			lst['name']=self.getText(dom.getElementsByTagName("name")[0].childNodes)
			lst['author']=self.getText(dom.getElementsByTagName("author")[0].childNodes)
			lst['note']=self.getText(dom.getElementsByTagName("note")[0].childNodes)
			lst['apps']=self.apps(dom.getElementsByTagName("app"))
			return lst
		else:
			return None
	def apps(self,aps):
		""" Vrací list aplikací v účelu
		\param self Ukazatel na objekt
		\param aps Ukazatel na node obsahující aplikace
		\return List všech aplikací účelu
		"""
		lst={}
		i=0
		for point in aps:
			lst[i]=(self.handleAps(point))
			i += 1
		return lst
	def handleAps(self,point):
		""" Vrací list jména a příkazu aplikace
		\param self Ukazatel na objekt
		\param point Ukazatel na aplikaci
		\return List se jménem a příkazem
		"""
		lst={}
		lst['name']=self.getText(point.getElementsByTagName("name")[0].childNodes)
		lst['comm']=self.getText(point.getElementsByTagName("comm")[0].childNodes)
		lst['uni']=self.getText(point.getElementsByTagName("uni")[0].childNodes)
		return lst
if __name__ == "__main__":
	print("Jen pro import")
	#x=xmlFocPar()
	#print(x.getLstFoc())