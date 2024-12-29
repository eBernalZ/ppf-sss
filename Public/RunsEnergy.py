"""
Runs energy.
"""

import numpy as np

from Public.ObtainMinMax import obtainMinMax
from Public.PairPotentialEnergyKernel import pairPotentialEnergyKernel

def runsEnergy(ppf, scheme, problem, m, N, runs):
    """Evaluates the energy of approximation sets using a given pair-potential kernel"""
    zmin, zmax = obtainMinMax(problem, m)
    energy = []
    for run in range(1, runs+1):
        print('PPF:', ppf, '| Scheme:', scheme, '| Problem:', problem, '| Objectives:', m, '| Cardinality:', N, '| Run:', run)
        A = np.genfromtxt('Results/Approximations/'+ppf+'_'+scheme+'_'+problem+'_{0:0=2d}D'.format(m)+'_{0:0=4d}N'.format(N)+'_R{0:0=2d}'.format(run)+'.pof')
        if A.ndim == 1:
            A = A[np.newaxis]
        Aprime = (A-zmin)/(zmax-zmin)
        Diss = pairPotentialEnergyKernel(Aprime, ppf)
        energy.append(np.sum(Diss))
    return energy
