################################################################################
#
# @see Makefiles in the main dir, call this with make -B to always compile new
#
################################################################################

all: check1 check2 check3 check4
.PHONY: check1 check2 check3 check4

SHELL := /bin/bash
OPENQXD_SRC := ../src/openQxD-devel
QUDA_SRC := "../src/quda"
QUDA_BUILD_PATH := "../build"

# Target GPU architecture
# sm_60 = P100 (yoshi.ethz.ch)
# sm_61 = NVIDIA TITAN Xp (spaceml4.ethz.ch)
# @see https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/
# @see https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#gpu-feature-list
# @see https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#virtual-architecture-feature-list
CMAKE_FLAGS += -DQUDA_GPU_ARCH=sm_60
#CMAKE_FLAGS += -DQUDA_GPU_ARCH_SUFFIX=real # real or virtual, see links above

# see https://github.com/lattice/quda/wiki/QUDA-Build-With-CMake#reducing-qudas-build-time
CMAKE_FLAGS += -DCMAKE_BUILD_TYPE=DEVEL # DEVEL, RELEASE, STRICT, DEBUG, HOSTDEBUG, SANITIZE

####################
#    Compilers     #
####################

# Uncomment to use GNU C++ (version 11) compiler on yoshi
CMAKE_FLAGS += -DCMAKE_CXX_COMPILER=/usr/bin/g++-11

# Uncomment to use Clang C++ (version 14) compiler on yoshi
#CMAKE_FLAGS += -DCMAKE_CXX_COMPILER=/usr/bin/clang++-14

# This select GNU gcc 11 on yoshi
CMAKE_FLAGS += -DCMAKE_C_COMPILER=/usr/bin/gcc-11
CMAKE_FLAGS += -DMPI_CXX_SKIP_MPICXX=ON

# This selects CUDA 12.0 on yoshi
CMAKE_FLAGS += -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc
CMAKE_FLAGS += -DCUDAToolkit_BIN_DIR=/usr/local/cuda/bin
CMAKE_FLAGS += -DCUDAToolkit_INCLUDE_DIR=/usr/local/cuda/include

# This speeds up compilation substantially
CMAKE_FLAGS += -DCMAKE_CUDA_COMPILER_LAUNCHER=ccache
CMAKE_FLAGS += -DCMAKE_CXX_COMPILER_LAUNCHER=ccache

# To mimic QUDAs CI/CD tests
# * uncomment below flags
# * set CMAKE_BUILD_TYPE=STRICT
# * set QUDA_GPU_ARCH_SUFFIX=virtual
# * comment QUDA_MAX_MULTI_BLAS_N=1
#CMAKE_FLAGS += -DQUDA_MDW_FUSED_LS_LIST=4
#CMAKE_FLAGS += -DQUDA_MULTIGRID_NVEC_LIST=24
#CMAKE_FLAGS += -DQUDA_MULTIGRID_MRHS_LIST=16
#CMAKE_FLAGS += -DQUDA_JITIFY=ON # needs LibDL, does just-in-time compilation of kernels

####################
# Dirac Operators  #
####################
CMAKE_FLAGS += -DQUDA_DIRAC_DEFAULT_OFF=ON		# disables ALL Dirac operators
CMAKE_FLAGS += -DQUDA_DIRAC_WILSON=ON			# enables Wilson-Dirac operators
CMAKE_FLAGS += -DQUDA_DIRAC_CLOVER=ON			# enables Wilson-clover operators


CMAKE_FLAGS += -DQUDA_PRECISION=14				# 4-bit number that specifies which precisions we will enable
												# (8 - double, 4 - single, 2 - half, 1 - quarter).
CMAKE_FLAGS += -DQUDA_RECONSTRUCT=7				# 3-bit number that specifies which reconstructs we will enable
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
CMAKE_FLAGS += -DQUDA_MULTIGRID=ON

quda_ninja:
	mkdir -p $(QUDA_BUILD_PATH)
	cmake $(CMAKE_FLAGS) -GNinja -B $(QUDA_BUILD_PATH) $(QUDA_SRC)
	cmake --build $(QUDA_BUILD_PATH)

quda_update:
	cd $(QUDA_BUILD_PATH) && ninja

quda_make quda:
	mkdir -p $(QUDA_BUILD_PATH)
	cd $(QUDA_BUILD_PATH) && cmake ${QUDA_SRC} $(CMAKE_FLAGS)
	cd $(QUDA_BUILD_PATH) && $(MAKE) -j 24

quda_clean:
	rm -rf ../build

check1:
	cd $(OPENQXD_SRC)/devel/quda/ && $(MAKE) -j 24 check1
	cp $(OPENQXD_SRC)/devel/quda/check1 .

check2:
	cd $(OPENQXD_SRC)/devel/quda/ && $(MAKE) -j 24 check2
	cp $(OPENQXD_SRC)/devel/quda/check2 .

check3:
	cd $(OPENQXD_SRC)/devel/quda/ && $(MAKE) -j 24 check3
	cp $(OPENQXD_SRC)/devel/quda/check3 .

check4:
	cd $(OPENQXD_SRC)/devel/quda/ && $(MAKE) -j 24 check4
	cp $(OPENQXD_SRC)/devel/quda/check4 .

clean:
	cd $(OPENQXD_SRC)/devel/quda/ && $(MAKE) clean
	rm -f check1 check2 check3 check4
