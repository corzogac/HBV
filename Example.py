#%%
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
import pandas as pd

#%%
Df=pd.read_excel('Bagmati.xlsx',index_col=0,parse_dates=True)
Df.head()
#%%
Q=Df["Qobs"].to_numpy()
Epot=Df["Epot"].to_numpy()
P=Df["P"].to_numpy()
T=Df["Temp"].to_numpy()


#%%
# For calibration is used percentage 'per' of data
per = 0.2
per = int(np.round(per*len(P)))
Prec = P[1:per]
Temp = T[1:per]
Flow = Q[1:per]
ET = Epot[1:per]
LTAT = np.mean(Temp[1:per])*np.ones((len(Flow),1))
AREA = 2900



#%%
#Parameter selection (initial guess)
p1 = [1,2,1,3,50,1,0.15,0.4,0.04,0.1,0.5,1.2,0.1,0.8,0.05,3.5,1,1] # parameters to be calibrated

#%%
v = [Prec[0], Temp[0], ET[0], LTAT[0]]
St = 50*np.ones(5) # Soil, Uz, Lz, Snow, SnowWC State initialisation
QNew = np.zeros((len(Q),1))
#%%
from HBV import *
Qnew,St2=HBV(p1,v,St)

#%%




#%%
#OPTOPT = optimset('Algorithm','interior-point')
#  Calibration
LB = [-1,0,0,1,50,0.6,0,0,0,0,0,0,0.001,0.01,0,0,0.6,0.6]
UB = [2,3,2,5,500,1.4,5,1,1,1,1,1.5,0.1,1,4,5,1.4,1.4]

#disp('Calibration Started')
#solCal = GODLIKE(@HBV_Wrapper,100,LB,UB)
print('Calibration Done, NSE value')
#NSECal = -HBV_Wrapper(solCal)
#FlowCal = QNew
# %%
