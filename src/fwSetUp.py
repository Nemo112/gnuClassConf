#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file fwSetUp.py
## \brief Ovládání doménového přístupu pomocí klienského /etc/hosts a /etc/resolv.conf
import re
import subprocess
import os
from ConsSys import ConsSys
from optparse import OptionParser
import md5

class fwSetUp:
	""" \brief Třída obsahující metody pro práci s /etc/hosts
	"""
	def __init__(self):
		""" Konstruktor třídy okna
		\param self Ukazatel na objekt
		"""
		## List pravidel
		self.clhs="/NFSROOT/class/addons/rules.sh"
		sy=ConsSys()
		inIp=sy.getEthIp(sy.getDfIlInt()['in'])
		## Hash listu pravidel
		self.har="/NFSROOT/class/addons/harsh"
		## Příkazy pro blokování všeho
		self.bla = "iptables -I INPUT -s " + inIp + " -j ACCEPT;\n"
		self.bla += "iptables -I OUTPUT -d  " + inIp + " -j ACCEPT;\n"
		self.bla +="""
iptables -D OUTPUT -j ACCEPT;
iptables -D INPUT -j ACCEPT;
iptables -A OUTPUT -j DROP;
iptables -A INPUT -j DROP;
"""
		## Příkazy pro povolení všeho
		self.ola = """
iptables -A OUTPUT -j ACCEPT;
iptables -A INPUT -j ACCEPT;
iptables -D OUTPUT -j DROP;
iptables -D INPUT -j DROP;
"""
		if os.path.isfile(self.clhs):
			open(self.har,"w").write(md5.new(open(self.clhs,"r").read()).digest())
			os.chmod(self.har,0666)
		## Hlavička rules.sh souboru
		self.hed = "#!/bin/bash\n# Needitujte nikdy tento soubor!\n"
	def changeHash(self):
		""" Metoda vytvoří hash pravidel
		\param self Ukazatel na objekt
		"""
		# načte soubor pravidel
		r=open(self.clhs,"r")
		md=r.read()
		r.close()
		# vypočte hash a uloží
		f=open(self.har,"w")
		f.write(md5.new(md).digest())
		f.close()
	def getNETpa(self):
		""" Metoda pro vybrání části definující NET z konfiguračního souboru pravidel rules.sh
		\param self Ukazatel na objekt
		"""
		if os.path.isfile(self.clhs) == False:
			return ""
		f=open(self.clhs,"r")
		cn=f.read().split("\n")
		f.close()
		cod=""
		rd=False
		for line in cn:
			if line == "# NET" and rd == False:
				rd = True
			elif line == "# ===" and rd == True:
				rd = False
			elif rd == True:
				cod += line + "\n"
			else:
				continue
		return cod
	def getDOMpa(self):
		""" Metoda pro vybrání části definující DOM z konfiguračního souboru pravidel rules.sh
		\param self Ukazatel na objekt
		"""
		if os.path.isfile(self.clhs) == False:
			return ""
		f=open(self.clhs,"r")
		cn=f.read().split("\n")
		f.close()
		cod=""
		rd=False
		for line in cn:
			if line == "# DOM" and rd == False:
				rd = True
			elif line == "# ===" and rd == True:
				rd = False
			elif rd == True:
				cod += line + "\n"
			else:
				continue
		return cod
	def blDom(self,domain):
		""" Metoda přidá do rules.sh další záznam k blokování
		\param domain Doména k blokování
		\param self Ukazatel na objekt
		\return False pokud už záznam existuje, True pokud se přidá bez problémů
		"""
		l=self.getLstBl()
		for i in l:
			if l[i]['hostname'] == domain:
				return False
		if os.path.isfile(self.clhs) == False:
			return False
		net=self.getNETpa()
		dom=self.getDOMpa()
		twr = self.hed 
		twr += "# DOM\n" + dom  
		twr += "iptables -I INPUT -m tcp -p tcp -d \"" + domain.encode("utf-8")  +"\" --dport 443 -j DROP;\n";
		twr += "iptables -I FORWARD  -m string --string \"" + domain.encode("utf-8")  +"\" --algo bm --from 1 --to 600 -j REJECT;\n"
		twr += "iptables -I INPUT -p tcp --sport 443 -m string --string \"" + domain.encode("utf-8") + "\" --algo bm -j DROP;\n"
		twr += "iptables -I OUTPUT -p tcp --dport 80  -m string --string \"Host: " + domain.encode("utf-8") + "\" --algo bm -j DROP;\n" + "# ===\n"
		twr += "# NET\n" + net + "# ===\n"
		f = open(self.clhs,"w")
		f.write(twr.rstrip('\n'))
		f.close()
		self.changeHash()
	def unDom(self,domain):
		""" Metoda odebere doménu z listu blokování
		\param domain Doména k odblokování
		\param self Ukazatel na objekt
		\return True pokud vše proběhlo v pořádku, False pokud ne
		"""
		l=self.getLstBl()
		if os.path.isfile(self.clhs) == False:
			return False
		net=self.getNETpa()
		dom=self.getDOMpa()
		twr = self.hed
		twr += "# DOM\n"
		tdo = ""
		for i in dom.split("\n"):
			if ( " " + domain + "\"" in i or " " + domain + " " in i or "\"" + domain + "\"" in i) == False:
				tdo +=  i + "\n"
		twr += tdo + "# ===\n"
		twr += "# NET\n" + net + "# ===\n"
		f = open(self.clhs,"w")
		f.write(twr.rstrip('\n'))
		f.close()
		self.changeHash()
	def relBlDom(self,domain):
		""" Metoda oblokuje doménu ale nechá jí v tabulce
		\param domain Doména k odblokování
		\param self Ukazatel na objekt
		\return True pokud vše proběhlo v pořádku, False pokud ne
		"""
		l=self.getLstBl()
		if os.path.isfile(self.clhs) == False:
			return False
		net=self.getNETpa()
		dom=self.getDOMpa().rstrip('\n').lstrip('\n')
		twr = self.hed 
		twr += "# DOM\n"
		tdo = ""
		for i in dom.split("\n"):
			if i == "iptables -I INPUT -m tcp -p tcp -d \"" + domain.encode("utf-8")  +"\" --dport 443 -j DROP;":
				tdo += "iptables -D INPUT -m tcp -p tcp -d \"" + domain.encode("utf-8")  +"\" --dport 443 -j DROP;\n"
			elif i == "iptables -I FORWARD  -m string --string \"" + domain.encode("utf-8")  +"\" --algo bm --from 1 --to 600 -j REJECT;":
				tdo += "iptables -D FORWARD  -m string --string \"" + domain.encode("utf-8")  +"\" --algo bm --from 1 --to 600 -j REJECT;\n"
			elif i == "iptables -I INPUT -p tcp --sport 443 -m string --string \"" + domain.encode("utf-8") + "\" --algo bm -j DROP;":
				tdo += "iptables -D INPUT -p tcp --sport 443 -m string --string \"" + domain.encode("utf-8") + "\" --algo bm -j DROP;\n"
			elif i == "iptables -I OUTPUT -p tcp --dport 80  -m string --string \"Host: " + domain.encode("utf-8") + "\" --algo bm -j DROP;":
				tdo += "iptables -D OUTPUT -p tcp --dport 80  -m string --string \"Host: " + domain.encode("utf-8") + "\" --algo bm -j DROP;\n"
			else:
				tdo += i + "\n"
		twr += tdo + "# ===\n"
		twr += "# NET\n" + net + "# ===\n"
		f = open(self.clhs,"w")
		f.write(twr.rstrip('\n'))
		f.close()
		self.changeHash()
	def isNet(self):
		""" Metoda zkontroluje stav blokování klientů
		\param self Ukazatel na objekt
		\return True pokud jsou blokovány, False pokud ne
		"""
		if os.path.isfile(self.clhs) == False:
			return False
		f=open(self.clhs,"r")
		cn=f.read().split("\n")
		f.close()
		cod=""
		rd=False
		for line in cn:
			if line == "# NET" and rd == False:
				rd = True
			elif line == "# ===" and rd == True:
				rd = False
			elif rd == True:
				cod += line + "\n"
			else:
				continue
		if cod.rstrip('\n').lstrip('\n') == self.ola.rstrip('\n').lstrip('\n'):
			return False
		else:
			return True
	def blNet(self):
		""" Metoda zablokuje přístup na internet (upraví /addons/rules.sh hosta)
		\param self Ukazatel na objekt
		\return True pokud vše projde, False pokud už v listu neni
		"""
		if os.path.isfile(self.clhs) == False:
			return False
		f=open(self.clhs,"r")
		cn=f.read().split("\n")
		f.close()
		cod=""
		rd = False
		for line in cn:
			if line == "# NET" and rd == False:
				rd = True
			elif line == "# ===" and rd == True:
				rd = False
			elif rd == True:
				cod += line + "\n"
			else:
				continue
		if cod == self.ola:
			f=open(self.clhs,"r")
			cn=f.read().split("\n")
			f.close()
			sw = ""
			for line in cn:
				if line =="# NET" and rd == False:
					rd = True
					sw += "# NET\n" + self.bla + "# ===\n"
				if line =="# ===" and rd == True:
					rd = False
				elif rd == False:
					sw += line + "\n"		
			f=open(self.clhs,"w")
			cn=f.write(sw.rstrip('\n'))
			f.close()
			self.changeHash()
			return True
		return False
	def unBlNet(self):
		""" Metoda odblokuje přístup na internet
		\param self Ukazatel na objekt
		\return True pokud vše projde, False pokud už v listu neni
		"""
		if os.path.isfile(self.clhs) == False:
			return False
		f=open(self.clhs,"r")
		cn=f.read().split("\n")
		f.close()
		cod=""
		rd = False
		for line in cn:
			if line == "# NET" and rd == False:
				rd = True
			elif line == "# ===" and rd == True:
				rd = False
			elif rd == True:
				cod += line + "\n"
			else:
				continue
		if cod == self.bla:
			f=open(self.clhs,"r")
			cn=f.read().split("\n")
			f.close()
			sw = ""
			for line in cn:
				if line =="# NET" and rd == False:
					rd = True
					sw += "# NET\n" + self.ola + "# ===\n"
				if line =="# ===" and rd == True:
					rd = False
				elif rd == False:
					sw += line + "\n"		
			f=open(self.clhs,"w")
			cn=f.write(sw.rstrip('\n'))
			f.close()
			self.changeHash()
			return True
		return False
	def getLstBl(self):
		""" Metoda načte všechny blokované domény z rules
		\param self Ukazatel na objekt
		\return lst List jako slovník obsahující položky očíslované od 0-n, kde každá obsahuje hostname a ip
		"""
		i=0
		lst={}
		rd=False
		if os.path.isfile(self.clhs) == False:
			return lst
		f=open(self.clhs,"r")
		cn=f.read().split("\n")
		f.close()
		for line in cn:
			if line == "# DOM" and rd == False:
				rd = True
			elif line == "# ===" and rd == True:
				rd = False
			elif rd == True:
				m = re.search(r"\"Host: ([\wěščřžýáíé.]+)\"", line)
				if m != None:
					lst[i]={}
					if line.split()[1] == "-D":
						lst[i]['blocking'] = False
					else:
						lst[i]['blocking'] = True
					lst[i]['hostname']= m.group(1).decode("utf-8")
					i += 1
			else:
				continue
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
	