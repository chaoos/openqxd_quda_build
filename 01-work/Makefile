################################################################################
#
# @see Makefiles in the main dir, call this with make -B to always compile new
#
################################################################################

all: check1 check5
.PHONY: check1 check5

# target GPU architecture
# sm_60 = P100
# see https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/
QUDA_BUILD_TARGET := sm_60

SHELL := /bin/bash
OPENQXD_HOME := ../src/openQxD-devel
QUDA_HOME := "../src/quda"
QUDA_BUILD_PATH := "../build"

CMAKE_FLAGS += -DCMAKE_BUILD_TYPE=DEVEL
CMAKE_FLAGS += -DQUDA_GPU_ARCH=$(QUDA_BUILD_TARGET)
CMAKE_FLAGS += -DQUDA_DIRAC_DEFAULT_OFF=ON
CMAKE_FLAGS += -DQUDA_DIRAC_CLOVER=ON
CMAKE_FLAGS += -DQUDA_DIRAC_WILSON=ON
CMAKE_FLAGS += -DQUDA_PRECISION=12
CMAKE_FLAGS += -DQUDA_RECONSTRUCT=4
CMAKE_FLAGS += -DQUDA_FAST_COMPILE_DSLASH=ON
CMAKE_FLAGS += -DQUDA_FAST_COMPILE_REDUCE=ON
CMAKE_FLAGS += -DQUDA_INTERFACE_OPENQCD=ON 		# compile the openqxd interface
CMAKE_FLAGS += -DQUDA_MPI=ON 					# enable MPI
CMAKE_FLAGS += -DQUDA_DOWNLOAD_USQCD=OFF
CMAKE_FLAGS += -DQUDA_QIO=OFF
CMAKE_FLAGS += -DQUDA_QMP=OFF
CMAKE_FLAGS += -DQUDA_REORDER_LOCATION=GPU

quda_ninja:
	mkdir -p $(QUDA_BUILD_PATH)
	cd $(QUDA_BUILD_PATH) && cmake -GNinja $(QUDA_HOME) $(CMAKE_FLAGS)
	cd $(QUDA_BUILD_PATH) && ninja

quda_make:
	mkdir -p $(QUDA_BUILD_PATH)
	cd $(QUDA_BUILD_PATH) && cmake ${QUDA_HOME} $(CMAKE_FLAGS)
	cd $(QUDA_BUILD_PATH) && make -j 12

check1:
	cd $(OPENQXD_HOME)/devel/quda/uflds/ && $(MAKE) check1
	cp $(OPENQXD_HOME)/devel/quda/uflds/check1 .

check5:
	cd $(OPENQXD_HOME)/devel/quda/uflds/ && $(MAKE) check5
	cp $(OPENQXD_HOME)/devel/quda/uflds/check5 .

check2:
	cd $(OPENQXD_HOME)/devel/quda/uflds/ && $(MAKE) check2
	cp $(OPENQXD_HOME)/devel/quda/uflds/check2 .

clean:
	cd $(OPENQXD_HOME)/devel/quda/uflds/ && $(MAKE) clean
	rm -f check1

quda_clean:
	rm -rf ../build
