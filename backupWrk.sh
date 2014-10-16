#!/bin/bash
[[ "$1" != "" ]] && { exit 1; }
doxygen doxyfile;
p=$PWD;
cd ..;
tar cvf ./gnuClassConf.tar ./gnuClassConf;
gzip -f ./gnuClassConf.tar;
scp ./gnuClassConf.tar.gz nemo@nemor.cz:/raid/home/nemo/00_imp_data_rep_nemo/SKOLA2/baka_prace;
scp ./gnuClassConf.tar.gz nemo@nemor.cz:/raid/www/nemo/gnuClassConf/src;
cd $p;
./makeBuild.sh;
scp ./gnuClassConf_0.001_all.deb nemo@nemor.cz:/raid/www/nemo/gnuClassConf/src;
