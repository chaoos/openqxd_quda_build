# QUDA compile manual
This repository aims to help compiling [openQxD](https://gitlab.com/rcstar/openQxD-devel) against [QUDA](https://github.com/lattice/quda).

## Inital setup

```bash
# Clone this repo
git clone https://github.com/chaoos/openqxd_quda_build.git

# Clone the repos
cd src
git clone -b feature/quda/main-thesis-release https://gitlab.com/rcstar/openQxD-devel.git
git clone -b feature/openqxd-thesis-release https://github.com/fernandezdlg/quda.git

# Download dependencies
cd ../deps
wget https://cmake.org/files/v3.24/cmake-3.24.2-linux-x86_64.tar.gz
tar xfs cmake-3.24.2-linux-x86_64.tar.gz
rm cmake-3.24.2-linux-x86_64.tar.gz

# add the new cmake version to the PATH
export PATH=$(realpath cmake-3.24.2-linux-x86_64/bin/):$PATH
```

## Environment on linux

Make sure that these are available

```bash
cmake --version # should be 3.24 now
nvcc --version
ninja --version # not strictly necessary, see below
gcc --version # should be version 9
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

export CC=cc
export CXX=CC
export FC=ftn
```

## Compiling

Then one has to edit

```Makefile
CC=mpicc
```

to

```Makefile
CC=cc
```

in the Makefile of openqxd and the environment variables:

```bash
export GCC="cc"
export MPI_HOME="${CRAY_MPICH_DIR}"
export MPI_INCLUDE="${MPI_HOME}/include"
```

Then compile the quda and openqxd in the `01-work` directory:

```bash
cd 01-work
make quda_ninja # make quda_make if ninja is not available
make check1
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$(realpath ../build/lib) # for the dynamic linker to find libquda.so
```

## Running binaries


```bash
mpirun -np <N> check1 -i ...
srun ...
```
