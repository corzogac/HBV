#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Snow import *
from SoilMoisture import *
from Evapotranspiration import *
from HydrologicalResponse import *
from Routing import *

#read data
Df=pd.read_excel('../Bagmati.xlsx',index_col=0,parse_dates=True)
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


#Preliminary parameters

#p1 =[1,2,1,3,50,1,0.15,0.4,0.04,0.1,0.5,1.2,0.1,0.8,0.05,3.5,1,1] # parameters to be calibrated
TT = 0    #Limit temperature for rain/snow precipitation
CFMAX = 3    # Degree day factor [measures the temperature variation along the day] 
SFCF = 1     # Rainfal correction factor 
CWH = 0.05     # Maximum amount of water that can be stored in snow pack 
CFR = 0.8     # Refreezing factor 
#For Soil
FC = 50    # Field Capacity=Maximum of soil moisture
BETA = 1.2 # Shape Coefficient - exponential variation of the relationship
LP=0.4   
K = 0.04
K1 = 0.1
ALPHA = 0.5
CF = 0.05  #Capilarity Flux 
PERC = 0.05
MaxBas=10
psnow=[TT,CFMAX,SFCF,CWH,CFR]
psoil=[FC,BETA]
#Soil moisture percentage in decimal where soil moisture reaches maximum potential evapotranspiration
pEvap=[LP]
pRun=[K,K1,ALPHA,CFR]
pMaxBas=[MaxBas]

p1=[*psnow,*psoil,*pEvap,*pRun,*pMaxBas]

#%%
Sn=[]
Wat=[]
Ins=[]
Sm=[]
R=[]
Evap=[]
Qs=[]
Uz=[]
Lz=[]

for i,pr in enumerate(P): 
    SP,WC,insoil,snow=SnowRoutine(p1,pr,T[i],SP,WC,TFAC = 1)
    Re,SM=SoilMoisture(p1,insoil,SMOld)
    
    if snow:
        act_E = 0
    else:
        PotE=True
        SM,act_E=Evapotranspiration(p1,SM,SMOld,Epot[i],PotE)


    QNew,UZ2,LZ2 =SurfaceFlow(p1,UZ1,LZ1,Re,TFAC = 1,AREA = 2900)
    UZ1=UZ2
    LZ1=LZ2
    SMOld=SM
    Sn.append(SP)
    Wat.append(WC)
    Ins.append(insoil)
    Sm.append(SM)
    R.append(Re)
    Evap.append(act_E)
    Qs.append(QNew)
    Uz.append(UZ2)
    Lz.append(LZ2)
    
    
plt.plot(Sn,label="Snow Pack")
plt.plot(Wat,label="Water Content")
plt.plot(Ins,label="Water Infiltrte soil")
plt.legend()

plt.figure(figsize=(8,6))
plt.plot(Sm,label="Soil Moisture")
plt.plot(R,label="Recharge")
plt.legend()

plt.figure(figsize=(8,6))
plt.plot(Uz,label="Uz")
plt.plot(Lz,label="Lz")
plt.legend()

plt.figure(figsize=(8,6))
plt.plot(Qs,label="Qs")
plt.plot(Qo,label="Qo")

# %%
