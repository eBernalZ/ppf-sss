"""
Obtain minimum and maximum.
"""

import numpy as np

def obtainMinMax(problem, m):
    """Returns ideal and nadir vectors of the Pareto front for a given problem"""
    if problem in ['DTLZ1']:
        zmin = np.zeros(m)
        zmax = np.ones(m)*(0.5)
    elif problem in ['DTLZ1_MINUS']:
        zmin = np.ones(m)*(-5.511507e+02)
        zmax = np.zeros(m)
    elif problem in ['DTLZ2']:
        zmin = np.zeros(m)
        zmax = np.ones(m)
    elif problem in ['DTLZ2_MINUS']:
        zmin = np.ones(m)*(-3.5)
        zmax = np.zeros(m)
    elif problem in ['DTLZ7']:
        zmin = np.zeros(m-1)
        zmax = np.append(np.ones(m-1)*(0.859401), 2*m)
        if m == 3:
            zmin = np.append(zmin, 2.614009)
        elif m == 5:
            zmin = np.append(zmin, 3.228017)
        elif m == 8:
            zmin = np.append(zmin, 4.149031)
        elif m == 10:
            zmin = np.append(zmin, 4.763039)
    elif problem in ['WFG1', 'WFG2']:
        zmin = np.zeros(m)
        zmax = np.arange(2.0, 2*m+1, 2)
    elif problem in ['WFG1_MINUS']:
        zmin = np.arange(-3.0, -2*m-2, -2)
        zmax = np.ones(m)*(-1)
    elif problem in ['Soldado']:
        zmin = np.array([-1.8705, -2.3141, -1.0])
        zmax = np.array([2.3623, 2.2071, 9.85])
    return zmin, zmax
