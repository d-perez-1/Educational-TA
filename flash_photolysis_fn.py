import numpy as np
import matplotlib.pyplot as plt
from gpiozero import LED
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import csv

flash=LED(14)
cw=LED(15)
leadtime=0.2 # time to collect before flash
flashtime=.020 # time flash should be on
binwidth=.005 # width of time bins in seconds

def main():
    # main stuff here
    save_full_data=False; # if true, save full data. False, save binned data
    plot_deltaOD=False; # True: plot delta OD, false: plot intensity
    direct='/home/pi/Adafruit_Python_ADS1x15/examples'
    fname='testing_saves.txt' # file name
    n_scan=1 # number of scans to combine
    runtime=2 # runtime in seconds
    GAIN=4
    run_flash_photolysis(direct,fname,n_scan,runtime,GAIN,save_full_data,plot_deltaOD)

def run_flash_photolysis(direct,fname,n_scan,runtime,GAIN,save_full_data,plot_deltaOD):
    print("Starting experiment") 
    # initialize adc board
    i2c=busio.I2C(board.SCL, board.SDA)

    ads=ADS.ADS1015(i2c)

    # set adc parameters
    ads.data_rate=3300
    ads.gain=GAIN
    ads.mode=0 # continuous mode

    chan=AnalogIn(ads,0) 
    tmp=chan.value # seems like whatever pin and gain are used here is used for get_last_result

    cw.on() # turn on probe
    flash.off() 
    # wait for probe to warm up
    wait_start=time.time()
    while time.time()-wait_start<5:
        tmp=1

    total_time=runtime+leadtime


    y=np.array([0]);
    t=np.array([0]);
    for n in range(n_scan):
        last_time=0
        i=0
        start=time.time()
        # prealocate for raw reads
        raw=np.zeros(round(3000*total_time))
        tmes=np.zeros_like(raw) # measured times
        # take measurements
        while last_time<total_time:
            # control the flash
            if last_time>leadtime and last_time<leadtime+flashtime: # turn on if in window
                flash.on()
            elif last_time>leadtime+flashtime and last_time<leadtime+flashtime+.02: # turn off in window after, don't need to keep calling
                flash.off()
            
            raw[i]=ads.get_last_result(fast=True)
            last_time=time.time()-start
            tmes[i]=last_time
            i+=1

        # chop off unused part of vectors
        raw=raw[0:i-1]
        tmes=tmes[0:i-1]
        y=np.concatenate((y,raw))
        t=np.concatenate((t,tmes))
        #print(time.time()-start)
        print("Completed "+str(n+1)+" out of "+str(n_scan))

    cw.off();

    # remove leading 0s
    y=y[1:-1]
    t=t[1:-1]

    # sort from low to high time
    #ind_sort=np.argsort(t)
    #t=t[ind_sort]
    #y=y[ind_sort]

    # bin data
    tb=np.linspace(0,total_time,round(total_time/binwidth))
    yb=np.zeros_like(tb)
    fill_count=np.zeros_like(tb)
    for i in range(np.size(t)):
        tmp=abs(tb-t[i])
        loc=np.where(tmp==np.min(tmp))
        yb[loc]+=y[i]
        fill_count[loc]+=1
    yb=np.divide(yb,fill_count)


    # save data
    with open(direct+'/'+fname,'w+') as f:
        if save_full_data==True:
            data=np.array([t,y])
        else:
            data=np.array([tb,yb])
        data=data.T
        np.savetxt(f,data)

    if plot_deltaOD:
        # find average value before flash
        tmp=abs(tb-leadtime)
        loc=np.where(tmp==np.min(tmp))
        loc=int(loc[0]-3) # make sure none of the flash is caught
        preFlash=np.mean(yb[0:loc])
        dOD=np.divide(preFlash,yb)
        dOD=np.log10(dOD)
        #dOD=1000*dOD # convert to mOD
        plt.plot(tb,dOD)
        plt.ylabel('delta OD')
        
    else:
        plt.plot(tb,yb)
        plt.ylabel('Intensity')
    
    print("Experiment completed")
    plt.xlabel('Time (S)')
    plt.show()
    return()

if __name__ == "__main__":
    main()
