#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   HBV.py
@Time    :   2022/03/29 22:28:24
@Author  :   Gerald Corzo 
@Version :   1.0
@Contact :   g.corzo@un-ihe.org
@License :   [C]Copyright 2022, G. Corzo
@Desc    :   #Hydrological Model HBV-96
             #Original source Lindström 1997.
             #Based on the implementation done by Juan Carlos Chacon in Matlab

'''

#%%
#[QNew, St] =
def  HBV(p,v,St,TFAC = 1,AREA = 2900): 
    """HBV[p,v,St,TFAC = 1,AREA = 2900]

    Args:
        p [numpy array of 18 positions]: Parameter Set
            p[1] ->  TT = Limit temperature for rain/snow precipitation 
            p[2] ->  TTI = temperature treshold for linear mix of snow/rain precipitation 
            p[3] ->  TTM = Limit temperature for melting 
            p[4] ->  CFMAX = Degree day factor [measures the temperature variation along the day] 
            p[5] ->  FC = Field Capacity 
            p[6] ->  ECORR = Evapotranspiration corrector factor 
            p[7] ->  EP = Long term mean potential evapotranspiration 
            p[8] ->  LP = Soil moisture value where soil moisture reaches maximum potential evapotranspiration
            p[9] ->  K = Upper zone response coefficient 
            p[10] ->  K1 = Lowe zone response coefficient 
            p[11] ->  ALPHA = upper zone runoff coefficient 
            p[12]->  BETA = Controls the contribution of the increase in the soil moisture or to the response function 
            p[13] ->  CWH = Maximum amount of water that can be stored in snow pack 
            p[14] ->  CFR = Refreezing factor 
            p[15] ->  CFLUX = Capilar flux 
            p[16] ->  PERC = Percolation 
            p[17] ->  RFCF = Rainfal correction factor 
            p[18] ->  SFCF = Snowfall correction factor 
            
            
        v [numpy array of 4 positions]: Input vector 
            P = Total precipitation v[1]
            T = actual temperature v[2]
            ETF = Total potential evapotranspiration v[3] # input
            LTAT = long term average temperature v[4] #input
        
        St [_type_]: _description_
        Internal States -> storages
            SPOld = intial estimation of snow pack St[1]
            SMOld = Soil Moisture in previous time step St[2]
            UZOld = Upper zone storage previous time step St[3]
            LZOld = Lower zone storage previous time step St[4]
            WCOld = Water content in snow pack St[5]
        
        TFAC = Time factor  = dt/86400
        AREA = Catchment area [km²]
            
    """
    # input arguments of the function are parameters [p], inputs [v] and states [St]
    # Data load

    #v = Input vector
    #p = Parameter vector
    #St = State vector
    #x = Aditional parameters [values that multiply old states in the model]

    #inputs v[1,2]
    P = v[0] # Precipitation [mm]
    T = v[1] # Temperature [C]
    EP = v[2] # Long terms [monthly] Evapotranspiration [mm]
    TM = v[3] # Long term [monthly] average temperature [C]

    # Parameters vector of p[1,20]
    TT = p[0]
    TTI = p[1]
    TTM = p[2]
    CFMAX = p[3]
    FC = p[4]
    ECORR = p[5]
    ETF = p[6]
    LP = p[7]
    K = p[8]
    K1 = p[9]
    ALPHA = p[10]
    BETA = p[11]
    CWH = p[12]
    CFR = p[13]
    CFLUX = p[14]
    PERC = p[15]
    RFCF = p[16]
    SFCF = p[17]

    #Non optimised parameters

    #print(St)
    # States vector St[1,5]
    SPOld = St[0] # Snow Pack
    SMOld = St[1] # Soil Moisture
    UZOld = St[2] # Upper Zone
    LZOld = St[3] # Lower Zone
    WCOld = St[4] # Water Content in Snow Pack

    ## Inputs Routine
    #Input: Here is defined the ammount of rain or snow precipitated over the
    #basin
    #T = Actual temperature in the catchment
    #TT = Temperature limit for rain/snow precipitation
    #TTI = temperature treshold for linear mix of snow/rain precipitation
    if T<=(TT-TTI/2): # if temerature is below the snow/rain treshold
                    # then all precipitation becomes snowfall [SF]
        RF = 0.0
        SF = P*SFCF
    else:
        if T>=TT+TTI/2.0: # if the temperature is over the snow/rain treshold,
                                # the all precipitation becomes rainfall [RF]
            RF = P*RFCF
            SF = 0.0
        else: #Otherwise, the amount of snow and rain precipitated is a linear combination of both
            RF =      2.0*[T-TT]/TTI  * P * RFCF
            SF = [1.0-2.0*[T-TT]/TTI] * P * SFCF


    ## Snow Routine
    """
    TTM = Limit temperature for melting
    CFMAX = Degree day factor (measures the temperature variation along the day)
    TFAC = Temperature factor
    SP, SPOld, SPNew = frozen part of snowpack
    SF = Snowfall [comes from input]
    CFR = Refreezing factor
    """
    if T>TTM: # if temeperature is higher than limit temperature 
              # for melting [snow is melting]

        if (CFMAX*TFAC*(T-TTM)<SPOld+SF): # Evaluate if the snow melt is higher
                                            # than the designed fraction of the snow pack
            MELT = CFMAX*TFAC*(T-TTM) # if yes, then the thaw is equivalent 
                                        # to the one described by the physical process
        else:
                MELT = SPOld+SF # Otherwise, the snow melt is going to be considered
                            # as a fraction of the snow pack, plus the actual snowfall
        SPNew = SPOld+SF-MELT
        WCInt = WCOld+MELT+RF

    else: # if the temperature is below the critical treshold

        if [CFR*CFMAX*TFAC*[TTM-T]<WCOld+RF]: # this is a conditional for the
                                                # refreezing of water stored in the snow
            REFR = CFR*CFMAX*TFAC*[TTM-T] # if the temperature is too low, it
                                                # will freeze again
        else:
            REFR = WCOld+RF # otherwise the frozen water will be the same
                                # as the previous stored water plus the rainfall
        SPNew = SPOld+SF+REFR
        WCInt = WCOld-REFR+RF

    if (WCInt>CWH*SPNew): #if there is more water than snow holding capacity then
        IN = WCInt-CWH*SPNew #There is going to be infiltration
        WCNew = CWH*SPNew # the snow will be saturated by liquid water
        
    else: 
        IN = 0.0 #if there is no saturation, then there is no infiltration to soil
        WCNew = WCInt # the amount of water stored in the snow will be the same as before
    

    """ Soil Routine
    FC = Maximum soil moisture content
    IN = Infiltration -> defined by the snow melt if considered````
    BETA = Controls the contribution of the increase in the soil moisture or
    to the response function
    ETF = Total potential evapotranspiration
    TM = daily long term mean temperature
    ECORR = Evapotranspiration height corrector factor
    EP = Long term mean potential evapotranspiration
    EPInt = Adjusted potential evapotranspiration
    LP = Soil moisture value where soil moisture reaches maximum potential evapotranspiration
    SMOld = Soil Moisture
    CFLUX = Capilar flux
    UZOld = Upper zone storage previous time step
    """

    R = ((SMOld/FC)**BETA)*IN #Runoff from soil
    EPInt = (1.0+ETF*(T-TM))*ECORR*EP # Monthly coefficient for evapotranspiration

    if (SMOld < (LP*FC)): # conditional to check if the old soil moisture is
                            # greater than the limit for potential evapotranspiration
        EA = TFAC*SMOld/[LP*FC]*EPInt #actual evapotranspiration when there is
                                        # no moisture to reach the potential evapotranspiration
    else:
        EA = TFAC*EPInt #actual evapotranspiration with total moisture availability
    
    
    # if the upper zone storage is greater 
    #than the potential capilar flow, then is going to be caiplar flow    
    #print(TFAC)
    #print(CFLUX)
    #print(SMOld)
    #print(FC)
    
    if (TFAC*CFLUX*(1.0-(SMOld/FC))<UZOld): 
        CF = TFAC*CFLUX*(1.0-(SMOld/FC)) #capilar flow definition
    else:
        CF = UZOld #if the storage in the upper zone is lower than the flow
                    # itself, it will remain as the previous value for the UZ storage
    
    SMNew = SMOld+[IN-R]+CF-EA #soil moisture content after runoff and evapotranspiration and rainfall
    UZInt1 = UZOld+R-CF #upper zone storage.

    ## Response Routine
    #PERC = Percolation
    #LZOld = Lower zone storage
    #K = Upper zone response coefficient
    #K1 = Lowe zone response coefficient
    #ALPHA = upper zone runoff coefficient
    #AREA = Catchment area
    
    if (TFAC*PERC<UZInt1): # Check for percolation. if the level in the upper zone
                            #is higher, then the lower zone is going to be affected by this
        LZInt1 = LZOld+TFAC*PERC # the definition of the lower zone is equal to
                                    # the previous one, plus the percolation from the upper zone
    else:
        LZInt1 = LZOld+UZInt1 # otherwise, the lower zone is going to be defined by the
                                # actual upper zone plus the previous lower zone response

    if (UZInt1>TFAC*PERC): # The same procedure as before, but now considering the upper box
        UZInt2 = UZInt1-TFAC*PERC #definition of the storage due to losses on percolation
    else:
        UZInt2 = 0.0 # if the upper zone storage is not enough, then all goes
                        #to percolation, and is reflected in the lower response box


    Q0 = K*(UZInt2**(1.0+ALPHA)) #definition of outflow from upper reponse box
    Q1 = K1*LZInt1 # definition of outflow from lower response box

    UZNew = UZInt2-TFAC*Q0 #new value for the upper zone storage
    LZNew = LZInt1-TFAC*Q1 # new value for the lower zone storage

    QNew = AREA*(Q0+Q1)/86.4 # total outflow

    ## State vector  updater save
    # WCOld = WCNew
    # SMOld = SMNew
    # UZOld = UZNew
    # LZOld = LZNew
    # SPOld = SPNew
    
    St[0] = SPNew
    St[1] = SMNew
    St[2] = UZNew
    St[3] = LZNew
    St[4] = WCNew
    
    return QNew,St

#%%
import matplotlib.pyplot as plt
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


    
# %%
