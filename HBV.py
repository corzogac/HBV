#%%
import matplotlib.pyplot as plt
import pandas as pd
from func import *

    
#%%
class HBV():
    rd=readData
    ls=loadStates
    lp=loadPar
    lpv=ParamerVector
    Sn=SnowRoutine
    Sm=SoilMoisture
    Ps=PrintSnow
    Ev=Evapotranspiration
    Sf=SurfaceFlow
    Ri=ReadInfo
    GP=GenerateRanParameters
    Pe=Performance
    Pl2=Plot2Axis
    Ple=PlotError
    Plp=PlotPolarError
    def __init__(self):

        self.Ri()
        #self.rd('Bagmati.xlsx') #Hydrological Data
        self.rd(self.FileName)
        self.ls()  #Load states
        self.PotE=True #Input of column E is Evapotranspiration
        self.Qs=[]
        self.SPs=[]
        self.WCs=[]
        self.ins=[]
        self.Evs=[]
        self.SMs=[]
        
    
    def sim(self):
        for i ,T in enumerate(self.T):
            P=self.P[i]
            E=self.Epot[i]
            self.run(P,T,E)
            self.Qs.append(self.QNew)
            self.SPs.append(self.SP)
            self.WCs.append(self.WC)
            self.ins.append(self.insoil)
            self.Evs.append(self.act_E)
            self.SMs.append(self.SM)
        self.r=self.Pe()
        #self.Ple() #Plot errors
        #return self.Qs, r
    
    def run(self,P,T,E):
        self.Sn(P,T)
        #print(f"SM  {self.SM}")
        self.Sm()
        #print(f"SMOld  {self.SMOld}")
        #print(f"SM  {self.SM}")
       
        if self.snow:
            self.act_E = 0
        else:
            self.PotE=True
        
        self.Ev(E)
        #print(f"SM  {self.SM}")
        #print(f"actE  {self.act_E}")
       
        self.Sf()
        #print(f"QNew  {self.QNew}")
    def Optimize(self):
        self.lp()  #group parameters
        self.lpv() #load Parameter vector
    
    def uncertainty(self):
        self.GP() #group parameters
        n=self.mc_parset.shape[0]
        self.Qruns=[]
        for i in range(n):
            plt.close
            self.p=self.mc_parset[1]
            self.lp()
            self.ls()  #Load states
            self.sim()
            self.Qruns.append(self.Qs)
            plt.visible=False
            plt.plot(self.Qs)
            plt.savefig(f"Run{i}")    
            
            
    
if __name__ == "__main__":        
    A=HBV()
    A.Sr(10,10)  

#%%
def Plot2Axis(x,y1,y2,var1="precip",var2="surf",Name="HRU",xmin=0,xmax=2000):
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


    



