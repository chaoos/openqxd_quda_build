from global_replacers import *
import os

global_file  = '../src/openQxD-devel/include/global.h'
include_file = '../src/openQxD-devel/main/ym1.in'

local_lattice = [8,8,8,8]
replace_local_lattice(local_lattice, global_file)

for t in range(4):
    for x in range(4):
        for y in range(4):
            for z in range(4):
                np = t + x + y + z
                if np > 3:
                    continue
                
                
                new_name = 'Snoopy_'+str(t)+str(x)+str(y)+str(z)+'_8888'
                
                replace_name(new_name,include_file)
                replace_process_grid([2**t,2**x,2**y,2**z], global_file)
                
                os.system('cd ../src/openQxD-devel/main && make clean && make ym1 && mpirun -np '+str(2**np)+' ./ym1 -i ym1.in')
                
                # os.system('./main')
                # os.wait()
            



