# QUDA compile manual
This repository aims to help compiling [openQxD](https://gitlab.com/rcstar/openQxD-devel) against [QUDA](https://github.com/lattice/quda).

## Inital setup

```bash
# Clone this repo
git clone https://github.com/chaoos/openqxd_quda_build.git

cd openqxd_quda_build
# Clone the repos of openqxd and quda into src/
git clone -b feature/quda/main-thesis-release https://gitlab.com/rcstar/openQxD-devel.git src/openQxD-devel
git clone -b feature/openqxd https://github.com/chaoos/quda.git src/quda
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
export GCC="gcc" # use gcc-9 on yoshi
export CC=mpicc
export CXX=mpicxx
export MPI_HOME="/usr/lib/x86_64-linux-gnu/openmpi/" # for example
export MPI_INCLUDE="${MPI_HOME}/include"
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
export GCC="cc"
export CXX=CC
export MPI_HOME="${CRAY_MPICH_DIR}"
export MPI_INCLUDE="${MPI_HOME}/include"
export PATH="~/openqxd_quda_build/deps/cmake-3.24.2-linux-x86_64/bin/":$PATH
export LD_LIBRARY_PATH="~/openqxd_quda_build/build/lib":$LD_LIBRARY_PATH
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

### Note for compiling on Daint

Before executing the `make check1`, `make check2`, ... commands, ensure to modify the compiler settings in the `Makefile` located at `PATH/openqxd_quda_build/src/openQxD-devel/devel/quda/` in the following way: change the lines

```Makefile
CC=mpicc
CLINKER=$(CC)
CXX=mpicxx
```

to 

```Makefile
CC=cc
CLINKER=$(CC)
CXX=cxx
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
mpirun -np 2 nsys profile -o profiler%q{OMPI_COMM_WORLD_RANK} ./check3 -i check.in
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
## Environment on Leonardo:

Setup the environment on Leonardo:

```bash
module load profile/global
module load cmake
module load cuda/12.1
module load gcc/12.2.0
module load openmpi/4.1.6--gcc--12.2.0
module load ninja
```

Set the environment variables:

```bash
export GCC="gcc"
export MPI_HOME="${OPENMPI_HOME}"
export MPI_INCLUDE="${MPI_HOME}/include"
```

Change `01-work/Makefile`:

```bash
CMAKE_FLAGS += -DQUDA_GPU_ARCH=sm_80
CMAKE_FLAGS += -DCMAKE_BUILD_TYPE=STRICT
CMAKE_FLAGS += -DCMAKE_CXX_COMPILER=g++
CMAKE_FLAGS += -DCMAKE_C_COMPILER=gcc
CMAKE_FLAGS += -DMPI_CXX_SKIP_MPICXX=ON
CMAKE_FLAGS += -DCMAKE_CUDA_COMPILER=nvcc
CMAKE_FLAGS +=
-DCUDAToolkit_BIN_DIR=/leonardo/prod/opt/compilers/cuda/12.1/none/bin
CMAKE_FLAGS +=
-DCUDAToolkit_INCLUDE_DIR=/leonardo/prod/opt/compilers/cuda/12.1/none/include
```

The QUDA compilation takes longer than 10 mins. The large production runs are executed in batch mode, see [LEONARDO Booster UserGuide](https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.2.1%3A+LEONARDO+Booster+UserGuide).

This is an example of script file to compile QUDA:

```bash
#!/bin/bash
#SBATCH -A <account_name>
#SBATCH -p boost_usr_prod
#SBATCH --exclusive
#SBATCH --time 00:50:00     # format: HH:MM:SS
#SBATCH -N 1
#SBATCH --ntasks-per-node=1 # 1 tasks out of 32
#SBATCH --gres=gpu:0        # 0 gpus per node out of 4
#SBATCH --job-name=my_batch_job

srun make quda_ninja
```

Note that since compute nodes don't have internet connection, you should

1) guide cmake to a local folder, where eigen3 has been downloaded and unpacked and change `01-work/Makefile` accordingly:

```bash
CMAKE_FLAGS += -DCPM_DOWNLOAD_ALL=OFF
CMAKE_FLAGS += -DQUDA_DOWNLOAD_EIGEN=OFF
CMAKE_FLAGS +=
-DEIGEN_INCLUDE_DIR=realpath ../eigen3
```

2) modify `openqxd_quda_build/src/quda/CMakeLists.txt`

```bash 
# add a directory for cmake modules
...
include(cmake/CPM.cmake)
```

in order to include the folder where CPM.cmake-0.38.7 has been downloaded and unpacked. 

Compile openqxd in the 01-work directory:

Since libraries like libcuda.so and libnvidia-ml.so are only available when one is on a compute node, you can run 
```bash
make check{1,2,3,4} 
```

for example, via salloc 

```bash
salloc -N 1 -t 00:05:00 --ntasks-per-node=1 --gres=gpu:0 -p boost_usr_prod -A<account_name>
```
