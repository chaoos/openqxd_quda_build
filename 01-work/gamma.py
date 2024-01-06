#! /usr/bin/env python3

import numpy as np
import math as mt
from termcolor import colored

eps = 1e-15
padding = 3

def fmt(x):
    if abs(x.real) <= eps and abs(x.imag) <= eps:
        return f'{0:>{padding}.0f}'
    elif mt.isclose(x.real,1) and abs(x.imag) <= eps:
        return f'{1:>{padding}.0f}'
    elif mt.isclose(x.real,-1) and abs(x.imag) <= eps:
        return f'{-1:>{padding}.0f}'
    elif abs(x.real) <= eps and mt.isclose(x.imag,1):
        return f'{"j":>{padding}}'
    elif abs(x.real) <= eps and mt.isclose(x.imag,-1):
        return f'{"-j":>{padding}}'
    else:
        return f'{x}'

np.set_printoptions(formatter={'complexfloat': fmt})

# gamma matrices
gamma = {
    'openQCD': { # convention of openQCD
        't': np.matrix([[0,0,-1,0],[0,0,0,-1],[-1,0,0,0],[0,-1,0,0]], dtype=np.complex128),
        # 0 0  0 -i
        # 0 0 -i  0
        # 0 i  0  0
        # i 0  0  0
        'x': np.matrix([[0,0,0,-1j],[0,0,-1j,0],[0,1j,0,0],[1j,0,0,0]], dtype=np.complex128),
        'y': np.matrix([[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]], dtype=np.complex128),
        'z': np.matrix([[0,0,-1j,0],[0,0,0,1j],[1j,0,0,0],[0,-1j,0,0]], dtype=np.complex128),
    },
    'quda': { # exactly as it is implemented in color_spinor.h
        't': np.matrix([[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-1]], dtype=np.complex128),
        'x': np.matrix([[0,0,0,1j],[0,0,1j,0],[0,-1j,0,0],[-1j,0,0,0]], dtype=np.complex128),
        'y': np.matrix([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]], dtype=np.complex128),
        'z': np.matrix([[0,0,1j,0],[0,0,0,-1j],[-1j,0,0,0],[0,1j,0,0]], dtype=np.complex128),
    },
}

# gamma matrix basis transformations
transformations = {
    'openQCD': np.matrix([[1,0,1,0],[0,1,0,1],[-1,0,1,0],[0,-1,0,1]], dtype=np.complex128)/np.sqrt(2)
}

gamma5 = {
    'openQCD': lambda t,x,y,z: t @ x @ y @ z,
    'quda':    lambda t,x,y,z: x @ y @ z @ t,
}

def g5(t,x,y,z):
    return t @ x @ y @ z

idx = {
    'openQCD': {'t': 0, 'x': 1, 'y': 2, 'z': 3, 5: 5,},
    'quda':    {'x': 0, 'y': 1, 'z': 2, 't': 3, 5: 5,},
}

def print_2mats(m1, m2):
    margin = 10
    for row1, row2 in zip(m1, m2):
        print(' '.join(map(str, np.array(row1))) + ' '*margin + ' '.join(map(str, np.array(row2))))

ss = {"t": "ᵗ", "x": "ˣ", "y": "ʸ", "z": "ᶻ", 5: "^5", 0: "^0", 1: "¹", 2: "²", 3: "³"}
print(f"in openQCD: ɣ5 is defined as ɣ5 :=  ɣᵗ ɣˣ ɣʸ ɣᶻ               = ɣ0 ɣ1 ɣ2 ɣ3 (txyz)")
print(f"in quda:    ɣ5 is defined as ɣ5 := -ɣᵗ ɣˣ ɣʸ ɣᶻ = ɣˣ ɣʸ ɣᶻ ɣᵗ = ɣ0 ɣ1 ɣ2 ɣ3 (xyzt)")

for prog, val in gamma.items():
    print("-"*50)
    print(f"Gamma matrices in {prog} convention:")
    val[5] = gamma5[prog](**val)
    #val[5] = gamma5[prog](val["t"], val["x"], val["y"], val["z"])
    for d, g in val.items():
        print(f"{d}-direction:\nɣ{ss[d]} = ")
        print(g)

for prog, U in transformations.items():
    print("-"*50)
    print("sqrt(2)*U = ")
    print(np.sqrt(2)*U)
    print("sqrt(2)*U^H = ")
    print(np.sqrt(2)*U.H)
    print(colored("U^H U = id", 'green' if np.allclose(U.H @ U, np.eye(4)) else 'red'))
    print(colored("U U^H = id", 'green' if np.allclose(U @ U.H, np.eye(4)) else 'red'))
    for d in ["t", "x", "y", "z", 5]:
        print(f"Checking if U^H ɣ{ss[d]}_quda U = ɣ{ss[d]}_{prog}"
            f" (U^H ɣ{ss[idx['quda'][d]]}_quda U = ɣ{ss[idx[prog][d]]}_{prog}):")
        gamma1 = U.H @ gamma['quda'][d] @ U
        gamma2 = gamma[prog][d]
        # print(gamma1)
        # print(gamma2)
        print_2mats(gamma1, gamma2)
        test1 = np.allclose(gamma1, gamma2)
        # test2 = np.allclose(gamma1, -gamma2)
        print(f"equality: {colored(test1, 'green' if test1 else 'red')}")
          #  f" (minus: {colored(test2, 'green' if test2 else 'red')})")

