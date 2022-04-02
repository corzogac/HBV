import pandas as pd
import numpy as np
import os
#def readData(FileName):
print(os.getcwd())
FileName ="func/data/Bagmati.xlsx"
Df=pd.read_excel(FileName,index_col=0,parse_dates=True)
#Df.head()
Qo=Df["Qobs"].to_numpy()
Epot=Df["Epot"].to_numpy()
P=Df["P"].to_numpy()
T=Df["Temp"].to_numpy()
LTAT = np.mean(T)*np.ones(len(Qo))
AREA = 2900
TFAC=1
#
#def load(self):
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

#def ParamerVector():
psnow=[TT,CFMAX,SFCF,CWH,CFR]
psoil=[FC,BETA]
#Soil moisture percentage in decimal where soil moisture reaches maximum potential evapotranspiration
pEvap=[LP]
pRun=[K,K1,ALPHA,CFR]
pMaxBas=[MaxBas]
p=[*psnow,*psoil,*pEvap,*pRun,*pMaxBas]
#return p