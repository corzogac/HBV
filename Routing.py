import numpy as np

#%%
def MAXBAS(Q,MaxBas):
    """_summary_

    Args:
        Q (numpy): array of discharges to be routed
        MaxBas (float): Time of the routing

    Returns:
        Numpy Array: Matrix of discharges in time
    """
    #decimal part
    I=int(np.floor(MaxBas))
    #Integer part
    d=MaxBas-I 
    if d>0:
        plus=1 #addding one step 
    else:
        plus=0

    m=4/(MaxBas**2)
    #going up
    x=np.linspace(0,MaxBas/2,int(np.floor(MaxBas/2)))
    y=m*x
    #going down
    x2=np.linspace(MaxBas/2,MaxBas,int(np.floor(MaxBas/2))+plus)
    y2=y[-1]-m*(x2-MaxBas/2)
    z=np.array([*y,*y2])
    return z*Q


# %%
import matplotlib.pyplot as plt
def PlotMaxBas(max):
    max=10
    m=4/(max**2)
    x=np.linspace(0,max/2,int(np.floor(max/2)))
    y=m*x
    x2=np.linspace(max/2,max,int(np.floor(max/2)))
    y2=y[-1]-m*(x2-max/2)
    plt.plot(x,y)
    plt.plot(x2,y2)

    A=y*max/2  #One so to have mass conservation
    print(f"Area={A}")
# %%
