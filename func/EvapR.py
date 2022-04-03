
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
                print(f"seem to have more Evapotranspiration={act_E} and SM={self.SM}")
                state_SM = 0
                    
        #    ' Updating the states for next elevation zone
    else:
        state_SM=self.SM-E # Assumption is that this function received not PotE but Actual Evapotranspiration
        act_E=E

    self.SM=state_SM
    self.act_E=act_E 
