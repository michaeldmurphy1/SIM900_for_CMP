from serial_talking import SRS_Device
from time import sleep

if __name__ == "__main__":
    #Creating obect representing commmunication channel to device
    Chan = SRS_Device()
    #Who are we talking to?
    Chan.get_idn()
    
    #Syntax for getting data goes as Chan.get_temp(n) or Chan.get_volt(n), where
    #   'n' represents the SIM922 channel in question (1-4)

    #Call to get temperature for diode on line 1
    Chan.get_temp(1,1)
    Chan.get_volt(2)
    quit()


    #Creating channel to device
    Chan = SRS_Device()
    #Who are we talking to?
    Chan.get_idn()
    
    #Call to get temperature for diode on line 1
    Chan.get_temp(1)

    #To be called when closing
    #TODO:how #1 to make it so we don't need to manually do this?
    Chan.end()
    quit()
    Chan.set_points(1,0,"testing",[0.444,293,0.990,77])
    Chan.view_points(1)
    Chan.set_curve(1,1)
    Chan.get_volt(2, 1)


'''
Average voltage at 77 K: 9.924571428571431 mV
'''