#%%
import numpy as np
import matplotlib.pyplot as plt
#%%
from scipy.stats import qmc

sampler = qmc.Sobol(d=2, scramble=False)
sample = sampler.random_base2(m=3)
# %%
l_bounds = [0, 2]
u_bounds = [10, 5]
qmc.scale(sample, l_bounds, u_bounds)
# %%

def rosen(x):
    """The Rosenbrock function"""
    b=100
    a=1
    return np.sum(b*(x[1]-x[0]**2.0)**2.0 + a*(1-x[0])**2.0)

x=np.array([0.5,0.5])
rosen(x)

#%%

def optimize(func,iter=20,lb=[0, 2],ub= [10, 5]):
    sampler = qmc.Sobol(d=2, scramble=False)
    sample = sampler.random_base2(m=3)
    p1=np.zeros(8)
    for i in range(iter):
        x=qmc.scale(sample, lb, ub)
        for k,j in enumerate(x):
            print(f"Iteration {k}")
            print(f"Array to test {j}")
            p1[k]=func(j)
            print(f"Function is {p1[k]}")
        v=np.argsort(p1)
        print(v)
        lb=x[v[1]]
        ub=x[v[0]]
        
        if lb[0]>ub[0]:
            te=ub[0]
            ub[0]=lb[0]
            lb[0]=te

        if lb[1]>ub[1]:
            te=ub[1]
            ub[1]=lb[1]
            lb[1]=te
        plt.plot(p1)
    return x

optimize(rosen)
# %%
