This repository aims to help compiling [openQxD](https://gitlab.com/rcstar/openQxD-devel) against [QUDA](https://github.com/lattice/quda).

# QUDA compile manual

```bash
git clone <TODO>

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

Check for binaries:

```bash
cmake --version # should be 3.24 now
nvcc --version
ninja --version
```

In work dir:

```bash
cd 01-work
make quda
make check1
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$(realpath ../build/lib)
```

Run checks:

```bash
mpirun -np <N> check1 -i ...
```

## Compilation on daint

TODO
