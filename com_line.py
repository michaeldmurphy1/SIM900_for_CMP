from serial_talking import SRS_Device
from time import sleep

if __name__ == "__main__":
    
    #file = open("3/23_first_run.txt","x")

    Chan = SRS_Device()
    Chan.get_idn()
    Chan.end()
    quit()
    Chan.get_temp(1)
    Chan.set_points(1,0,"testing",[0.444,293,0.990,77])
    Chan.view_points(1)
    Chan.set_curve(1,1)
    Chan.get_volt(2, 1)
    Chan.end()
    
    try:
        while( True ):
            temp1 = Chan.get_temp(1)
            temp2= Chan.get_temp(2)
            volt1 = Chan.get_volt(1)
            volt2 = Chan.get_volt(2)
            file.write(f"{volt1},{temp1},{volt2},{temp2}")
            sleep(1)
    except:
        file.close()

    #while True:
    #    Chan.get_volt(2)
    #    sleep(1)

    #Chan.set_points(1, axis_type=2, name='new_test')
    #Chan.view_points(1)
    '''Chan.set_points(1, data=[0.01,0.01,0.02,0.02,0.03,0.03,0.04,0.04,0.05,0.05,0.06,0.06,0.07,0.07,0.08,0.08])
    Chan.view_points(1)
    Chan.view_points(2)
    Chan.view_points(3)
    Chan.view_points(4)'''


    '''Chan.set_points(1, axis_type=2, name='after_break')
    Chan.view_points(1)
    Chan.set_points(1, data=[0.0001,.0002])
    Chan.view_points(1)'''
    quit()
    quit()
    #Chan.set_points(1, 1, "TEST")
    data = [0.0002,0.0001]#,0.0002,0.0003, 0.04, 0.05, 0.2,0.3]
    for i in range(int(len(data)/2)):
        print(f"{data[2*i]}, {data[2*i+1]}")
    Chan.set_points(1, 0, "NEW", data=data)
    #Chan.set_points(1, data=data)
    Chan.view_points(1)


'''
Average voltage at 77 K: 9.924571428571431 mV
'''