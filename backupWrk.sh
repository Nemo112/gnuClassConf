#!/bin/bash
p=$PWD;
cd /;
tar cvf /opt/gnuClassConf.tar /opt/gnuClassConf;
cd /opt;
gzip -f ./gnuClassConf.tar;
cd $p;
