import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
import pandas as pd

#%%
Df=pd.read_excel('Bagmati.xlsx',index_col=0,parse_dates=True)
Df.head()
Qo=Df["Qobs"].to_numpy()
Epot=Df["Epot"].to_numpy()
P=Df["P"].to_numpy()
T=Df["Temp"].to_numpy()
LTAT = np.mean(T)*np.ones(len(Qo))
AREA = 2900
#%%
#Parameter selection (initial guess)
p1 = [1,2,1,3,50,1,0.15,0.4,0.04,0.1,0.5,1.2,0.1,0.8,0.05,3.5,1,1] # parameters to be calibrated
Pos=200 #45,0,200 
v = [P[Pos], T[Pos], Epot[Pos], LTAT[Pos]]
St = [0,10,50,50,0] # SP,SMOld, Uz, Lz, SWC



# %%
from Snow import *
SP = St[0] # Snow Pack
WC = St[4] # Water Content in Snow Pack
SP2,WC,insoil,snow=SnowRoutine(p1,P[Pos],T[Pos],SP,WC,TFAC = 1,AREA = 2900)

#%%
from SoilMoisture import *
SMOld = St[1] # Soil Moisture

Re,SM=SoilMoisture(p1,insoil,SMOld)


#%%
#Evapotranspiration
from Evapotranspiration import *

#' If there was snow then put the actual PotE in zero

if snow:
    act_E = 0
else:
    PotE=False
    SM2,Act_E=Evapotranspiration(p1,SM,SMOld,Epot[Pos],PotE)


#%%
from HydrologicalResponse import *

UZ1 = St[2] # Upper Zone
LZ1 = St[3] # Lower Zone

QNew,UZ2,LZ2 =SurfaceFlow(p1,UZ1,LZ1,Re,TFAC = 1,AREA = 2900)


#%% MaxBas or transfer function

#To confirm the slope should be 1/maxbas^2
Qv=MAXBAS(QNew,10)
plt.plot(Qv)




#%%
from pymoo.algorithms.soo.nonconvex.pattern_search import PatternSearch
from pymoo.factory import Himmelblau
from pymoo.optimize import minimize


problem = Himmelblau()

algorithm = PatternSearch()

res = minimize(problem,
               algorithm,
               verbose=True,
               seed=1)

print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
# %%
