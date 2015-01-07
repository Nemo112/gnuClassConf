#!/bin/bash
[[ "$1" != "" ]] && { exit 1; }
doxygen doxyfile;
p=$PWD;
cd ..;
tar cvf ./gnuClassConf.tar ./gnuClassConf;
gzip -f ./gnuClassConf.tar;
scp ./gnuClassConf.tar.gz nemo@nemor.cz:/raid/home/nemo/00_imp_data_rep_nemo/SKOLA2/baka_prace;
scp ./gnuClassConf.tar.gz nemo@nemor.cz:/raid/www/gnuclassconf/src;
cd $p;
nmb=$(./makeBuild.sh);
scp ./$nmb nemo@nemor.cz:/raid/www/gnuclassconf/src;
nmb=$(./makeBuild.sh vb);
scp ./$nmb nemo@nemor.cz:/raid/www/gnuclassconf/src;
