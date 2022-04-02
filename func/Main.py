import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def readData(self,FileName):
        Df=pd.read_excel(FileName,index_col=0,parse_dates=True)
        #Df.head()
        self.Qo=Df["Qobs"].to_numpy()
        self.Epot=Df["Epot"].to_numpy()
        self.P=Df["P"].to_numpy()
        self.T=Df["Temp"].to_numpy()
        self.LTAT = np.mean(self.T)*np.ones(len(self.Qo))
        self.AREA = 2900
        self.TFAC=1

def loadPar(self):
        self.TT = 0    #Limit temperature for rain/snow precipitation
        self.CFMAX = 3    # Degree day factor [measures the temperature variation along the day] 
        self.SFCF = 1     # Rainfal correction factor 
        self.CWH = 0.05     # Maximum amount of water that can be stored in snow pack 
        self.CFR = 0.8     # Refreezing factor 
        #For Soil
        self.FC = 50    # Field Capacity=Maximum of soil moisture
        self.BETA = 1.2 # Shape Coefficient - exponential variation of the relationship
        self.LP=0.4   
        self.K = 0.04
        self.K1 = 0.1
        self.ALPHA = 0.5
        self.CF = 0.05  #Capilarity Flux 
        self.PERC = 0.05
        self.MaxBas=10

def ParamerVector(self):
        psnow=[self.TT,self.CFMAX,self.SFCF,self.CWH,self.CFR]
        psoil=[self.FC,self.BETA]
        #Soil moisture percentage in decimal where soil moisture reaches maximum potential evapotranspiration
        pEvap=[self.LP]
        pRun=[self.K,self.K1,self.ALPHA,self.CFR]
        pMaxBas=[self.MaxBas]
        self.p=[*psnow,*psoil,*pEvap,*pRun,*pMaxBas]

def loadStates(self):
    self.SP = 10 # Snow Pack
    self.WC = 10 # Water Content in Snow Pack
    self.SM=20 # Initial value of soil moisture, assuming less than half Field Capacity
    self.UZ1 = 20 # Upper Zone
    self.LZ1 = 20 # Lower Zone
    


def PrintSnow(self):
        print(f"Temp Threshold {self.TT}")
        print(f"CF Max {self.CFMAX}")
        print(f"SFCF {self.SFCF}")
        print(f"CWH {self.CWH}")
        print(f"CFR {self.CFR}")

def Plot2Axis(self):
  var1="Discharge"
  var2="Precipitation"
  y1=self.Qo
  Name="HRU"
  xmin=0
  xmax=len(y)
  x=np.linspace(1,len(y),len(y))
  y2=self.P
  
  fig, ax1 = plt.subplots()
  plt.xlim(xmin,xmax)
  ax2 = ax1.twinx()

  ax1.plot(x, y1, 'g-')
  ax2.plot(x, y2, 'b-')

  ax1.set_xlabel('X data')
  ax1.set_ylabel(f'Y1 {var1}', color='g')
  ax2.set_ylabel(f'Y2 {var2}', color='b')
  plt.savefig(Name)
  #plt.show()  

