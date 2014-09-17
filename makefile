TDIR=/opt/gnuClassConf

all: prepare install luncher

luncher:
	./instLouncher.sh
install:
	test "$(PWD)" = "$(TDIR)" && { exit 10; } || { test -d "$(TDIR)" && {  cp . "$(TDIR)"; } || { mkdir "$(TDIR)" &&  cp . "$(TDIR)"; } }
prepare:
	apt-get install python-tk python3 -y
doc:
	doxygen doxyfile
bac:
	./backupWrk.sh