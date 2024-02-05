# TODO

## Gauge field indexing

- [x] All reordering of gauge fields in reorder_openqcd_to_quda() in quda_utils.c
- [x] Only have generic lexicographical ordering in OpenQCDOrder in gauge_field_order.h
- [x] All reordering of gauge fields in OpenQCDOrder in QUDA (what about communication?)
- [x] Gauge field spacetime index solved
- [x] Gauge field Dirac index solved
- [x] Gauge field color (row) index solved
- [x] Gauge field color (column) index solved

## Spinor field indexing

- [x] All reordering of spinor field in reorder_spinor_openqcd_to_quda() in quda_utils.c
- [x] Generic load() and save() in color_spinor_field_order.h (in the same way as in OpenQCDOrder in gauge_field_order.h)
- [x] All reordering of spinor fields in OpenQCDDiracOrder in QUDA
- [x] Check norm_square of a random spinor
- [x] Calculate and compare gamma5 |psi>, with psi random
- [x] Calculate and compare gamma0 |psi>, with psi random
- [x] Calculate and compare gamma1 |psi>, with psi random
- [x] Calculate and compare gamma2 |psi>, with psi random
- [x] Calculate and compare gamma3 |psi>, with psi random
- [x] Spinor field spacetime index solved (untested)
- [x] Spinor field spin index solved
- [x] Spinor field color index solved

## Dirac operator

- [x] Wilson-Dirac operator without Clover-term on a random spinor field
- [x] Wilson-Dirac operator with Clover-term on a random spinor field
- [ ] Wilson-Dirac operator with twisted mass mu!=0.0 on a random spinor field
- [x] Our gamma matrix basis implemented (and working)

### Clover field

- [x] Calculate the clover field on GPU using (already transfered) gauge fields
- [x] Transfer of clover field using `loadCloverQuda()` from host to device (needed once we have QCD+QED, since QED has its own clover term)

## Inverters

- [x] Run GCR on QUDA and compare to via Dw_dble()
- [x] Run other inverter on QUDA and compare to via Dw_dble()
- [ ] Run inverter with multiple RHS on QUDA and compare to via Dw_dble()

## Eigensolvers

- [x] Interface eigensolvers of QUDA

## Misc

- [x] Add input file to repo
- [x] Pure function that does what `ipt[]` does, see `ipt_function()`
- [x] Merge most recent openQxD master branch
- [x] Go back to std=c89
- [x] Merge most recent QUDA development branch into ours
- [ ] Send pull request to QUDA
- [ ] Multiple solver handles at the same time
- [ ] Print solver parameters
- [ ] ifdef in `read_solver_parms()`, `print_solver_params()`
- [ ] `extras/main/lowrank/pbp.c`
- [ ] `check_solver_params()`
- [ ] `write_solver_params()`
- [ ] `get_gfld_flags()` to check gauge field version
- [x] Reduced format for the gauge fields in `check{1..4}`, ie. `QUDA_RECONSTRUCT_8/12` for SU(3) fields
- [ ] Reduced format for the gauge fields in `check{1..4}`, ie. `QUDA_RECONSTRUCT_9/13` for U(3) fields


## Gamma Basis

DeGrand-Rossi basis seems to be this: https://backend.mhpc.sissa.it/sites/default/files/2021-02/PeterLabus.pdf (page 16)


## Questions

* How to find target architecture from command line (like the `sm_60` string for example)?
* What is the difference between `QUDA_MASS_NORMALIZATION` and `QUDA_KAPPA_NORMALIZATION`? It only works with the former.
* What is difference between all the `QudaSolutionType`? And why is `MatQuda` dependent on them? It's not solving a system.
* What is `QudaSiteSubset`? `QUDA_PARITY_SITE_SUBSET`, `QUDA_FULL_SITE_SUBSET`?
* In `color_spinor_field.h`, we have 

```cpp
else if (inv_param.dirac_order == QUDA_OPENQCD_DIRAC_ORDER) {
  fieldOrder = QUDA_OPENQCD_FIELD_ORDER;
  siteOrder = QUDA_EVEN_ODD_SITE_ORDER;
}
```

What effect has `siteOrder`? Since I reversed the openQCD order and made it lexicographical (xyzt)?
* What is the difference between `QudaDiracFieldOrder` (`QUDA_OPENQCD_DIRAC_ORDER`) and `QudaFieldOrder` (`QUDA_OPENQCD_FIELD_ORDER`) and `QudaSiteOrder`?
* How does QUDA want to have the clover fields?
* I disabled all Dirac operators from compiling except for Wilson and Clover. Even though I see compilations of eq:
```
[ 76%] Building CUDA object lib/CMakeFiles/quda.dir/dslash_domain_wall_4d_m5inv.cu.o
...
```

## Answered
* What does `invertQuda()` actually solve? Dslash or Mat? With or without Clover term?
* What is `QudaInvertParam.reliable_delta`? Used in GCR

* How to impose periodic BCs for the gauge field and anti-periodic for the fermion field (in time-direction)? `QudaGaugeParam.t_boundary = QUDA_PERIODIC_T;` seems to have no effect.
    Answer: By default, QUDA implements anti-periodic boundary conditions in time direction for fermions.
* Somehow our Dirac operator (definition see https://gitlab.com/rcstar/openQxD-devel/-/raw/master/doc/openQCD-1.6/dirac.pdf?ref_type=heads&inline=true eq. 2.6) and `MatQuda()` differ by a global minus sign and 2 gamma^5, why? Answer: You can set a parameter `QUDA_DAG_NO` to get the undaggered Dirac operator.
* Why does `MatQuda()`, `dslashQuda()` take a parameter of type QudaInvertParam?

* What's the intended way to apply gamma matrices to spinors? Answer: See `ApplyGamma` in `quda/lib/dslash_gamma_helper.cu`.
* `D_openQCD = - gamma^5 MatQuda gamma^5 = - MatQuda^dagger`. Is this because of the different gamma-matrix convention?
* What is the difference between `dslashQuda` and `MatQuda`? And which one is inverted when calling `invertQuda`? `dslashQuda` applies the hopping part, `MatQuda` the Dirac operator.

* In the Dirac operator of quda, how are gamma matrices applied and in which convention?
* What's the definition of the sw-term in quda?
* Can we calculate the sw-term on quda side?
* Twisted mass term in quda? Setting `QudaInvertParam.mu` seems to have no effect.



## Tests

Below there is the current state of the checks.

```
D5d = 48x24x24x24, bc=3, cstar=0, QCD-only
A5  = 64x32x32x32, bc=3, cstar=0, QCD-only
QxD = 64x32x32x32, bc=3, cstar=3, QCD+QED
```


### `check1.c`

| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check1.c` | 1x1x1x1 | GPU | D5d | |
| `check1.c` | 1x1x1x1 | CPU | D5d | |
| `check1.c` | 2x1x1x1 | GPU | D5d | |
| `check1.c` | 2x1x1x1 | CPU | D5d | |
| `check1.c` | 1x2x1x1 | GPU | D5d | |
| `check1.c` | 1x2x1x1 | CPU | D5d | |
| `check1.c` | 1x1x2x1 | GPU | D5d | |
| `check1.c` | 1x1x2x1 | CPU | D5d | |
| `check1.c` | 1x1x1x2 | GPU | D5d | |
| `check1.c` | 1x1x1x2 | CPU | D5d | |
| `check1.c` | 1x2x2x2 | GPU | D5d | ✅ |
| `check1.c` | 1x2x2x2 | CPU | D5d | ✅ |
| `check1.c` | 2x1x2x2 | GPU | D5d | ✅ |
| `check1.c` | 2x1x2x2 | CPU | D5d | ✅ |
| `check1.c` | 2x4x1x1 | GPU | D5d | |
| `check1.c` | 2x4x1x1 | CPU | D5d | |
| `check1.c` | 2x1x4x1 | GPU | D5d | |
| `check1.c` | 2x1x4x1 | CPU | D5d | |
| `check1.c` | 2x1x1x4 | GPU | D5d | |
| `check1.c` | 2x1x1x4 | CPU | D5d | |
| `check1.c` | 8x1x1x1 | GPU | D5d | |
| `check1.c` | 8x1x1x1 | CPU | D5d | |


| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check1.c` | 1x2x2x2 | GPU | A5 | ✅ |
| `check1.c` | 1x2x2x2 | CPU | A5 | ✅ |


| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check1.c` | 1x2x2x2 | GPU | QxD | ✅ |
| `check1.c` | 1x2x2x2 | CPU | QxD | ✅ |


### `check2.c`

| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check2.c` | 1x1x1x1 | GPU | D5d | ✅ |
| `check2.c` | 1x1x1x1 | CPU | D5d | ✅ |
| `check2.c` | 2x1x1x1 | GPU | D5d | ✅ |
| `check2.c` | 2x1x1x1 | CPU | D5d | ✅ |
| `check2.c` | 1x2x1x1 | GPU | D5d | |
| `check2.c` | 1x2x1x1 | CPU | D5d | |
| `check2.c` | 1x1x2x1 | GPU | D5d | |
| `check2.c` | 1x1x2x1 | CPU | D5d | |
| `check2.c` | 1x1x1x2 | GPU | D5d | |
| `check2.c` | 1x1x1x2 | CPU | D5d | |
| `check2.c` | 1x2x2x2 | GPU | D5d | |
| `check2.c` | 1x2x2x2 | CPU | D5d | |
| `check2.c` | 2x1x2x2 | GPU | D5d | ✅ |
| `check2.c` | 2x1x2x2 | CPU | D5d | ✅ |
| `check2.c` | 2x4x1x1 | GPU | D5d | ✅ |
| `check2.c` | 2x4x1x1 | CPU | D5d | ✅ |
| `check2.c` | 2x1x4x1 | GPU | D5d | ✅ |
| `check2.c` | 2x1x4x1 | CPU | D5d | ✅ |
| `check2.c` | 2x1x1x4 | GPU | D5d | ✅ |
| `check2.c` | 2x1x1x4 | CPU | D5d | ✅ |
| `check2.c` | 8x1x1x1 | GPU | D5d | ✅ |
| `check2.c` | 8x1x1x1 | CPU | D5d | ✅ |


| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check2.c` | 1x2x2x2 | GPU | A5 | ✅ |
| `check2.c` | 1x2x2x2 | CPU | A5 | ✅ |


| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check2.c` | 1x2x2x2 | GPU | QxD | ✅ calculate Clover term in QUDA fails (but that's OK) |
| `check2.c` | 1x2x2x2 | CPU | QxD | ✅ calculate Clover term in QUDA fails (but that's OK) |


### `check3.c`

| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check3.c` | 1x2x2x2 | GPU | D5d | ✅ |
| `check3.c` | 1x2x2x2 | CPU | D5d | ✅ |


| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check3.c` | 1x2x2x2 | GPU | A5 | ✅ |
| `check3.c` | 1x2x2x2 | CPU | A5 | ✅ |


| check | process grid | QUDA_REORDER_LOCATION | config | status |
| --- | --- | --- | --- | --- |
| `check3.c` | 1x2x2x2 | GPU | QxD | ✅ |
| `check3.c` | 1x2x2x2 | CPU | QxD | ✅ |


## More Questions

* Can there be a place to put indexing helper functions that are needed in all of `gauge_field_order.h`, `color_spinor_field_order.h`, `clover_field_order.h`, ...? But they are needed only for the openQCD order classes. Else I have to write them 3 times.
* What does the `Bytes()` method mean in these order classes? It seems to have no impact.
* What do these warnings mean?

```
ptxas warning : Local memory used for function '_ZN4quda8Kernel3DINS_12CoarseDslashENS_15DslashCoarseArgILb1ELb1ELb1ELNS_10DslashTypeE2ELi1ELi1EfffLi2ELi32ELb1EEELb0EEENSt9enable_ifIXclsr6deviceE14use_kernel_argIT0_EEEvE4typeES6_', size of stack frame: 120 bytes
```

* How to use eigensolvers to obtain small eigenvalue, vectors?
* How to compile QUDA correctly?
* `QudaGaugeParam.t_boundary` seems to have effect only if reconstruct != QUDA_RECONSTRUCT_NO. Why does the underlying data format have an influence in the temporal boundary conditions?

# Known Issues

* When building openQxD in ISO C90, we have to ignore the following compiler warning about complex types `ISO C90 does not support complex types`. `quda.h` exposes functions with signatures containing `_Complex` as types.
* We had to remove the "-Werror" compiler flag, that treats warnings as errors because of the above.
* P2P communication problem (solved)
* EO-preconditioned Dirac operator not working
