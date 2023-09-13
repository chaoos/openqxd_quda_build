# TODO

## Gauge field indexing

- [x] All reordering of gauge fields in reorder_openqcd_to_quda() in quda_utils.c
- [x] Only have generic lexicographical ordering in OpenQCDOrder in gauge_field_order.h
- [ ] all reordering of gauge fields in OpenQCDOrder in QUDA (what about communication?)
- [ ] Gauge field spacetime index solved
- [ ] Gauge field Dirac index solved
- [ ] Gauge field color (row) index solved
- [ ] Gauge field color (column) index solved

## Spinor field indexing

- [x] All reordering of spinor field in reorder_spinor_openqcd_to_quda() in quda_utils.c
- [x] Generic load() and save() in color_spinor_field_order.h (in the same way as in OpenQCDOrder in gauge_field_order.h)
- [x] all reordering of spinor fields in OpenQCDDiracOrder in QUDA
- [x] Check norm_square of a random spinor
- [x] Calculate and compare gamma5 |psi>, with psi random
- [x] Calculate and compare gamma0 |psi>, with psi random
- [x] Calculate and compare gamma1 |psi>, with psi random
- [x] Calculate and compare gamma2 |psi>, with psi random
- [x] Calculate and compare gamma3 |psi>, with psi random
- [x] Spinor field spacetime index solved (untested)
- [x] Spinor field spin index solved
- [ ] Spinor field color index solved

## Dirac operator

- [x] Wilson-Dirac operator without Clover-term on a random spinor field
- [x] Wilson-Dirac operator with Clover-term on a random spinor field
- [ ] Wilson-Dirac operator with twisted mass mu!=0.0 on a random spinor field
- [ ] Our gamma matrix basis implemented (and working)

### Clover field

- [x] Calculate the clover field on GPU using (already transfered) gauge fields
- [ ] Transfer of clover field using `loadCloverQuda()` from host to device (needed once we have QCD+QED, since QED has its own clover term)

## Inverters

- [ ] Run CG on QUDA and compare to openQCD CG
- [ ] Run multigrid on QUDA and compare to solution of openQCD

## Misc

- [x] Add input file to repo
- [x] Pure function that does what `ipt[]` does, see `ipt_function()`


## Gamma Basis

DeGrand-Rossi basis seems to be this: https://backend.mhpc.sissa.it/sites/default/files/2021-02/PeterLabus.pdf (page 16)


## Questions

* How to impose periodic BCs for the gauge field and anti-periodic for the fermion field (in time-direction)? `QudaGaugeParam.t_boundary = QUDA_PERIODIC_T;` seems to have no effect.
* Somehow our Dirac operator (definition see https://gitlab.com/rcstar/openQxD-devel/-/raw/master/doc/openQCD-1.6/dirac.pdf?ref_type=heads&inline=true eq. 2.6) and `MatQuda()` differ by a global minus sign and 2 gamma^5, why?
* Why does `MatQuda()`, `dslashQuda()` take a parameter of type QudaInvertParam?
* How to find target architecture from command line (like the `sm_60` string for example)?
* What's the intended way to apply gamma matrices to spinors?
* `D_openQCD = - gamma^5 MatQuda gamma^5 = - D_openQCD^dagger`. Is this because of the different gamma-matrix convention?
* What is the difference between `dslashQuda` and `MatQuda`? And which one is inverted when calling `invertQuda`?
* What is the difference between `QUDA_MASS_NORMALIZATION` and `QUDA_KAPPA_NORMALIZATION`? It only works with the former.
* In the Dirac operator of quda, how are gamma matrices applied and in which convention?
* What's the definition of the sw-term in quda?
* Can we calculate the sw-term on quda side?
* Twisted mass term in quda? Setting `QudaInvertParam.mu` seems to have no effect.
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



