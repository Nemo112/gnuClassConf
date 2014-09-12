#!/bin/bash
p=$PWD;
cd /;
tar --absolute-names -c -f /opt/gnuClassConf.tar /opt/gnuClassConf;
cd /opt;
gzip -f ./gnuClassConf.tar;
cd $p;
