#!/bin/bash
tar --absolute-names -c -v -f ../gnuClassConf.tar /opt/gnuClassConf;
gzip -f ../gnuClassConf.tar;
