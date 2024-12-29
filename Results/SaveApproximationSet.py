"""
Save approximation set.
"""

import numpy as np
import matplotlib.pyplot as plt

from Public.ObtainMinMax import obtainMinMax

def saveApproximationSet(A, ppf, scheme, problem, distance, run, N, m, M, sample_size=None, p_minkowski=None, mode='save_all'):
    """Draws and saves a given approximation set"""
    if scheme in ["rand_inclusion", "rand_removal", "iterative"]:
        prefix = 'Results/Approximations/'+ppf+'_'+scheme+'_{0:0=4d}S_'.format(sample_size)+problem
    else:
        prefix = 'Results/Approximations/'+ppf+'_'+scheme+'_'+problem

    if distance != "minkowski":
        if M:
            file_name = prefix+'_'+distance+'_{0:0=2d}D'.format(m)+'_{0:0=4d}N'.format(N)+'_{0:0=2d}M'.format(M)+'_R{0:0=2d}'.format(run)
        else:
            file_name = prefix+'_'+distance+'_{0:0=2d}D'.format(m)+'_{0:0=4d}N'.format(N)+'_R{0:0=2d}'.format(run)
    else:
        if M:
            file_name = prefix+'_'+distance+'_{0:.3f}_{1:0=2d}D'.format(p_minkowski, m)+'_{0:0=4d}N'.format(N)+'_{0:0=2d}M'.format(M)+'_R{0:0=2d}'.format(run)
        else:
            file_name = prefix+'_'+distance+'_{0:.3f}_{1:0=2d}D'.format(p_minkowski, m)+'_{0:0=4d}N'.format(N)+'_R{0:0=2d}'.format(run)
      
    # if mode == 'save_txt':
    #     np.savetxt(file_name+'.pof', A, fmt='%.6e', header=str(N)+' '+str(m))
    # else:
    #     zmin, zmax = obtainMinMax(problem, m)
    #     if (m == 2):
    #         plt.scatter(A[:,0], A[:,1], color=(0.7, 0.7, 0.7), edgecolors=(0.4, 0.4, 0.4))
    #         eps = (zmax-zmin)/np.array([25, 20])
    #         plt.xlim([zmin[0]-eps[0], zmax[0]+eps[0]])
    #         plt.ylim([zmin[1]-eps[1], zmax[1]+eps[1]])
    #     elif (m == 3):
    #         fig = plt.figure()
    #         ax = fig.add_subplot(111, projection='3d')
    #         ax.view_init(30, 45)
    #         ax.scatter(A[:,0], A[:,1], A[:,2], color=(0.7, 0.7, 0.7), edgecolors=(0.4, 0.4, 0.4), alpha=1)
    #         ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    #         ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    #         ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    #         ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    #         ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    #         ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    #         ax.xaxis.set_rotate_label(False)
    #         ax.yaxis.set_rotate_label(False)
    #         ax.zaxis.set_rotate_label(False)
    #         eps = (zmax-zmin)/20
    #         ax.set_xlim(zmin[0]-eps[0], zmax[0]+eps[0])
    #         ax.set_ylim(zmin[1]-eps[1], zmax[1]+eps[1])
    #         ax.set_zlim(zmin[2]-eps[2], zmax[2]+eps[2])
    #     else:
    #         for i in range(0, N):
    #             plt.plot(A[i], color=(0.5, 0.5, 0.5))
    #         x = []
    #         labels = []
    #         for i in range(0, m):
    #             x.append(i)
    #             labels.append(str(i+1))
    #         plt.xticks(x, labels)
    #         epsx = (m-1)/25
    #         epsy = (max(zmax)-min(zmin))/20
    #         plt.xlim([-epsx, m-1+epsx])
    #         plt.ylim([min(zmin)-epsy, max(zmax)+epsy])
    # plt.title(ppf+' using '+scheme+' on '+problem+' with '+str(N), fontsize=18)
    # plt.tight_layout()
    # if (mode == 'save_all'):
    #     np.savetxt(file_name+'.pof', A, fmt='%.6e', header=str(N)+' '+str(m))
    #     plt.savefig(file_name+'.png', format='png')
    #     plt.close()
    # elif (mode == 'save_fig'):
    #     plt.savefig(file_name+'.png', format='png')
    #     plt.close()
    # elif (mode == 'plot'):
    #     plt.show()
    #     plt.close()
    return
