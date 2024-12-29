import sys
import numpy as np

from Public.RunsEnergy import runsEnergy

if __name__ == '__main__':
    if (len(sys.argv) != 7):
        sys.exit('Incorrect number of arguments.')
    ppf = str(sys.argv[1])
    scheme = str(sys.argv[2])
    problem = str(sys.argv[3])
    m = int(sys.argv[4])
    N = int(sys.argv[5])
    runs = int(sys.argv[6])
    fitness = runsEnergy(ppf, scheme, problem, m, N, runs)
    np.savetxt('Results/Evaluations/'+ppf+'_'+scheme+'_'+problem+'_{0:0=2d}D'.format(m)+'_{0:0=4d}N'.format(N)+'.energy', fitness, fmt='%.18e', header=str(len(fitness))+' 1')
