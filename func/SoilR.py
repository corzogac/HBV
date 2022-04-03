import numpy as np

def SoilMoisture(self):
    """Soil Moisture function
    Will work with the values of the object_
    """
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
                    print(f"Increase field capacity you are having values of soil moisture up to {self.SM}")
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
