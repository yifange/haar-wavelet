import numpy as np
import math
def haar_matrix(n):
    level = int(math.log(n, 2))

    H = np.matrix([1])
    NC = 1 / math.sqrt(2)
    LP = np.matrix([1, 1])
    HP = np.matrix([1, -1])
    for i in range(level):
        H = NC * np.vstack((np.kron(H, LP), np.kron(np.eye(2 ** i, 2 ** i), HP)))
        # print "===================== i"
        # print H
        # print "===================== i"
        H = np.reshape(H, (2 ** (i + 1), 2 ** (i + 1)))
    return H

if __name__ == "__main__":
    S = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [8, 7, 6, 5],
                  [4, 3, 2, 1]])
    S = np.ones((8, 8))
    print S
    H = haar_matrix(8)
    print H
    C = H * S * H.I
    print C
    RS = H.I * C * H
    print RS
