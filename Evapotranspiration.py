

def Evapotranspiration(p,SM,SMOld,E,PotE):
    """Evapotranspiration estimates from SM
    Evapotranspiration(p,SM,SMOld,PotE,snow)
    Args:
        p (numpy array): _description_
        SM (Float): Soil Moisture in current time step
        SMOld (Float): Soil Moisture previous state 
        PotE (Float): values should
        snow (Binary): If there was Snow, not Evap

    Returns:
        float, float: state_SM,act_E 
    """
    #Check if Potential evapotranspiration was provided or Actual
    if PotE:
        LP = p[7]    # (% of FC) Limit for PotEvap=Threshold for reduction of evapotranspiration
        FC = p[5]    # Field Capacity=Maximum of soil moisture
    
        #'Working with the Mean value of SM to have a better approximation of the dynamics of the transition
        mean_SM = (SM + SMOld) / 2
        
        #Validation of the SM bellow the LP limit (Decimal units,between  0-1)
        if mean_SM < LP * FC:
            act_E = E * mean_SM/(LP * FC)
        else:
            act_E = E
                        
        #'Update the soil Moisture substracting the Actual Evapotranspiration
        state_SM = SM - act_E
            
        #' If the Actual Evapotranspiration is higher than the SM then assign 0
        if state_SM < 0:
                print(f"seem to have more Evapotranspiration={act_E} and SM={SM}")
                state_SM = 0
                    
        #    ' Updating the states for next elevation zone
    else:
        state_SM=SM-E # Assumption is that this function received not PotE but Actual Evapotranspiration
        act_E=E

    return state_SM,act_E 
