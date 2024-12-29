"""
Pair-potential energy kernels.
"""

import numpy as np
from scipy.spatial import distance

def pairPotentialEnergyKernel(A1, ppf, dim_m, A2=None, distance_type="euclidean", p_minkowski=None):
    """Calculates dissimilarity matrix or vector using a given pair-potential kernel"""
    if ppf == 'RSE':
        d = RSE(A1, A2, dim_m+1, distance_type, p_minkowski)
    elif ppf == 'GAE':
        d = GAE(A1, A2, 512, distance_type, p_minkowski)
    elif ppf == 'COU':
        d = COU(A1, A2, distance_type, p_minkowski)
    elif ppf == 'PTP':
        d = PTP(A1, A2, 5, 3, 0.02, distance_type, p_minkowski)
    elif ppf == 'MPT':
        d = MPT(A1, A2, 1, 25, distance_type, p_minkowski)
    elif ppf == 'KRA':
        d = KRA(A1, A2, 5, 3, 0.02, distance_type, p_minkowski)
    if A2 is None:
        return distance.squareform(d, distance_type, p_minkowski)
    else:
        return d

def RSE(A1, A2, s, distance_type="euclidean", p_minkowski=None):
    """Calculates dissimilarity matrix or vector using the Riesz s-energy kernel"""
    # print("A1: ", A1)
    # print("A2: ", A2)
    if distance_type == "minkowski":
        d = calculateDistance(A1, A2, distance_type, p_minkowski)
    else:
        d = calculateDistance(A1, A2, distance_type)
    denom = d**s
    denom[denom == 0] = 1e-12
    return 1/denom

def GAE(A1, A2, alpha, distance_type="euclidean", p_minkowski=None):
    """Returns dissimilarity matrix using the Gaussian alpha-energy kernel"""
    if distance_type == "minkowski":
        d = calculateDistance(A1, A2, distance_type, p_minkowski)
    else:
        d = calculateDistance(A1, A2, distance_type)
    return np.e**(-alpha*(d**2))

def COU(A1, A2, distance_type="euclidean", p_minkowski=None):
    """Returns dissimilarity matrix using the Coulomb's law kernel"""
    k = 1/(4*np.pi*8.854e-12)
    norm1 = np.linalg.norm(A1, axis=1)
    if A2 is None:
        V = np.outer(norm1, norm1)
        np.fill_diagonal(V, 0)
        v = distance.squareform(V)
    else:
        if A2.ndim == 1:
            norm2 = np.linalg.norm(A2)
            v = norm1*norm2
        else:
            norm2 = np.linalg.norm(A2, axis=1)
            v = np.outer(norm1, norm2)
    if distance_type == "minkowski":
        d = calculateDistance(A1, A2, distance_type, p_minkowski)
    else:
        d = calculateDistance(A1, A2, distance_type)
    denom = d**2
    denom[denom == 0] = 1e-12
    d = k*v/denom
    return d

def PTP(A1, A2, V1, V2, alpha, distance_type="euclidean", p_minkowski=None):
    """Returns dissimilarity matrix using the Pösch-Teller potential kernel"""
    if distance_type == "minkowski":
        d = calculateDistance(A1, A2, distance_type, p_minkowski)
    else:
        d = calculateDistance(A1, A2, distance_type)
    denom1 = np.sin(alpha*d)**2
    denom1[denom1 == 0] = 1e-12
    denom2 = np.cos(alpha*d)**2
    denom2[denom2 == 0] = 1e-12
    return V1/denom1+V2/denom2

def MPT(A1, A2, D, alpha, distance_type="euclidean", p_minkowski=None):
    """Returns dissimilarity matrix using the modified Pösch-Teller potential kernel"""
    if distance_type == "minkowski":
        d = calculateDistance(A1, A2, distance_type, p_minkowski)
    else:
        d = calculateDistance(A1, A2, distance_type)
    return D/(np.cosh(alpha*d)**2)

def KRA(A1, A2, V1, V2, alpha, distance_type="euclidean", p_minkowski=None):
    """Returns dissimilarity matrix using the Kratzer potential kernel"""
    if distance_type == "minkowski":
        d = calculateDistance(A1, A2, distance_type, p_minkowski)
    else:
        d = calculateDistance(A1, A2, distance_type)
    denom = np.copy(d)
    denom[denom == 0] = 1e-12
    return V1*(((d-(1/alpha))/denom)**2)+V2

def calculateDistance(A1, A2, distance_type="euclidean", p_minkowski=None):
    """Calculates dissimilarity matrix or vector using a given distance metric"""
    if distance_type == "hausdorff":
        d_mat = np.zeros(len(A1))
        for i in range(len(A1)):
            d_mat[i] = distance.directed_hausdorff(A1[i], A2)[0]
        return d_mat
    elif A2 is None:
        if distance_type == "minkowski":
            return distance.pdist(A1, distance_type, p=p_minkowski)
        else:
            return distance.pdist(A1, distance_type)
    else:
        if A2.ndim == 1:
            if distance_type == "minkowski":
                return distance.cdist(A1, A2[np.newaxis], distance_type, p=p_minkowski).flatten()
            else:
                return distance.cdist(A1, A2[np.newaxis], distance_type).flatten()
        else:
            if distance_type == "minkowski":
                return distance.cdist(A1, A2, distance_type, p=p_minkowski)
            else:
                return distance.cdist(A1, A2, distance_type)