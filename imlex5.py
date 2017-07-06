import numpy as np


def c(x):
    if x == 0 or x == 1:
        return 0
    return -x * np.log2(x) - (1 - x) * np.log2(1 - x)


result = c(0.5) - ((3/4)*c(2/3) + 0.25*c(0))
print(result)
r2 = c(0.5) - (0.5*c(0.5) +0.5*c(0.5))
print(r2)
print(np.log2(2))