# QUDA compile manual
This repository aims to help compiling [openQxD](https://gitlab.com/rcstar/openQxD-devel) against [QUDA](https://github.com/lattice/quda).

## Inital setup

```bash
# Clone this repo
git clone https://github.com/chaoos/openqxd_quda_build.git

cd openqxd_quda_build
# Clone the repos of openqxd and quda into src/
git clone -b feature/quda/main-thesis-release https://gitlab.com/rcstar/openQxD-devel.git src/openQxD-devel
git clone -b feature/openqxd-thesis-release https://github.com/chaoos/quda.git src/quda

# Download cmake v3.24 if not available (quda needs exactly this version!)
wget -P deps/ https://cmake.org/files/v3.24/cmake-3.24.2-linux-x86_64.tar.gz
tar xfs deps/cmake-3.24.2-linux-x86_64.tar.gz -C deps/
rm deps/cmake-3.24.2-linux-x86_64.tar.gz

# add the new cmake version to the PATH
export PATH=$(realpath deps/cmake-3.24.2-linux-x86_64/bin/):$PATH
```

## Environment on linux

Make sure that these are available

```bash
cmake --version # should be 3.24 now
nvcc --version
ninja --version # not strictly necessary, see below
gcc --version # should be gcc version 9.x
```

If you don't find `nvcc` you might need to modify your path variable. For example on yoshi.ethz.ch:

```bash
export PATH=/usr/local/cuda-11.6/bin:$PATH
```

If CUDA is not in `usr/local/cuda`, you need to modify

```bash
export CUDA_HOME=/opt/cuda # example path
```

Set the environment variables:

```bash
export GCC="gcc-9" # make sure it's gcc version 9.x
export MPI_HOME="/usr/lib/x86_64-linux-gnu/openmpi/" # for example
export MPI_INCLUDE="${MPI_HOME}/include"
```

## Environment on daint

Setup the environment on daint for quda

```bash
module purge
module load PrgEnv-gnu
module load daint-gpu
module load craype-accel-nvidia60 # adds nvcc to the path
module unload gcc/11.2.0
module load gcc/9.3.0 # we need this specific gcc version
module load cray-mpich
module load Ninja
```

Set the environment variables:

```bash
export CC=cc
export CXX=CC
export FC=ftn
export PATH=$(realpath deps/cmake-3.24.2-linux-x86_64/bin/):$PATH
export GCC="cc"
export CXX=CC
export MPI_HOME="${CRAY_MPICH_DIR}"
export MPI_INCLUDE="${MPI_HOME}/include"
```

Uncomment the compilers in `01-work/Makefile`:

```bash
# CMAKE_FLAGS += -DCMAKE_C_COMPILER=/usr/bin/gcc-9
# CMAKE_FLAGS += -DCMAKE_CXX_COMPILER=/usr/bin/g++-9
# CMAKE_FLAGS += -DCMAKE_Fortran_COMPILER=/usr/bin/gfortran-9
```

Check the environment:

```bash
cmake --version # should be 3.24 now
nvcc --version
ninja --version # not strictly necessary, see below
gcc --version # should be gcc version 9.x
```

## Compiling

Compile QUDA and openqxd in the `01-work` directory:

```bash
cd 01-work
make quda # or "make quda_make" or "make quda_ninja"
make check1 # this build check1 in openqxd and links it against quda dynamically
make check2
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$(realpath ../build/lib) # for the dynamic linker to find libquda.so
```

Verify with

```bash
ldd check1 # libquda should be in the LD_LIBRARY_PATH now
```

Output may look like:

```
[...]
libquda.so => /[...]/openqxd_quda_build/build/lib/libquda.so (0x000014e90fcf8000)
[...]
```

## Running binaries

```bash
# modify L and NPROC in ../src/openqxd-devel/include/global.h
# compile again: make check1
# make sure that configuration specified in check.in is available
mkdir log
mpirun -np <N> check1 -i check.in # on regular linux
srun ... # via slurm
```
