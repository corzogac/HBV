#%%
import matplotlib.pyplot as plt
import numpy as np
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
    def __init__(self):
        self.rd('Bagmati.xlsx') #Hydrological Data
        self.lp()  #group parameters
        self.lpv() #load Parameter vecto
        
        self.PotE=True #Input of column E is Evapotranspiration
        self.Qs=[]
        self.SPs=[]
        self.WCs=[]
        self.ins=[]
        
    
    def sim(self):
        for i ,T in self.T:
            self.run(self.P[i],T,self.Epot[i])
    
    def run(self,P,T,E):
        self.Sn(P,T)
        
        #SP,WC,insoil,snow=
        print(f"SM  {self.SM}")
        self.Sm()
        print(f"SMOld  {self.SMOld}")
        print(f"SM  {self.SM}")
       
        #Re,SM=
        if self.snow:
            self.act_E = 0
        else:
            self.PotE=True
        
        self.Evapotranspiration(E)
        print(f"SM  {self.SM}")
        print(f"actE  {self.act_E}")
       
        #SM,act_E=
        
        self.SurfaceFlow()
        print(f"QNew  {self.QNew}")
        #QNew,UZ2,LZ2 =
        
            
            
           

    def Evapotranspiration(self,E):
        #Check if Potential evapotranspiration was provided or Actual
        if self.PotE:
            #'Working with the Mean value of SM to have a better approximation of the dynamics of the transition
            mean_SM = (self.SM + self.SMOld) / 2
            
            #Validation of the SM bellow the LP limit (Decimal units,between  0-1)
            if mean_SM < self.LP * self.FC:
                act_E = E * mean_SM/(self.LP * self.FC)
            else:
                act_E = E
                            
            #'Update the soil Moisture substracting the Actual Evapotranspiration
            state_SM = self.SM - act_E
                
            #' If the Actual Evapotranspiration is higher than the SM then assign 0
            if state_SM < 0:
                    print(f"seem to have more Evapotranspiration={act_E} and SM={SM}")
                    state_SM = 0
                        
            #    ' Updating the states for next elevation zone
        else:
            state_SM=self.SM-E # Assumption is that this function received not PotE but Actual Evapotranspiration
            act_E=E

        self.state_SM=state_SM
        self.act_E=act_E 

    def SurfaceFlow(self):
        UZ1=self.UZ1
        LZ1=self.LZ1
        PERC=self.PERC
        CF=self.CF
        R=self.R
        TFAC=self.TFAC
        
        if CF<(UZ1+R):
            UZ2 = UZ1+R-CF #upper zone storage updated with coming recharge and capilarity flux.
        else:
            UZ2 = UZ1+R
        # Check for percolation. if the level in the upper zone
        #is higher, then the lower zone is going to be affected by this
        if (TFAC*PERC<UZ2): 
            UZ2 = UZ2-TFAC*PERC
            LZ2 = LZ1+TFAC*PERC  
        else:
            LZ2 = LZ1+UZ1
            UZ2 = 0.0 # if the upper zone storage is not enough, then all goes
                    #to percolation, and is reflected in the lower response box
        if UZ2>0:
            Q0 = self.K*((UZ1+UZ2)/2)**(1.0+self.ALPHA) #definition of outflow from upper reponse box
            UZ2 = UZ2-TFAC*Q0 # new value for the upper zone storage
        else:
            Q0=0         
        
        if LZ2>0:
            Q1 = self.K1*(LZ1+LZ2)/2 # definition of outflow from lower response box
            LZ2 = LZ2-TFAC*Q1 # new value for the lower zone storage
        else:
            Q1=0

        self.QNew = self.AREA*(Q0+Q1)/86.4 # total outflow m/s ( Assuming Area (1000mx1000m * 0.001 m / 86.400.000))
        self.UZ2=UZ2
        self.LZ2=LZ2 

    

    
    def readSPar(self):
            self.TT = self.p[0] 
            self.CFMAX = self.p[1]
            self.SFCF = self.p[2]
            self.CWH = self.p[3]
            self.CFR = self.p[4]

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


    



