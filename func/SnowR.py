def SnowRoutine(self,P,T):
    """Snow Routine based on the Degree day method
    Args:
        P (float): Precipitation value
        T (float): Temperature
    """
    self.Ps()
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
