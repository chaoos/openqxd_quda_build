################################################################################
#
# @see Makefiles in the main dir, call this with make -B to always compile new
#
################################################################################

targets = check1 check1j check2 check2a check3
all: $(targets)
.PHONY: all
.PHONY: clean

# target GPU architecture
# sm_60 = P100 (yoshi.ethz.ch)
# sm_61 = NVIDIA TITAN Xp (spaceml4.ethz.ch)
# see https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/
QUDA_BUILD_TARGET := sm_60

SHELL := /bin/bash
OPENQXD_SRC := ../src/openQxD-devel
QUDA_SRC := "../src/quda"
QUDA_BUILD_PATH := "../build"

# see https://github.com/lattice/quda/wiki/QUDA-Build-With-CMake#reducing-qudas-build-time
CMAKE_FLAGS += -DCMAKE_BUILD_TYPE=DEBUG
CMAKE_FLAGS += -DQUDA_GPU_ARCH=$(QUDA_BUILD_TARGET)

####################
#    Compilers     #
####################
CMAKE_FLAGS += -DCMAKE_C_COMPILER=/usr/bin/gcc-9
CMAKE_FLAGS += -DCMAKE_CXX_COMPILER=/usr/bin/g++-9
CMAKE_FLAGS += -DCMAKE_Fortran_COMPILER=/usr/bin/gfortran-9

####################
# Dirac Operators  #
####################
CMAKE_FLAGS += -DQUDA_DIRAC_DEFAULT_OFF=ON		# disables ALL Dirac operators
CMAKE_FLAGS += -DQUDA_DIRAC_WILSON=ON			# enables Wilson-Dirac operators
CMAKE_FLAGS += -DQUDA_DIRAC_CLOVER=ON			# enables Wilson-clover operators


CMAKE_FLAGS += -DQUDA_PRECISION=12				# 4-bit number that specifies which precisions we will enable
												# (8 - double, 4 - single, 2 - half, 1 - quarter).
CMAKE_FLAGS += -DQUDA_RECONSTRUCT=4				# 3-bit number that specifies which reconstructs we will enable
												# (4 - reconstruct-no, 2 - reconstruct-12/13, 1 - reconstruct-8/9).
CMAKE_FLAGS += -DQUDA_FAST_COMPILE_DSLASH=ON	# only use in dev-mode to reduce compile time
CMAKE_FLAGS += -DQUDA_FAST_COMPILE_REDUCE=ON	# only use in dev-mode to reduce compile time
CMAKE_FLAGS += -DQUDA_MPI=ON					# enable MPI
CMAKE_FLAGS += -DQUDA_MAX_MULTI_BLAS_N=1 		# disables some kernel fusion optimization for BLAS routines
												# (reduces compile time)

####################
#    Interfaces    #
####################
CMAKE_FLAGS += -DQUDA_INTERFACE_OPENQCD=ON		# enable openQCD interface
CMAKE_FLAGS += -DQUDA_INTERFACE_MILC=OFF		# disable MILC interface
CMAKE_FLAGS += -DQUDA_INTERFACE_QDP=OFF			# disable QDP interface
CMAKE_FLAGS += -DQUDA_INTERFACE_BQCD=OFF		# disable BQCD interface
CMAKE_FLAGS += -DQUDA_INTERFACE_CPS=OFF			# disable CPS interface
CMAKE_FLAGS += -DQUDA_INTERFACE_QDPJIT=OFF		# disable QDPJIT interface
CMAKE_FLAGS += -DQUDA_INTERFACE_TIFR=OFF		# disable TIFR interface

CMAKE_FLAGS += -DQUDA_DOWNLOAD_USQCD=OFF
CMAKE_FLAGS += -DQUDA_QIO=OFF
CMAKE_FLAGS += -DQUDA_QMP=OFF
CMAKE_FLAGS += -DQUDA_REORDER_LOCATION=GPU

quda_ninja:
	mkdir -p $(QUDA_BUILD_PATH)
	cd $(QUDA_BUILD_PATH) && cmake -GNinja $(QUDA_SRC) $(CMAKE_FLAGS)
	cd $(QUDA_BUILD_PATH) && ninja

quda_update:
	cd $(QUDA_BUILD_PATH) && ninja

quda_make quda:
	mkdir -p $(QUDA_BUILD_PATH)
	cd $(QUDA_BUILD_PATH) && cmake ${QUDA_SRC} $(CMAKE_FLAGS)
	cd $(QUDA_BUILD_PATH) && $(MAKE) -j 24

quda_clean:
	rm -rf ../build

# $@ means current target in targets
$(targets):
	cd $(OPENQXD_SRC)/devel/quda/ && $(MAKE) -j 24 $@
	cp $(OPENQXD_SRC)/devel/quda/$@ .

clean:
	cd $(OPENQXD_SRC)/devel/quda/ && $(MAKE) clean
	rm -f $(targets)