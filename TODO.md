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
- [x] Calculate and compare gamma5 |psi>, with psi random (works with QUDA_DEGRAND_ROSSI_GAMMA_BASIS)
- [ ] Calculate and compare gamma0 |psi>, with psi random
- [ ] Calculate and compare gamma1 |psi>, with psi random
- [ ] Calculate and compare gamma2 |psi>, with psi random
- [ ] Calculate and compare gamma3 |psi>, with psi random
- [ ] Calculate and compare <psi| gamma |psi>, with psi random
- [ ] Wilson-Dirac operator without Clover-term using unit gauge field
- [x] Spinor field spacetime index solved
- [ ] Spinor field spin index solved
- [ ] Spinor field color index solved

## Misc

- [x] Add input file to repo
- [x] Pure function that does what ipt[] does, see ipt_function()


## Gamma Basis

DeGrand-Rossi basis seems to be this: https://backend.mhpc.sissa.it/sites/default/files/2021-02/PeterLabus.pdf (page 16)

