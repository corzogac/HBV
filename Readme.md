# HBV Hydrological model


## Desription
This repository contains an example of the HBV hydrological model following the version of Lindström 1997.


## Features

Hydrological

- Made to process a single step of the hydrological processes

- Has a soil moisture analysis that works as a exponential function that retains it state and relates a ratio between rain and response to the

- Has two tanks that represent the upper zone and lower zone groundwater processes


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

## Examples

