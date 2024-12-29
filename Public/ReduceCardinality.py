"""
Reduce cardinality.
"""

import numpy as np
import random
from util import find_min_max
from Public.PairPotentialEnergyKernel import pairPotentialEnergyKernel

def reduceCardinality(A, ppf, scheme, N, dim_N, dim_m, dim_M, distance="euclidean", p_minkowski=None, opt=None):
    """Reduces the cardinality of the Pareto front for a given problem"""
    if scheme == 'inclusion':
        S = fastGreedyInclusionAlgorithm(A, N, ppf, distance, p_minkowski, dim_N, dim_m, dim_M)
    elif scheme == 'rand_inclusion':
        S = randomizedGreedyInclusionAlgorithm(A, N, ppf, distance, p_minkowski, opt, dim_N, dim_m, dim_M)
    elif scheme == 'removal':
        S = fastGreedyRemovalAlgorithm(A, N, ppf, distance, p_minkowski, dim_N, dim_m, dim_M)
    elif scheme == 'rand_removal':
        S = randomizedGreedyRemovalAlgorithm(A, N, ppf, distance, p_minkowski, opt, dim_N, dim_m, dim_M)
    elif scheme == 'ITEseq':
        S = fastSequentialIterativeGreedyRemovalAlgorithm(A, N, ppf, distance, p_minkowski, dim_N, dim_m, dim_M)
    elif scheme == 'iterative':
        S = fastRandomizedIterativeGreedyRemovalAlgorithm(A, N, ppf, distance, p_minkowski, opt, dim_N, dim_m, dim_M)
    return S

def fastGreedyInclusionAlgorithm(A, N, ppf, distance, p_minkowski, dim_N, dim_m, dim_M):
    """Selects N solutions from A using the fast greedy inclusion algorithm"""
    if len(A) <= N:
        S = np.copy(A)
    else:
        if dim_M is not None:
            zmin, zmax = find_min_max(A)
        else:
            zmin = np.min(A, axis=0)
            zmax = np.max(A, axis=0)
        denom = zmax-zmin
        denom[denom == 0] = 1e-12

        if dim_M is not None:
            Aprime = [0 for i in range(dim_M)]
            for i in range(dim_M):
                Aprime[i] = (A[i]-zmin)/denom
        else:
            Aprime = (A-zmin)/denom
        extreme = extremeSolution(Aprime, dim_N, dim_m, dim_M)
        selected = [extreme]
        candidates = np.setdiff1d(np.arange(0, len(A)), extreme)
        Memo = pairPotentialEnergyKernel([Aprime[x] for x in candidates], ppf, dim_m=dim_m, A2=Aprime[extreme], distance_type=distance, p_minkowski=p_minkowski)
        while len(selected) < N:
            best = np.argmin(Memo)
            Memo = Memo+pairPotentialEnergyKernel([Aprime[x] for x in candidates], ppf, dim_m=dim_m, A2=Aprime[candidates[best]], distance_type=distance, p_minkowski=p_minkowski)
            Memo = np.delete(Memo, best)
            selected.append(candidates[best])
            candidates = np.delete(candidates, best)
        if dim_M is not None:
            S = [A[i] for i in selected]
        else:
            S = A[selected]
    return S

def randomizedGreedyInclusionAlgorithm(A, N, ppf, distance, p_minkowski, sample_size, dim_N, dim_m, dim_M):
    """Selects N solutions from A using the randomized greedy inclusion algorithm"""
    if len(A) <= N:
        S = np.copy(A)
    else:
        zmin = np.min(A, axis=0)
        zmax = np.max(A, axis=0)
        denom = zmax-zmin
        denom[denom == 0] = 1e-12
        Aprime = (A-zmin)/denom
        extreme = extremeSolution(Aprime, dim_N, dim_m, dim_M)
        selected = [extreme]
        candidates = np.setdiff1d(np.arange(0, len(A)), extreme)
        while len(selected) < N:
            sample_size = len(candidates) if sample_size > len(candidates) else sample_size
            idx = np.random.choice(len(candidates), sample_size, replace=False)
            Diss = pairPotentialEnergyKernel(Aprime[selected], ppf, Aprime[candidates[idx]], distance_type=distance, p_minkowski=p_minkowski)
            C = np.sum(Diss, axis=0)
            best = np.argmin(C)
            selected.append(candidates[idx[best]])
            candidates = np.delete(candidates, idx[best])
        S = A[selected]
    return S

def extremeSolution(A, dim_N, dim_m, dim_M):
    """Returns the extreme solution of the first objective function using the achievement scalarizing function"""
    w = np.hstack((1, np.zeros(dim_m-1)))
    w[w<1e-6] = 1e-6
    if dim_M is not None:
        # extremeSolution = np.inf
        # print("dim_M is not None")
        # for i in range(dim_M):
        #     print("A[i]: ", A[i])
        #     asf = np.max(A[i]/w, axis=1)
        #     extremeSolution = min(extremeSolution, np.argmin(asf))
        index = random.randint(0, dim_M-1)
        return index
    else:
        print("dim_M is None")
        asf = np.max(A/w, axis=1)
        extremeSolution = np.argmin(asf)
        print("extremeSolution: ", extremeSolution)
    # asf = np.max(A/w, axis=1)
    # extremeSolution = np.argmin(asf)
    # print("extremeSolution: ", extremeSolution)
        return extremeSolution

def fastGreedyRemovalAlgorithm(A, N, ppf, distance, p_minkowski, dim_N, dim_m, dim_M):
    """Selects N solutions from A using the fast greedy removal algorithm"""
    if len(A) <= N:
        S = np.copy(A)
    else:
        zmin = np.min(A, axis=0)
        zmax = np.max(A, axis=0)
        denom = zmax-zmin
        denom[denom == 0] = 1e-12
        Aprime = (A-zmin)/denom
        Diss = pairPotentialEnergyKernel(Aprime, ppf, distance_type=distance, p_minkowski=p_minkowski)
        selected = np.arange(0, len(A))
        Memo = np.sum(Diss, axis=1)
        while len(selected) > N:
            worst = np.argmax(Memo)
            Memo = Memo-Diss[selected,selected[worst]]
            Memo = np.delete(Memo, worst)
            selected = np.delete(selected, worst)
        S = A[selected]
    return S

def randomizedGreedyRemovalAlgorithm(A, N, ppf, distance, p_minkowski, sample_size, dim_N, dim_m, dim_M):
    """Selects N solutions from A using the randomized greedy removal algorithm"""
    if len(A) <= N:
        S = np.copy(A)
    else:
        zmin = np.min(A, axis=0)
        zmax = np.max(A, axis=0)
        denom = zmax-zmin
        denom[denom == 0] = 1e-12
        Aprime = (A-zmin)/denom
        selected = np.arange(0, len(A))
        while len(selected) > N:
            sample_size = len(selected) if sample_size > len(selected) else sample_size
            idx = np.random.choice(len(selected), sample_size, replace=False)
            Diss = pairPotentialEnergyKernel(Aprime[selected[idx]], ppf, distance_type=distance, p_minkowski=p_minkowski)
            C = np.sum(Diss, axis=1)
            worst = np.argmax(C)
            selected = np.delete(selected, idx[worst])
        S = A[selected]
    return S

def fastSequentialIterativeGreedyRemovalAlgorithm(A, N, ppf, distance, p_minkowski, dim_N, dim_m, dim_M):
    """Selects N solutions from A using the fast sequential iterative greedy removal algorithm"""
    if len(A) <= N:
        S = np.copy(A)
    else:
        np.random.shuffle(A)
        zmin = np.min(A, axis=0)
        zmax = np.max(A, axis=0)
        denom = zmax-zmin
        denom[denom == 0] = 1e-12
        Aprime = (A-zmin)/denom
        selected = np.arange(0, N)
        candidates = np.arange(N, len(A))
        Diss = pairPotentialEnergyKernel(Aprime[selected], ppf, distance_type=distance, p_minkowski=p_minkowski)
        memo = np.sum(Diss, axis=1)
        for candidate in candidates:
            diss = pairPotentialEnergyKernel(Aprime[selected], ppf, Aprime[candidate], distance_type=distance, p_minkowski=p_minkowski)
            memo = memo+diss
            cnew = np.sum(diss)
            worst = np.argmax(np.append(memo, cnew))
            if worst == len(memo):
                memo = memo-diss
            else:
                memo = memo-Diss[:,worst]
                selected[worst] = candidate
                memo[worst] = cnew-diss[worst]
                diss[worst] = 0
                Diss[:,worst] = diss
                Diss[worst,:] = diss
        S = A[selected]
    return S

def fastRandomizedIterativeGreedyRemovalAlgorithm(A, N, ppf, distance, p_minkowski, cycles, dim_N, dim_m, dim_M):
    """Selects N solutions from A using the fast randomized iterative greedy removal algorithm"""
    if len(A) <= N:
        S = np.copy(A)
    else:
        np.random.shuffle(A)
        zmin = np.min(A, axis=0)
        zmax = np.max(A, axis=0)
        denom = zmax-zmin
        denom[denom == 0] = 1e-12
        Aprime = (A-zmin)/denom
        selected = np.arange(0, N)
        candidates = np.arange(N, len(A))
        Diss = pairPotentialEnergyKernel(Aprime[selected], ppf, distance_type=distance, p_minkowski=p_minkowski)
        memo = np.sum(Diss, axis=1)
        for i in range(0, cycles):
            idx = np.random.randint(0, len(candidates))
            candidate = candidates[idx]
            diss = pairPotentialEnergyKernel(Aprime[selected], ppf, Aprime[candidate], distance_type=distance, p_minkowski=p_minkowski)
            memo = memo+diss
            cnew = np.sum(diss)
            worst = np.argmax(np.append(memo, cnew))
            if worst == len(memo):
                memo = memo-diss
            else:
                candidates[idx] = selected[worst]
                memo = memo-Diss[:,worst]
                selected[worst] = candidate
                memo[worst] = cnew-diss[worst]
                diss[worst] = 0
                Diss[:,worst] = diss
                Diss[worst,:] = diss
        S = A[selected]
    return S
