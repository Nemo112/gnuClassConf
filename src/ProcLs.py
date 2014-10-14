#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file ProcLs.py
## \brief Třída pro práci s procesy
import time
import os
import sys
import subprocess

class ProcLs:
	"""\brief Třída pro práci s procesy systému
	"""
	def killApp(self,name):
		""" Ukončí aplikaci podle jména
		\param name Jméno aplikace
		\param self Ukazatel na objekt
		\return True pokud je proces ukončen
		"""
		p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
		out, err = p.communicate()
		for line in out.splitlines():
			if name in line:
				pid = int(line.split(None, 1)[0])
				os.kill(pid, signal.SIGKILL)
				return True
		return False
	def isRnApp(self,name):
		""" Zjišťuje, zdali aplikace běží
		\param name Jméno aplikace
		\param self Ukazatel na objekt
		\return True pokud běží, False pokud ne
		"""
		p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
		out, err = p.communicate()
		for line in out.splitlines():
			if name in line:
				pid = int(line.split(None, 1)[0])
				return True
		return False
