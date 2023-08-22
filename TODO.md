# TODO

## Gauge field indexing

* All reordering of gauge field in reorder_openqcd_to_quda() in quda_utils.c
* Only have generic lexicographical ordering in OpenQCDOrder in gauge_field_order.h

## Spinor field indexing

* All reordering of spinor field in reorder_spinor_openqcd_to_quda() in quda_utils.c
* Generic load() and save() in color_spinor_field_order.h (in the same way as in OpenQCDOrder in gauge_field_order.h)
* Check norm_square of a random spinor
* Calculate and compare <psi| gamma |psi>
* Wilso-Dirac operator without Clover-term using unit gauge field

## Misc

* Add input file to repo
