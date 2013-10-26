import numpy as np
import math
def haar_matrix(n):
    level = int(math.log(n, 2))

    h = np.matrix([1])
    nc = 1 / math.sqrt(2)
    lp = np.matrix([1, 1])
    hp = np.matrix([1, -1])
    hs = [h]
    for i in range(level):
        h = nc * np.vstack((np.kron(h, lp), np.kron(np.eye(2 ** i, 2 ** i), hp)))
        h = np.reshape(h, (2 ** (i + 1), 2 ** (i + 1)))
        hs.append(h)
    coeffs = []
    for i in reversed(range(level)):
        h1 = hs[i + 1]
        h2 = hs[i]
        d = h2.shape[0]
        h22 = np.vstack((np.hstack((h2, zeros((d, d)))), np.hstack((zeros((d, d)), eye(d)))))
        coeffs.append(h22.I * h1)
    return (h, coeffs)

def thresholding(n):
    pass
if __name__ == "__main__":
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
