# QUDA compile manual
This repository aims to help compiling [openQxD](https://gitlab.com/rcstar/openQxD-devel) against [QUDA](https://github.com/lattice/quda).

## Inital setup

### Git clone with HTTPS
```bash
# Clone this repo
git clone https://github.com/chaoos/openqxd_quda_build.git

cd openqxd_quda_build
# Clone the repos of openqxd and quda into src/
git clone -b feature/quda/main-thesis-release https://gitlab.com/rcstar/openQxD-devel.git src/openQxD-devel
git clone -b feature/openqxd-thesis-release https://github.com/chaoos/quda.git src/quda
```

### Or git clone with SSH
```bash
# Clone this repo
git clone git@github.com:chaoos/openqxd_quda_build.git

cd openqxd_quda_build
# Clone the repos of openqxd and quda into src/
git clone -b feature/quda/main-thesis-release git@gitlab.com:rcstar/openQxD-devel.git src/openQxD-devel

git clone -b feature/openqxd-thesis-release git@github.com:chaoos/quda.git src/quda
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
 # example path
export CUDA_HOME=usr/local/cuda-11.6
export CUDACXX=/usr/local/cuda-11.6/bin/nvcc
export CUDA_BIN_PATH=/usr/local/cuda-11.6/bin
```

Set the environment variables:

```bash
# For MPI (e.g. openmpi):
export MPI_HOME="/usr/lib/x86_64-linux-gnu/openmpi/" # for example
export MPI_INCLUDE="${MPI_HOME}/include"
export PATH=/usr/lib/x86_64-linux-gnu/openmpi/bin:${PATH}
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/openmpi/lib:${LD_LIBRARY_PATH}
```
```bash
# For QUDA-OpenQxD compilation:
export GCC=gcc-9
export CC=mpicc
export CXX=mpicxx
```

## Environment on Yoshi

On `yoshi.ethz.ch`, add the following lines in `01-work/Makefile`:

```bash
CMAKE_FLAGS += -DCMAKE_C_COMPILER=/usr/bin/gcc-9
CMAKE_FLAGS += -DCMAKE_CXX_COMPILER=/usr/bin/g++-9
CMAKE_FLAGS += -DCMAKE_Fortran_COMPILER=/usr/bin/gfortran-9
```

Download cmake v3.24 if not available (quda needs exactly this version!)

```bash
wget -P deps/ https://cmake.org/files/v3.24/cmake-3.24.2-linux-x86_64.tar.gz
tar xfs deps/cmake-3.24.2-linux-x86_64.tar.gz -C deps/
rm deps/cmake-3.24.2-linux-x86_64.tar.gz

# add the new cmake version to the PATH
export PATH=$(realpath deps/cmake-3.24.2-linux-x86_64/bin/):$PATH

# add the new cmake version to the PATH via .bashrc
echo "export PATH=[...]/cmake-3.24.2-linux-x86_64/bin/:$PATH" >> ~/.bashrc
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
export GCC=cc
export MPI_HOME="${CRAY_MPICH_DIR}"
export MPI_INCLUDE="${MPI_HOME}/include"
export PATH="${HOME}/openqxd_quda_build/deps/cmake-3.24.2-linux-x86_64/bin/":$PATH
export LD_LIBRARY_PATH="${HOME}/openqxd_quda_build/build/lib":$LD_LIBRARY_PATH
```

And change `01-work/Makefile`:

```Makefile
CMAKE_FLAGS += -DCMAKE_C_COMPILER=cc
CMAKE_FLAGS += -DCMAKE_CXX_COMPILER=CC
CMAKE_FLAGS += -DCMAKE_Fortran_COMPILER=ftn
```

Check the environment:

```bash
cmake --version # should be 3.24 now
nvcc --version
ninja --version # not strictly necessary, see below
gcc --version # should be gcc version 9.x
```

## Compiling

Compile QUDA in the `01-work` directory:

```bash
cd 01-work
make quda # or "make quda_make" or "make quda_ninja"
# Add quda library (libquda.so) to LD_LIBRARY_PATH for the dynamic linker to find it
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$(realpath ../build/lib)
```

Compile OpenQxD programs
```bash
make check1 # this build check1 in openqxd and links it against quda dynamically
make check2
```

Verify dynamic linker works correctly with

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
mkdir log # if [...]/01-work/log does not exist
mpirun -np <N> check1 -i check.in # on regular linux
srun ... # via slurm on daint
```

## Save tune parameters

In order to cache the tune parameters you should set

```bash
export QUDA_RESOURCE_PATH=.
```

This will save the parameters to `tsv` files. When recompiling QUDA, you should
delete these `tsv`files, otherwise QUDA will crash at run-time.

## Profiler

Make sure to have `nsys` installed (e.g. yoshi.ethz.ch has it installed). Then run for example

```bash
mpirun -np 2 nsys profile -o profiler_check3_rank%q{OMPI_COMM_WORLD_RANK} ./check3 -i check.in
```

This will create two files `profiler0.nsys-rep` and `profiler1.nsys-rep`. Download them to your 
local laptop, and install [Nsight Systems 2023](https://developer.nvidia.com/gameworksdownload#?dn=nsight-systems-2023-3).
Note that you need to register at Nvidia in order to download the program. In order to
obtain named regions, run

```bash
# obtain named regions
export NSYS_NVTX_PROFILER_REGISTER_ONLY=0
mpirun -np 2 nsys profile --sample=none --trace=cuda,nvtx,mpi -o profiler_nvtx%q{OMPI_COMM_WORLD_RANK} ./check3 -i check.in
```

