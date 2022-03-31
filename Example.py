import matplotlib.pyplot as plt
import numpy as np
from HBV import *

#Reading data
#read data
Df=pd.read_excel('Bagmati.xlsx',index_col=0,parse_dates=True)
Df.head()
Qo=Df["Qobs"].to_numpy()
Epot=Df["Epot"].to_numpy()
P=Df["P"].to_numpy()
T=Df["Temp"].to_numpy()
LTAT = np.mean(T)*np.ones(len(Qo))
AREA = 2900

#Initial values
SP = 10 # Snow Pack
WC = 10 # Water Content in Snow Pack
SMOld=20 # Initial value of soil moisture, assuming less than half Field Capacity
UZ1 = 20 # Upper Zone
LZ1 = 20 # Lower Zone


#%%

#State Variable
SP = 0 # Initial state Snow Pack
WC = 0 # Initial state Water Content in Snow Pack

SMOld = 20 # Initial state Soil Moisture
UZ1 = 5.6 # Initial State Upper Zone
LZ1 = 24.3 # Initial state Lower Zone

psnow=[self.TT,self.CFMAX,self.SFCF,self.CWH,self.CFR]
psoil=[self.FC,self.BETA]
#Soil moisture percentage in decimal where soil moisture reaches maximum potential evapotranspiration
pEvap=[self.LP]
pRun=[self.K,self.K1,self.ALPHA,self.CFR]
pMaxBas=[self.MaxBas]

p1=[*psnow,*psoil,*pEvap,*pRun,*pMaxBas]


#Looping the time series in the model
for i,P in enumerate(Precipitation):
    State,Q=HBV(State,P,T[i],Evap[i])


#%%
plt.plot(Q)
plt.plot(Qo)

#%%
Xmin=0
Xmax=len(Q)
x=np.linspace(0,
              len(Q),len(Q))
Plot2Axis(x,Prec,Q,"Precipitation","Discharge",Name="HBVRun",xmin=Xmin,xmax=Xmax)

#%%
#Fitness functions
#To calibrate we need a fitness function

def fitness_func(Target,Predicted):
    output = np.sqrt(np.sum((Target-Predicted))**2)
    fitness = output/len(Target)
    return fitness
#%%

fitness_func(Qo,Q)

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



#%% If you want to run for certain percentage of data, you can
# For calibration percentage 'per' could be 70% of data
#per = 0.7
#per = int(np.round(per*len(P)))
Prec = P[1:per]
Temp = T[1:per]
Flow = Qo[1:per]
ET = Epot[1:per]
