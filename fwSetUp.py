#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file fwSetUp.py
## \brief Ovládání doménového přístupu pomocí klienského /etc/hosts a /etc/resolv.conf
import re
from ConsSys import ConsSys
from optparse import OptionParser

class fwSetUp:
	""" \brief Třída obsahující metody pro práci s /etc/hosts
	"""
	def __init__(self):
		""" Konstruktor třídy okna
		\param self Ukazatel na objekt
		"""
		## Klientský hosts
		self.clhs="/NFSROOT/class/etc/hosts"
		## Serverový hosts
		self.sehs="/etc/hosts"
	def blDom(self,domain):
		""" Metoda přidá do /etc/hosts překlad domény na učitelský počítač
		\param domain Doména k blokování
		\param self Ukazatel na objekt
		\return False pokud už záznam existuje, True pokud se přidá bez problémů
		"""
		sy=ConsSys()
		dc=self.getLstBl()
		for it in dc.items():
			if it[1]['hostname'] == domain:
				return False
		inIp=sy.getEthIp(sy.getDfIlInt()['in'])
		tar = open (self.clhs, 'a')
		tar.write(inIp + "\t\t" + domain +"\n") 
		tar.close()
		return True
	def unDom(self,domain):
		""" Metoda odebere z /etc/hosts překlad domény na učitelský počítač
		\param domain Doména k odblokování
		\param self Ukazatel na objekt
		\return True pokud vše proběhlo v pořádku, False pokud ne
		"""
		if domain == "localhost":
			return False
		if domain == "ip6-localnet":
			return False
		if domain == "ip6-loopback":
			return False
		if domain == "ip6-mcastprefix":
			return False
		if domain == "ip6-allnodes":
			return False
		if domain == "ip6-allrouters":
			return False
		ts=""
		for line in open(self.clhs):
			ip=line.split("\t")[0]
			host=line.split("\t")[-1][0:-1]
			if host == domain:
				continue
			else:
				ts = ts + line
		tar = open (self.clhs, 'w')
		tar.write(ts) 
		tar.close()
		return True
	def relBlDom(self,domain):
		""" Metoda oblokuje doménu ale nechá jí v tabulce
		\param domain Doména k odblokování
		\param self Ukazatel na objekt
		\return True pokud vše proběhlo v pořádku, False pokud ne
		"""
		if self.unDom(domain) == False:
			return False
		sy=ConsSys()
		dc=self.getLstBl()
		for it in dc.items():
			if it[1]['hostname'] == domain:
				return False
		inIp=sy.getEthIp(sy.getDfIlInt()['in'])
		tar = open (self.clhs, 'a')
		tar.write("#"+inIp + "\t\t" + domain +"\n") 
		tar.close()
		return True
	def isNet(self):
		""" Metoda zkontroluje stav blokování klientů
		\param self Ukazatel na objekt
		\return True pokud jsou blokovány, false pokud ne
		"""
		ts=""
		for line in open("/NFSROOT/class/etc/resolv.conf"):
			fr=line.split(" ")[0]
			se=line.split(" ")[-1][0:-1]
			if fr == "nameserver" and se =="127.0.0.1":
				return True
			else:
				return False
	def blNet(self):
		""" Metoda zablokuje přístup na internet (upraví /etc/resolv.conf hosta)
		\param self Ukazatel na objekt
		\return True pokud vše projde, False pokud už v listu neni
		"""
		ts=""
		for line in open("/NFSROOT/class/etc/resolv.conf"):
			fr=line.split(" ")[0]
			se=line.split(" ")[-1][0:-1]
			if fr == "nameserver":
				ts = ts + "nameserver 127.0.0.1" + "\n"
			else:
				ts = ts + line
		tar = open ("/NFSROOT/class/etc/resolv.conf", 'w')
		tar.write(ts) 
		tar.close()
	def unBlNet(self):
		""" Metoda odblokuje přístup na internet (upraví /etc/resolv.conf hosta)
		\param self Ukazatel na objekt
		\return True pokud vše projde, False pokud už v listu neni
		"""
		ts=""
		sy=ConsSys()
		for line in open("/NFSROOT/class/etc/resolv.conf"):
			fr=line.split(" ")[0]
			se=line.split(" ")[-1][0:-1]
			if fr == "nameserver":
				ts = ts + "nameserver " + sy.getDnsSer() + "\n"
			else:
				ts = ts + line
		tar = open ("/NFSROOT/class/etc/resolv.conf", 'w')
		tar.write(ts) 
		tar.close()
	def getLstBl(self):
		""" Metoda načte /etc/hosts a udělá seznam blokovaných domén
		\param self Ukazatel na objekt
		\return lst List jako slovník obsahující položky očíslované od 0-n, kde každá obsahuje hostname a ip
		"""
		i=0
		lst={}
		for line in open(self.clhs):
			ip4=line.split("\t")[0]
			hst=line.split("\t")[-1]
			#print hst
			st=re.match(r"student[0-9]*",hst)
			if st:
				continue
			aa=re.match(r"^((0|[1-9]|[1-9][0-9]|[1-2][0-9][0-9])\.){3}(0|[1-9]|[1-9][0-9]|[1-2][0-9][0-9])$",ip4)
			bb=re.match(r"^#((0|[1-9]|[1-9][0-9]|[1-2][0-9][0-9])\.){3}(0|[1-9]|[1-9][0-9]|[1-2][0-9][0-9])$",ip4)
			if aa:
				ip4 = aa.group()
				cols={}
				cols['hostname']=line.split("\t")[-1][0:-1]
				cols['ip']=ip4
				if cols['hostname'] == "localhost":
					continue
				cols['blocking'] = True
				lst[i]=cols
				i += 1
			elif 	bb:
				ip4 = bb.group()
				cols={}
				cols['hostname']=line.split("\t")[-1][0:-1]
				cols['ip']=ip4
				if cols['hostname'] == "localhost":
					continue
				cols['blocking'] = False
				lst[i]=cols
				i += 1
		return lst
if __name__ == "__main__":
	## Parser argumentů a parametrů
	parser = OptionParser(usage="usage: %prog [args]\n Serve for /etc/hosts management in client filesystem")

	parser.add_option("-b", "--block-net", action="store_true", dest="prBl", default=False,  help="Block internet by messing DNS path in client list")

	parser.add_option("-u", "--unblock-net", action="store_true", dest="prUl", default=False, help="Unblock internet by messing DNS path in client list")

	parser.add_option("-l", "--blocked-list",  action="store_true", dest="lst", default=False, help="Give a list of blocked domains")
	parser.add_option("-s", "--block-domain", action="store", type="string", dest="blD", default="", help="Tells to hosts that domain is on different IP")
	parser.add_option("-g", "--unblock-domain", action="store", type="string", dest="unDom", default="", help="Unblock domain")
	## Argumenty a parametry z parseru			
	(args, opts) = parser.parse_args()
	## Instance objektu
	f=fwSetUp()
	if args.prUl == True:
		f.unBlNet()
	if args.lst == True:
		for i in f.getLstBl():
			print f.getLstBl()[i]['hostname']
	if args.prBl == True:
		f.blNet()
	if args.unDom != "":
		f.unDom(args.unDom)
	if args.blD != "":
		f.blDom(args.blD)
	