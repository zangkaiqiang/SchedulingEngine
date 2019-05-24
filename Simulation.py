import numpy as np
import scipy.optimize as sco


def fun_linear(x, flag):
    return (x[0] + 2 * x[1]) * flag


cons = ({'type': 'ineq', 'fun': lambda x: -x[0] + 2},
        {'type': 'ineq', 'fun': lambda x: -x[1] + 2},
        {'type': 'ineq', 'fun': lambda x: x[0] + x[1] - 2}
        )
flags = [-1, 1]
for flag in flags:
    opt = sco.minimize(fun=fun_linear, x0=[1, 1], args=(flag,), constraints=cons)
    print(opt['fun']*flag)
