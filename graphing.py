import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from serial_talking import SRS_Device


def animate(i:int, ax, SRS_connection:SRS_Device, thermo_num:int, interval:int, interval_on_screen:int):
    SRS_connection.update_file(thermo_num, int(interval_on_screen/(interval/1000)))
    read_list = open("temperature_data.txt","r+").read().split('\n')
    xar = np.empty(len(read_list))
    yar = np.empty(len(read_list))
    for i, line in enumerate(read_list):
        x,y = line.split(',')
        xar[i] = float(x)
        yar[i] = float(y)
    xar *= interval/1000
    
    ax.clear()
    ax.set_title(f"Temperature of Diode {thermo_num}")
    ax.set_ylabel("Temperature [K]")
    ax.set_xlabel("Time [s]")
    ax.plot(xar,yar)

def create_animation(therm_num:int, curve_type:int=0, update_interval:int=500, interval_on_screen:int=15)->str|None:  
    '''Call this class to create an animation of diode `therm_num`'''
    
    #Clearing old data and ensuring we have a file to write to
    file = open("temperature_data.txt","w")
    file.close()
    try:
        chan = SRS_Device()
        name = chan.get_idn()
        assert name == "Stanford_Research_Systems,SIM922,s/n024290,ver2.70"
        chan.curve_type(therm_num,curve_type)

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ani = animation.FuncAnimation(fig, animate, fargs=(ax, chan,therm_num,update_interval,interval_on_screen), interval=update_interval, cache_frame_data=False )
        plt.show()
    except RuntimeError:
        #Thrown when the SIM900 is not turned on
        return "Problem Connecting to SIM900:\ntry turning on"
    except AssertionError:
        #Some other probllem connecting
        return "Problem Connecting to SIM900:\ntry turning off and on"
    else:
        chan.end()














































"""
#FROM 4/13 MONRING, correstly displays stream of temperature
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial_talking import SRS_Device
import numpy as np


def animate(i:int, SRS_connection:SRS_Device, thermo_num:int, interval:int, interval_on_screen:int):
    SRS_connection.update_file(thermo_num, int(interval_on_screen/(interval/1000)))
    read_list = open("temperature_data.txt","r+").read().split('\n')
    xar = np.empty(len(read_list))
    yar = np.empty(len(read_list))
    for i, line in enumerate(read_list):
        x,y = line.split(',')
        xar[i] = float(x)
        yar[i] = float(y)
    xar *= interval/1000
    #yar*=1000
    ax.clear()
    #mid = yar.mean()
    #mid = yar.median()
    #mini = yar.min()
    #maxi = yar.max()
    #ax.set_ylim(mid-mini,mid+maxi)
    ax.set_title(f"Temperature of Diode {thermo_num}")
    ax.set_ylabel("Temperature [K]")
    ax.set_xlabel("Time [s]")
    ax.plot(xar,yar)

if __name__ == "__main__":
    file = open("temperature_data.txt","w")
    file.close()
    
    chan = SRS_Device()
    therm_num=2
    #chan.set_points(therm_num,0,"read_data",[0.444,293,0.990,77])
    chan.set_curve(therm_num,0)
    interval = 500 # [ms]
    interval_on_screen = 15 #[s]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ani = animation.FuncAnimation(fig, animate, fargs=(chan,therm_num,interval,interval_on_screen), interval=interval, cache_frame_data=False )
    plt.show()"""