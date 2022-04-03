import numpy as np
import matplotlib.pyplot as plt

def Performance(self,FileName="R1"):
    r={}
    Qo=self.Qo
    Qs=self.Qs
    S=np.size(Qs)
    Error=Qo-Qs
    Do=Qo-np.mean(Qo) #Deviation from means Observed
    Ds=Qs-np.mean(Qs) #Deviation from means Simulated
    RMSE=np.sum(np.power(Error,2))/S
    MAE=np.sum(np.abs(Error))/S
    #how many times it overestimates
    Over=100*np.sum(Error<0)/S
    Under=100*np.sum(Error>0)/S
    r["Correlation"]=np.corrcoef(Qo,Qs)
    r["RMSE"]=RMSE
    r["MAE"]=MAE
    r["Over"]=Over #Percentage of over estimation
    r["Under"]=Under #Percentage of under estimation
    r["AvePerError"]=np.sum(100-(100*Error/Qo))/S
    r["Nash"]=1-(np.sum(Error**2)/np.sum(Do**2)) #The Nash-Sutcliffe model efficiency coefficient (𝐸) is used to quantify how well a model simulation can predict the outcome variable.
    #r["R2"]=1-  #he coefficient of determination (𝑅2) is a measure of the goodness of fit of a statistical model.
    with open(f"{FileName}.txt", 'w') as f: 
        for key, value in r.items(): 
            f.write('%s:%s\n' % (key, value))
    return r

def PlotError(self):
    f,(ax1, ax2) = plt.subplots(2, 1, sharex=True,figsize=(8,10))
    
    ax1.plot(self.Qs,label="Sim")
    ax1.plot(self.Qo,label="Obs")
    ax1.grid()
    ax2.set_xlabel("Time step")
    ax1.set_ylabel("Discharges")
    ax2.plot(self.Qo-self.Qs)
    ax2.set_ylabel("Error (Observed-Simulated)")
    ax2.grid()
    ax1.legend(loc="upper right")

def PlotError(self):
    f,(ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True,figsize=(8,13))
    x=np.linspace(0,np.size(self.Qs),np.size(self.Qs))
    ax1.plot(self.Qs,label="Sim")
    ax1.plot(self.Qo,label="Obs")
    ax1.grid()
    ax2.set_xlabel("Time step")
    ax1.set_ylabel("Discharges")
    ax2.plot(self.Qo-self.Qs)
    ax2.set_ylabel("Error (Observed-Simulated)")
    ax2.grid()
    ax1.legend(loc="upper right")
    ax3.bar(x,100*(self.Qo-self.Qs)/self.Qo)
    ax3.set_ylabel("Error Percentage of Observed")
    ax3.grid()
    ax3.set_ylim(-100,100)

def PlotPolarError(self):
    N=np.size(self.Qo)
    theta = np.linspace(0.0, N/(2 * np), N, endpoint=False)
    Perc=(self.Qo-self.Qs)/self.Qs  #Radius
    ax = plt.subplot(projection='polar')
    width = 1
    ax.bar(theta, Perc, width=width, bottom=0.0, alpha=0.5)