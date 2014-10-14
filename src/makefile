all: prepare install luncher

luncher:
	./instLouncher.sh
install:
	./install.sh
prepare:
	apt-get install python-tk python3 -y
doc:
	doxygen doxyfile
bac:
	./backupWrk.sh
