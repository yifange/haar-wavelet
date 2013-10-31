import numpy as np
import numpy.linalg as la
import math
import scipy.stats.threshold
from scidbpy import interface, SciDBQueryError, SciDBArray

# from scidbpy import interface, SciDBQueryError, SciDBArray

def haar_m(n):
    rows = np.array([[1 / math.sqrt(n)] * n])
    for i in range(n - 1):
        Is = n / (2 ** int(math.log(i + 1, 2)))
        before = ((i + 1)- 2 ** (int(math.log(i + 1, 2)))) * Is
        print "before", before
        after = n - Is - before
        print "after", after
        scale = math.sqrt(Is)
        print rows
        new_row = [[0] * before + [1 / scale] * (Is / 2) + [-1 / scale] * (Is / 2) + [0] * after]
        print new_row
        rows = np.append(rows, new_row, axis=0)
    return rows
def haar_m_to_file(n, path):
    # rows = np.array([[1 / math.sqrt(n)] * n])
    with open(path, "w") as f:
        f.write(" ".join(str(i) for i in ([1 / math.sqrt(n)] * n)))
        f.write("\n")
        for i in range(n - 1):
            Is = n / (2 ** int(math.log(i + 1, 2)))
            before = ((i + 1)- 2 ** (int(math.log(i + 1, 2)))) * Is
            after = n - Is - before
            scale = math.sqrt(Is)
            new_row = [0] * before + [1 / scale] * (Is / 2) + [-1 / scale] * (Is / 2) + [0] * after
            f.write(" ".join(str(i) for i in new_row))
            f.write("\n")
            # rows = np.append(rows, new_row, axis=0)

def scidb_stuff():
    haar = haar_matrix(8)[0]
    sdb_haar = sdb.from_array(haar)

    # if "H" in sdb.list_arrays():
    #     sdb.query("remove(H)")
    # q = "rename(" + sdb_haar.name + ", H)"
    # print q
    # sdb.query(q)

def threshold(m, thres=0.00001):
    return sp.stats.threshold(m, threshmin=thres)
def haar_matrix_2(n):
    level = int(math.log(n, 2))

    h = np.array([1], dtype="double")
    nc = 1 / math.sqrt(2)
    lp = np.array([1, 1], dtype="double")
    hp = np.array([1, -1], dtype="double")
    hs = [h]
    for i in range(level):
        lp2 = np.kron(h, lp)
        one_eyed = np.reshape(np.eye(2 ** i), (1, (2 ** i) ** 2))[0]
        hp2 = np.kron(one_eyed, hp)
        print lp2
        print hp2
        h = nc * np.hstack((lp2, hp2))
        hs.append(h)
    h = np.reshape(h, (2 ** level, 2 ** level))
#    coeffs = []
#    for i in reversed(range(level)):
#        h1 = hs[i + 1]
#        h2 = hs[i]
#        d = h2.shape[0]
#        h22 = np.vstack((np.hstack((h2, np.zeros((d, d)))), np.hstack((np.zeros((d, d)), np.eye(d)))))
#        coeffs.append(h22.I * h1)
#    return (h, coeffs)
    return h

def haar_matrix(n):
    level = int(math.log(n, 2))

    h = np.array([1], dtype="double")
    nc = 1 / math.sqrt(2)
    lp = np.array([1, 1], dtype="double")
    hp = np.array([1, -1], dtype="double")
    hs = [h]
    for i in range(level):
        h = nc * np.vstack((np.kron(h, lp), np.kron(np.eye(2 ** i, 2 ** i), hp)))
        h = np.reshape(h, (2 ** (i + 1), 2 ** (i + 1)))
        hs.append(h)
#    coeffs = []
#    for i in reversed(range(level)):
#        h1 = hs[i + 1]
#        h2 = hs[i]
#        d = h2.shape[0]
#        h22 = np.vstack((np.hstack((h2, np.zeros((d, d)))), np.hstack((np.zeros((d, d)), np.eye(d)))))
#        coeffs.append(h22.I * h1)
#    return (h, coeffs)
    return h

def thresholding(n):
    pass

if __name__ == "__main__":
    sdb = interface.SciDBShimInterface("http://localhost:8080")

