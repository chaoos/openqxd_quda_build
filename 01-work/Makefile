################################################################################
#
# @see Makefiles in the main dir, call this with make -B to always compile new
#
################################################################################

all: check1
.PHONY: check1

SHELL := /bin/bash
OPENQXD_HOME := ../src/openQxD-devel

quda:
	source build_ninja.sh

check1:
	cd $(OPENQXD_HOME)/devel/quda/uflds/ && $(MAKE) check1
	cp $(OPENQXD_HOME)/devel/quda/uflds/check1 .

clean:
	cd $(OPENQXD_HOME)/devel/quda/uflds/ && $(MAKE) clean
	rm -f check1

make clean_quda:
	rm -rf ../build
