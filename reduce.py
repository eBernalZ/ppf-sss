import sys
import time
import numpy as np
from Public.ReduceCardinality import reduceCardinality
from Public.SaveApproximationSet import saveApproximationSet
import argparse
from util import parse_file

distances = ['minkowski', 'euclidean', 'seuclidean', 'cityblock', 'chebyshev', 'cosine', 'correlation', 'canberra', 'braycurtis', 'mahalanobis']

message = """
    ***************************************************************************************************************
    python reduce.py PPF algorithm [num_samples] instance dimension subset_size executions distance [p_minkowski]
    
    PPF:\tPair-potential energy.
    \tRSE:\tRiesz s-energy.
    \tCOU:\tCoulomb's law.
    \tGAE:\tGaussian alpha energy.
    \tPTP:\tPöschl-Teller potential.
    \tMPT:\tModified Pöschl-Teller potential.
    \tKRA:\tKratzer potential.
    algorithm:\tGreedy algorithm to be executed.
    \tinclusion:\tFast greedy inclusion algorithm.
    \trand_inclusion:\tRandomized fast greedy inclusion algorithm.
    \tremoval:\tFast greedy removal algorithm.
    \trand_removal:\tRandomized fast greedy removal algorithm.
    \titerative:\tFast iterative greedy removal algorithm.
    [num_samples]:\t *OPTIONAL PARAMETER. Number of samples when using a randomized algorithm.
    [num_sets]:\t *OPTIONAL PARAMETER. Number of point sets in the file (Used to execute with sets of sets)
    instance:\tFile to be processed.
    dimension:\tDimension of the points to be processed.
    subset_size:\tDesired subset size.
    executions:\tNumber of executions.
    distance:\tDistance metric used by the PPFs.
    \teuclidean:\tEuclidean distance.
    \tseuclidean:\tStandardized Euclidean distance.
    \tcityblock:\tCity block (Manhattan) distance.
    \tchebyshev:\tChebyshev distance.
    \tcosine:\tCosine distance.
    \tcorrelation:\tCorrelation distance.
    \tcanberra:\tCanberra distance.
    \tbraycurtis:\tBray-Curtis distance.
    \tmahalanobis:\tMahalanobis distance.
    \tminkowski:\tMinkowski distance.
    [p_minkowski]:\t*OPTIONAL PARAMETER. In case of using Minkowski distance, it is mandatory to set the p value.
    ***************************************************************************************************************
    """

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pair-potential energy')
    parser.add_argument('--PPF', type=str, default='RSE',
                    choices=['RSE', 'COU', 'GAE', 'PTP', 'MPT', 'KRA'],
                    help='PPF to use, [RSE, COU, GAE, PTP, MPT, KRA]')
    parser.add_argument('--algorithm', type=str, default='inclusion',
                    choices=['inclusion', 'rand_inclusion', 'removal', 'rand_removal', 'iterative'],
                    help='Algorithm to use, [inclusion, rand_inclusion, removal, rand_removal, iterative]')
    parser.add_argument('--num_samples', type=int, default=-1)
    parser.add_argument('--num_sets', type=int, default=-1)
    parser.add_argument('--file', type=str, help='File to analyze')
    parser. add_argument('--problem', required=True, type=str, help='Problem to be processed')
    parser.add_argument('--dim', type=int, required=True, help='Dimension of the points to be processed')
    parser.add_argument('--subset_size', type=int, required=True, help='Desired subset size')
    parser.add_argument('--execs', type=int, required=True, help='Number of executions')
    parser.add_argument('--p_minkowski', type=float, help='In case of using Minkowski distance, set the p-value')
    parser.add_argument('--distance', type=str, default='euclidean',
                    choices=['euclidean', 'seuclidean', 'cityblock', 'chebyshev', 'cosine', 'correlation', 'canberra', 'braycurtis', 'mahalanobis', 'minkowski', 'hausdorff'],
                    help='Distance to be used by the PPFs [euclidean, seuclidean, cityblock, chebyshev, cosine, correlation, canberra, braycurtis, mahalanobis, minkowski, hausdorff]')
    args = parser.parse_args()

    if args.distance == 'minkowski' and args.p_minkowski is None:
        parser.error("Minkowski distance requires a p-value.")
    # if len(sys.argv) < 8 or len(sys.argv) > 10: 
    #     print("Syntax error! It is expected 8 or 9 parameters.")   
    #     sys.exit(message)
    # # get ppf type
    # ppf = str(sys.argv[1])
    # if ppf not in ["RSE", "COU", "MPT", "PTP", "KRA", "GAE"]:
    #     sys.exit("Error! Incorrect PPF selection.")
    # # get algorithm type 
    # algorithm_type = str(sys.argv[2])
    # if algorithm_type in ['inclusion', 'removal', 'ITEseq']:
    #     if len(sys.argv) > 9:
    #         print('Incorrect number of arguments for type of algorithm: {0}.'.format(algorithm_type))
    #         sys.exit(message)
    #     problem = str(sys.argv[3])
    #     try:
    #         dimension = int(sys.argv[4])
    #     except ValueError:
    #         sys.exit("Syntax error! The dimension should be a natural number.")
    #     if dimension < 2:
    #         sys.exit("Syntax error! The dimension should be greater or equal than 2.")
    #     try:
    #         subset_size = int(sys.argv[5])
    #     except ValueError:
    #         sys.exit("Syntax error! The subset size should be a natural number.")
    #     if subset_size < 1: 
    #         sys.exit("The subset size should be greater or equal than 1.")
    #     try:
    #         runs = int(sys.argv[6])
    #     except ValueError:
    #         sys.exit("Syntax error! The number of executions should be a natural number.")
    #     if runs < 1:
    #         sys.exit("Syntax error! The number of executions should be greater or equal than 1.")
    #     opt = None
    #     p_minkowski = None
    #     if len(sys.argv) == 8:
    #         if str(sys.argv[7]) != "minkowski":
    #             distance = str(sys.argv[7])
    #             if distance not in distances[1:]:
    #                 sys.exit("Syntax error! Incorrect distance selection.")
    #         else:
    #             sys.exit("Syntax error! Minkowski distance requires the p value.")
    #     elif len(sys.argv) == 9:
    #         distance = str(sys.argv[7])
    #         if distance != "minkowski":
    #             sys.exit("Syntax error! Minkowski distance expected.")
    #         try:
    #             p_minkowski=float(sys.argv[8])
    #         except ValueError:
    #             sys.exit("Syntax error! The p value should be a real number.")
    #         if p_minkowski <= 0:
    #             sys.exit("Syntax error! The p value should be greater than zero.")
    # elif algorithm_type in ['rand_inclusion', 'rand_removal', 'iterative']:
    #     if len(sys.argv) > 10:
    #         sys.exit('Incorrect number of arguments for given algorithm type.')
    #     try:
    #         opt = int(sys.argv[3])
    #     except ValueError:
    #         sys.exit("Syntax error! The number of samples should be a natural number.")
    #     if opt < 1:
    #         sys.exit("Syntax error! The number of samples should be greater or equal than 1.")
    #     problem = str(sys.argv[4])
    #     try:
    #         dimension = int(sys.argv[5])
    #     except ValueError:
    #         sys.exit("Syntax error! The dimension should be a natural number.")
    #     if dimension < 2:
    #         sys.exit("Syntax error! The dimension should be greater or equal than 2.")
    #     try:
    #         subset_size = int(sys.argv[6])
    #     except ValueError:
    #         sys.exit("Syntax error! The subset size should be a natural number.")
    #     if subset_size < 1: 
    #         sys.exit("The subset size should be greater or equal than 1.")
    #     try:
    #         runs = int(sys.argv[7])
    #     except ValueError:
    #         sys.exit("Syntax error! The number of executions should be a natural number.")
    #     if runs < 1:
    #         sys.exit("Syntax error! The number of executions should be greater or equal than 1.")
    #     p_minkowski = None
    #     if len(sys.argv) == 9:
    #         if str(sys.argv[8]) != "minkowski":
    #             distance = str(sys.argv[8])
    #             if distance not in distances[1:]:
    #                 sys.exit("Syntax error! Incorrect distance selection.")
    #         else:
    #             sys.exit("Syntax error! Minkowski distance requires the p value.")
    #     elif len(sys.argv) == 10:
    #         distance = str(sys.argv[8])
    #         if distance != "minkowski":
    #             sys.exit("Syntax error! Minkowski distance expected.")
    #         try:
    #             p_minkowski=float(sys.argv[9])
    #         except ValueError:
    #             sys.exit("Syntax error! The p value should be a real number.")
    #         if p_minkowski <= 0:
    #             sys.exit("Syntax error! The p value should be greater than zero.")
    # else:
    #     sys.exit('Error! Incorrect algorithm type.')

    
    elapsed = []
    for run in range(1, args.execs+1):
        if args.algorithm in ['inclusion', 'removal', 'ITEseq']:
            print('PPF:', args.PPF, '| Scheme:', args.algorithm, '| Problem:', args.file, 
                  '| Objectives:', args.dim, '| Cardinality:', args.subset_size, '| Run:', run)
        elif args.algorithm in ['rand_inclusion', 'rand_removal',]:
            print('PPF:', args.PPF, '| Scheme:', args.algorithm, '| Sample:', args.num_samples, '| Problem:', args.file, 
                  '| Objectives:', args.dim, '| Cardinality:', args.subset_size, '| Run:', run)
        else:
            print('PPF:', args.PPF, '| Scheme:', args.algorithm, '| Cycles:', args.num_samples, '| Problem:', args.file, 
                  '| Objectives:', args.dim, '| Cardinality:', args.subset_size, '| Run:', run)
        # Read data from file
        A, N, m, M = parse_file(args.file)
        start = time.time()
        S = reduceCardinality(A, args.PPF, args.algorithm, args.subset_size, dim_N=N, dim_m=m, dim_M=M, distance=args.distance, p_minkowski=args.p_minkowski, opt=args.num_samples)
        end = time.time()
        # Stop time        
        elapsed.append(end-start)
        saveApproximationSet(S, args.PPF, args.algorithm, args.problem, args.distance, run, N, m, M, mode='save_txt', p_minkowski=args.p_minkowski, sample_size=args.num_samples)
    if args.execs > 1:
        print('Mean execution time:', np.mean(elapsed))
    else:
        print("Execution time:", elapsed[0])


    # if args.algorithm in ["rand_inclusion", "rand_removal", "iterative"]:
    #     prefix = 'Results/Times/'+args.PPF+'_'+args.algorithm+'_{0:0=4d}S_'.format(args.num_samples)+args.file
    # else:
    #     prefix = 'Results/Times/'+args.PPF+'_'+args.algorithm+'_'+args.file

    # if args.distance != "minkowski":
    #     np.savetxt(prefix+'_'+args.distance+'_{0:0=2d}D'.format(args.dim)+'.time', elapsed, fmt='%.18e', header=str(len(elapsed))+' 1')
    # else:
    #     np.savetxt(prefix+'_'+args.distance+'_{0:.3f}_{1:0=2d}D'.format(args.p_minkowski, args.dim)+'.time', elapsed, fmt='%.18e', header=str(len(elapsed))+' 1')

