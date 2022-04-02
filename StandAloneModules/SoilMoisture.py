import numpy as np
#%%
def SoilMoisture(p,insoil,SM):
    #p[5] ->  FC = Field Capacity 
    FC = p[5]    # Field Capacity=Maximum of soil moisture
    BETA = p[6] # Shape Coefficient - exponential variation of the relationship

    if insoil > 0:
        R=0 #Initial recharge will be zero and below will be estimated based on Y
        
    #To work with the analysis of the decimal values it is divided into inger part of insoil + real part
        if insoil < 1:
            Y = insoil   #decimal part of the precipitation or water from the soil storage
        else:
            m = int(np.floor(insoil))  #Integer part of the precipitation
            Y = insoil - m   #Decimal part of the precipitation or water from the soil storage
            for i in range(m):
                if SM>FC:
                    print(f"Increase field capacity you are having values of soil moisture up to {SM}")
                    SM=FC
                dRdP = (SM/FC) ** BETA #' Percentage of water contribution from the soil to the groundwater
                if dRdP > 1:
                    dRdP = 1
                
                SM = SM + (1 - dRdP) #This is the recharge
                R = R + dRdP
    
        dRdP = (SM / FC) ** BETA
        if dRdP > 1:
            dRdP = 1
        
        SM = SM + (1 - dRdP) * Y #' Could be optimized by only multiplying from the beginig the total decimal value??
        R = R + dRdP * Y #'Amount of water RECHARGE for the tanks
    else:
        R=insoil #case when no rain or insoil water   
         #Soil moisture also remains as it started and will be affected later by Evapotranspiration (other module)
    
    return R, SM

# %%
