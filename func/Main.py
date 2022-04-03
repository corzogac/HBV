import yaml 
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

def loadDefPar(self):
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

    
def readSPar(self):
        self.TT = self.p[0] 
        self.CFMAX = self.p[1]
        self.SFCF = self.p[2]
        self.CWH = self.p[3]
        self.CFR = self.p[4]



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
  xmax=y1.shape[0]
  x=np.linspace(1,xmax,xmax)
  y2=self.P
  
  fig, ax1 = plt.subplots()
  plt.xlim(xmin,xmax)
  ax2 = ax1.twinx()
  ax2.set_ylim(0,np.floor(np.max(y2)*1.5))
  ax1.plot(x, y1, 'g-')
  ax2.invert_yaxis() 
  ax2.plot(x, y2, 'b-')
  ax2.fill_between(x, y2)
  ax1.set_xlabel('X data')
  ax1.set_ylabel(f'Y1 {var1}', color='g')
  ax2.set_ylabel(f'Y2 {var2}', color='b')
  plt.savefig(Name)
  #plt.show()  


def ReadInfo(self):
        with open('run.yaml', 'r') as stream:
                try:    
                        info=yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                        print(exc) 
        MP=info["Model Parameters"]
        self.TT=MP["TT"]
        self.CFMAX= MP["CFMAX"]
        self.SFCF= MP["SFCF"]
        self.CWH= MP["CWH"]
        self.CFR= MP["CFR"]
        self.FC=MP["FC"]
        self.BETA= MP["BETA"] 
        self.LP=MP["LP"]
        self.K= MP["K"] 
        self.K1=MP["K1"]
        self.ALPHA= MP["ALPHA"] 
        self.CF=MP["CF"] 
        self.PERC= MP["PERC"] 
        self.MaxBas= MP["MaxBas"]
        self.MP=pd.DataFrame.from_dict(MP,orient='index')
        self.MP=self.MP.T
        #self.MP.plot.bar()
        
        self.FileName=info["FileName"]
        
        St=info["States"]
        self.SP = St["SP"]   #10 # Snow Pack    
        self.WC = St["WC"]   #10 # Water Content in Snow Pack
        self.SM= St["SM"]   #20 # Initial value of soil moisture, assuming less than half Field Capacity
        self.UZ1 = St["UZ1"]   #20 # Upper Zone
        self.LZ1 = St["LZ1"]   #20 # Lower Zone
        self.St=pd.DataFrame.from_dict(St,orient='index')
        self.St=self.St.T
        
        
def GenerateRanParameters(self,nruns=10):
        #TLB = [-1,0,0,1,50,0.6,0,0,0,0,0,0,0.001,0.01,0,0,0.6,0.6]
        #TUB = [2,3,2,5,500,1.4,5,1,1,1,1,1.5,0.1,1,4,5,1.4,1.4]
        #indices=[0,3,17,12,13,4,11,7,8,9,10,14,15]
        #result_list = [LB[i] for i in indices]        
        #[]
        #psnow=[self.TT,self.CFMAX,self.SFCF,self.CWH,self.CFR]
        #psoil=[self.FC,self.BETA]
        #Soil moisture percentage in decimal where soil moisture reaches maximum potential evapotranspiration
        #pEvap=[self.LP]
        #pRun=[self.K,self.K1,self.ALPHA,self.CF]
        #pMaxBas=[self.MaxBas]
       
        #self.p=[*psnow,*psoil,*pEvap,*pRun,*pMaxBas]
        #[self.TT,self.CFMAX,self.SFCF,self.CWH,self.CFR]
        #[self.TT,self.CFMAX,self.)
        LB=np.array([-1, 1, 0.6, 0.001, 0.01, 50,  0.001, 0.001, 0.001, 0.001,   0,  0.6, 0,  50])
        UB=np.array([2,  5, 1.4,   0.1,    1, 500,     8,    1 ,     1,      1,  8, 1.4,  5, 30])
        print(LB.shape)
        print(UB.shape)
        parset=[]
        for i,lb in enumerate(LB):
                p=np.random.uniform(lb, UB[i], nruns)
                parset.append(p)
        self.mc_parset=np.array(parset).T
        
def loadPar(self):
        p=self.p
        self.TT=p[0]
        self.CFMAX=p[1] 
        self.SFCF=p[2] 
        self.CWH=p[3] 
        self.FC=p[4] 
        self.BETA=p[5] 
        self.LP=p[6] 
        self.K=p[7] 
        self.K1=p[8] 
        self.ALPHA=p[9] 
        self.CF=p[10]
        self.PERC=p[11]
        self.MaxBas=p[12]
        print(p)