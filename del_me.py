from numba import cuda
import numpy as np
# import matplotlib.pyplot as plt
from time import time

n = 512
blockdim = 16, 16
griddim = int(n / blockdim[0]), int(n / blockdim[1])

L = 1.
h = L / n
dt = 0.1 * h ** 2
nstp = 5000


@cuda.jit("void(float64[:], float64[:])")
def nextstp_gpu(u0, u):
    i, j = cuda.grid(2)

    u00 = u0[i + n * j]
    if i > 0:
        uim1 = u0[i - 1 + n * j]
    else:
        uim1 = 0.
    if i < n - 1:
        uip1 = u0[i + 1 + n * j]
    else:
        uip1 = 0.
    if j > 0:
        ujm1 = u0[i + n * (j - 1)]
    else:
        ujm1 = 0.
    if j < n - 1:
        ujp1 = u0[i + n * (j + 1)]
    else:
        ujp1 = 1.

    d2x = (uim1 - 2. * u00 + uip1)
    d2y = (ujm1 - 2. * u00 + ujp1)
    u[i + n * j] = u00 + (dt / h / h) * (d2x + d2y)


u0 = np.full(n * n, 0., dtype=np.float64)
u = np.full(n * n, 0., dtype=np.float64)

st = time()

d_u0 = cuda.to_device(u0)
d_u = cuda.to_device(u)
for i in xrange(0, int(nstp / 2)):
    nextstp_gpu[griddim, blockdim](d_u0, d_u)
    nextstp_gpu[griddim, blockdim](d_u, d_u0)

cuda.synchronize()
u0 = d_u0.copy_to_host()
print('time on GPU = ', time() - st)