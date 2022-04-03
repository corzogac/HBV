    
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
    self.UZ1=UZ2
    self.LZ1=LZ2 
    
