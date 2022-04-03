#%%
from HBV import *
A=HBV()
A.sim()
A.r
A.Pl2()
A.Ple()
A.Plp()


#%% Optimization
from scipy import optimize

def ObjF(x):
    x=x[0]+x[1]+x[2]
bounds=[(0,10),(-10,15),(-100,10)]
results = optimize.shgo(ObjF, bounds, n=200, iters=500,sampling_method='sobol')

#%%
import matplotlib.pyplot as plt
plt.plot(A.Qo)
plt.plot(A.Qs)

#%%
import matplotlib.pyplot as plt
plt.plot(A.SPs)
plt.plot(A.ins)

#%%
A.uncertainty()
# %%
plt.plot(A.SMs)

# %%
plt.plot(A.ins-A.P)
# %%
plt.plot(A.Evs)

# %%
