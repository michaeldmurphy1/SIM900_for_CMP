from serial_talking import SRS_Device
from time import sleep

'''
Average voltage at 77 K: 9.924571428571431 mV
'''

if __name__ == "__main__":
    
    chan = SRS_Device()
    chan.get_idn()


    chan.get_temp(1)
    chan.get_volt(1)

    chan.get_volt(1,5)

    #Valid Data
    chan.set_points(1,0,"real data",[0.444,293,0.99246,77])
    chan.view_points(1)
    chan.curve_type(1,1)
    chan.get_volt(2, 1)