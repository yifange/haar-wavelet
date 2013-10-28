import numpy as np
import numpy.linalg as la
import math

from scidbpy import interface, SciDBQueryError, SciDBArray

def scidb_stuff():
    haar = haar_matrix(8)[0]
    sdb_haar = sdb.from_array(haar)

    # if "H" in sdb.list_arrays():
    #     sdb.query("remove(H)")
    # q = "rename(" + sdb_haar.name + ", H)"
    # print q
    # sdb.query(q)


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
    s = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [8, 7, 6, 5],
                  [4, 3, 2, 1]])
    s = np.ones((8, 8))
    # print S
    h, coeffs = haar_matrix(8)
    # print h
    c = h * s * h.I
    # PRINT c
    rs = h.I * c * h
    # print rs
