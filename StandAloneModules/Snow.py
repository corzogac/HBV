# %%
def SnowRoutine(p,P,T,SP,WC,TFAC = 1):
    """SnowRoutine

    Args:
        p (numpy array):
            TT    = p[0] 
            CFMAX = p[1]
            SFCF = p[2]
            CWH = p[3]
            CFR = p[4]
        P (float): precipitation
        T (float):Actual temperature in the catchment
        SP (float): _description_
        WC (float): _description_
        TFAC (int, optional): _description_. Defaults to 1.
        AREA (int, optional): _description_. Defaults to 2900.

    Returns:
        floats: SP Updated snow pack,
        WC   Updated Water content, 
        insoil    Final water to going into soil routine 
        snow binary to be used in other routines (just to know avoid running this routine)
    """
    TT = p[0] 
    CFMAX = p[1]
    SFCF = p[2]
    CWH = p[3]
    CFR = p[4]
    if (SP > 0):
        snow = True #'SP = Snow pack
    else:
        snow = False

    if P > 0 :
       #' If the tempearature doesnt freeze
       if T > TT :
            WC = WC + P    #' Water content increases
       else:
            SP = SP + P * SFCF # ' if not Snow pack increases with the precipitation conv into snow
    
    if T > TT :
       melt = CFMAX * (T - TT) * TFAC
       if melt > SP:
           insoil = SP + WC
           WC = 0
           SP = 0
       else:
           SP = SP - melt
           WC = WC + melt
           if WC >= CWH * SP:
               insoil = WC - CWH * SP
               WC = CWH * SP
    else:
       refrez = CFR * CFMAX * (TT - T)
       if refrez > WC:
            refrez = WC
       
       SP = SP + refrez
       WC = WC - refrez
    #' If there was no snow pack information then pass the valus of precipitation to the funoff rutine
    #' If there the temperature is above the freeting threshold the pass all precipitation direc to the tanks
    
    if T < TT:
        #' Else pass it to the SNOW PACK
          SP = SP+ P*SFCF
    
    return SP, WC,insoil,snow
