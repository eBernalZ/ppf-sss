import numpy as np
def parse_file(file):
    f = open(file, "r")
    header = f.readline().strip("#").split()
    M = None if len(header) == 2 else int(header[0])
    N = int(header[1]) if M else int(header[0])
    m = int(header[2]) if M else int(header[1])
    if (M):
        set = [[] for i in range(M)]
    else:
        set = np.ndarray((N, m))
    lines = f.readlines()
    for index, line in enumerate(lines):
        line = line.strip().split()
        if (M):
            # set[int(line[0]) - 1].append([float(x) for x in line[1:]])
            set[int(line[0]) - 1].append(np.array([float(x) for x in line[1:]]))
        else:
            # set.append([float(x) for x in line])
            set[index] = np.array([float(x) for x in line])

    f.close()
    return set, N, m, M if M else None

def find_min_max(A):
    set = []
    for i in range(len(A)):
        for j in range(len(A[0])):
            set.append(A[i][j])
    set = np.array(set)
    return np.min(set, axis=0), np.max(set, axis=0)
