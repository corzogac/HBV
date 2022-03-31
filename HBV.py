#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#%%
class HBV():
    
    def __init__(self):
        self.load()
        self.readData('Bagmati.xlsx')
        self.ParamerVector()
        self.States()
        self.PotE=True #Input of column E is Evapotranspiration
        self.Qs=[]
        self.SPs=[]
        self.WCs=[]
        self.ins=[]
        
        
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
    
    def load(self):
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
    
    
    def sim(self):
        for i ,T in self.T:
            self.run(self.P[i],T,self.Epot[i])
    
    def run(self,P,T,E):
        self.PrintSnow()
        self.SnowRoutine(P,T)
        self.PrintSnow()
        
        #SP,WC,insoil,snow=
        print(f"SM  {self.SM}")
        self.SoilMoisture()
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
        
            
            
    def SnowRoutine(self,P,T):
        self.PrintSnow()
        if (self.SP > 0):
            self.snow = True #'SP = Snow pack
        else:
            self.snow = False

        if P > 0 :
            #' If the tempearature doesnt freeze
            if T > self.TT :
                    self.WC = self.WC + P    #' Water content increases
            else:
                # ' if not Snow pack increases with the precipitation conv into snow
                self.SP = self.SP + P * self.SFCF 
        
        if T > self.TT :
            melt = self.CFMAX * (T - self.TT) * self.TFAC
            if melt > self.SP:
                insoil = self.SP + self.WC
                self.WC = 0
                self.SP = 0
            else:
                self.SP = self.SP - melt
                self.WC = self.WC + melt
                if self.WC >= self.CWH * self.SP:
                    insoil = self.WC - self.CWH * self.SP
                    self.WC = self.CWH * self.SP
        else:
            refrez = self.CFR * self.CFMAX * (self.TT - T)
            if refrez > self.WC:
                    refrez = self.WC
            
            self.SP = self.SP + refrez
            self.WC = self.WC - refrez
            #' If there was no snow pack information then pass the valus of precipitation to the funoff rutine
            #' If there the temperature is above the freeting threshold the pass all precipitation direc to the tanks
            
        if T < self.TT:
            #' Else pass it to the SNOW PACK
            self.SP = self.SP+P*self.SFCF
        self.insoil=insoil
        print(f" SP= {self.SP} , WC= {self.WC}")
        print(f"Insoil {insoil}")

    def SoilMoisture(self):
        insoil=self.insoil
        self.SMOld=self.SM
        if insoil > 0:
            R=0 #Initial recharge will be zero and below will be estimated based on Y
            
        #To work with the analysis of the decimal values it is divided into inger part of insoil + real part
            if insoil < 1:
                Y = insoil   #decimal part of the precipitation or water from the soil storage
            else:
                m = int(np.floor(insoil))  #Integer part of the precipitation
                Y = insoil - m   #Decimal part of the precipitation or water from the soil storage
                for i in range(m):
                    if self.SM>self.FC:
                        print(f"Increase field capacity you are having values of soil moisture up to {SM}")
                        self.SM=self.FC
                    dRdP = (self.SM/self.FC) ** self.BETA #' Percentage of water contribution from the soil to the groundwater
                    if dRdP > 1:
                        dRdP = 1
                    
                    self.SM = self.SM + (1 - dRdP) #This is the recharge
                    R = R + dRdP
        
            dRdP = (self.SM / self.FC) ** self.BETA
            if dRdP > 1:
                dRdP = 1
            
            self.SM = self.SM + (1 - dRdP) * Y #' Could be optimized by only multiplying from the beginig the total decimal value??
            R = R + dRdP * Y #'Amount of water RECHARGE for the tanks
        else:
            R=insoil #case when no rain or insoil water   
            #Soil moisture also remains as it started and will be affected later by Evapotranspiration (other module)
        self.R=R
        

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

    
    def States(self):
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
    
    def readSPar(self):
            self.TT = self.p[0] 
            self.CFMAX = self.p[1]
            self.SFCF = self.p[2]
            self.CWH = self.p[3]
            self.CFR = self.p[4]
        
A=HBV()
A.SnowRoutine(10,10)  

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


    



