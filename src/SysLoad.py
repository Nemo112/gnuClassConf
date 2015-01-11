#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file SysLoad.py
# \brief Třída pro načítání zatížení systému

import os
import time
from ParConfFl import ParConfFl


class SysLoad:

    """ \brief Třída obsahující metody s prací s načítáním zatížení systému
    """

    def __init__(self, interval=0.1):
        """ Konstruktor třídy okna
        \param self Ukazatel na objekt
        \param interval Obnova času při načítání zatížení procesoru
        """
        # Interval obnovy statistiky
        self.int = interval

    def diskstatsParse(self, dev=None):
        """ Metoda parsující statistiky z /proc/diskstats
        \param self Ukazatel na objekt
        \param dev Jméno zařízení
        """
        file_path = '/proc/diskstats'
        result = {}
        columns_disk = ['m', 'mm', 'dev', 'reads', 'rd_mrg', 'rd_sectors',
                        'ms_reading', 'writes', 'wr_mrg', 'wr_sectors',
                        'ms_writing', 'cur_ios', 'ms_doing_io', 'ms_weighted']
        columns_partition = [
            'm',
            'mm',
            'dev',
            'reads',
            'rd_sectors',
            'writes',
            'wr_sectors']
        lines = open(file_path, 'r').readlines()
        for line in lines:
            if line == '':
                continue
            split = line.split()
            if len(split) == len(columns_disk):
                columns = columns_disk
            elif len(split) == len(columns_partition):
                columns = columns_partition
            else:
                continue
            data = dict(zip(columns, split))
            if dev is not None and dev != data['dev']:
                continue
            for key in data:
                if key != 'dev':
                    data[key] = int(data[key])
            result[data['dev']] = data
        return result

    def getTrReBy(self, eth):
        """ Metoda vracící celkový počet odeslaných a přijatých bytů rozhraní
        \param self Ukazatel na objekt
        \param eth Jméno rozhraní
        \return Číselný údaj
        """
        etl = open("/proc/net/dev", "r").readlines()
        for it in etl:
            if eth in it:
                ots = it
                break
        ts = " ".join(ots.split())
        tra = int(ts.split(" ")[1]) + int(ts.split(" ")[2])
        rec = int(ts.split(" ")[9]) + int(ts.split(" ")[10])
        return tra + rec

    def getLoadNet(self, eth="eth0"):
        """ Metoda vracící 0-100 jako procento zatížení rozhraní v proměnné eth
        \param self Ukazatel na objekt
        \param eth Jméno rozhraní
        \return Rozsah 0-100 jako procento zatížení
        """
        if os.path.isfile("/sys/class/net/" + eth + "/speed") is False:
            return 0
        try:
            h = open("/sys/class/net/" + eth + "/speed", "r")
        except:
            return 0
        try:
            hs = h.readline().replace("\n", "").replace(" ", "")
        except:
            return 0
        speed = int(hs) * self.int / 8 * 1024 * 1024
        cur1 = self.getTrReBy(eth)
        time.sleep(self.int)
        cur2 = self.getTrReBy(eth)
        return int((cur2 - cur1) / speed * 100)

    def getTimeList(self):
        """ Metoda parsující statistiky z /proc/stat
        \param self Ukazatel na objekt
        \return Mapu zparsovanou z /proc/stat
        """
        cpuStats = file("/proc/stat", "r").readline()
        columns = cpuStats.replace("cpu", "").split(" ")
        return map(int, filter(None, columns))

    def deltaTime(self, interval):
        """ Metoda vrací rozdíl z cpu statistik
        \param self Ukazatel na objekt
        \param interval Čas mezi delta časy
        \return Číselný rozdíl
        """
        timeList1 = self.getTimeList()
        time.sleep(interval)
        timeList2 = self.getTimeList()
        return [(t2 - t1) for t1, t2 in zip(timeList1, timeList2)]

    def getCpuLoad(self):
        """ Metoda vrací vytížení procesoru mezi 0 a 1
        \param self Ukazatel na objekt
        \return Číslo mezi 0 a 1
        """
        dt = list(self.deltaTime(self.int))
        idle_time = float(dt[3])
        total_time = sum(dt)
        if total_time == 0:
            total_time = 1
        load = 1 - (idle_time / total_time)
        return load

    def getPercCpuLoad(self):
        """ Metoda vrací vytížení procesoru v procentech 0 až 100
        \param self Ukazatel na objekt
        \return Procento mezi 0 až 100
        """
        return int(self.getCpuLoad() * 100.0)

    def getPercSdaLoad(self):
        """ Metoda vrací vytížení pevného disku v procentech 0 až 100
        \param self Ukazatel na objekt
        \return Procento mezi 0 až 100
        """
        dct = self.diskstatsParse("sda")
        st = (dct['sda']['cur_ios'] / 16) * 10
        return int(st)

    def getLoadAvg(self):
        """ Metoda vrací vytížení systému (disk,cpu,...)
        \param self Ukazatel na objekt
        \return Procento mezi 0 až 100
        """
        pri = ParConfFl()
        ints = pri.getInterfaces()
        if ints is not None:
            if ints['inti'] != "" and ints['outi'] != "":
                return((self.getPercSdaLoad() + self.getPercCpuLoad() + self.getLoadNet(ints['inti']) + self.getLoadNet(ints['outi'])) / 4)
            else:
                return((self.getPercSdaLoad() + self.getPercCpuLoad()) / 2)
        else:
            return((self.getPercSdaLoad() + self.getPercCpuLoad()) / 2)
if __name__ == "__main__":
    print("Jen pro import")
