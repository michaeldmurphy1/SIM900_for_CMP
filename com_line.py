from serial_talking import SRS_Device
from time import sleep

if __name__ == "__main__":
    
    #Creating obect representing commmunication channel to device
    chan = SRS_Device()
    #Who are we talking to?
    chan.get_idn()
    #Output: Stanford_Research_Systems,SIM922,s/n024290,ver2.70
    chan.set_points(1,0,"real1",[0.444,293,0.99246,77])
    chan.set_points(2,0,"real2",[0.444,293,0.99246,77])
    chan.view_points(1)
    chan.view_points(2)
    #Syntax for getting data goes as chan.get_temp(n) or chan.get_volt(n), where
    #   'n' represents the SIM922 channel in question (1-4)
    quit()
    #Call to get temperature for diode on line 1
    chan.get_temp(1)
    #Example output: 2.930000E+02 K
    chan.get_volt(1)
    #Example output: 4.439230E-01 V

    #One can also get multiple values by passing a second parameter, say to average over noise (really not that useful)
    chan.get_volt(1,5)
    #Example output: 4.438780E-01 V, 4.438810E-01 V, 4.438780E-01 V, 4.438810E-01 V, 4.438790E-01 V

    #To be able to access these numbers (specifically converting voltage into temperature),
    #   it is important that the SIM922 has accurate data for its "calibration curve"
    # Just as TeachSpin gives us a model for converting voltage to temperature, the SIM922
    #   has a built in algorithm, which you feed datapoints and it in turn knows how to 
    #   convert values
    # Each diode channel has its own256-point nonvolatile memory to store these calibration curve.
    #   Once they are set up, they remain through power-cycles, but one still needs to manually
    #   switch the active curve from the default to the user-defined
    # 
    # To instantiate a curve, you must pass 4 things:
    #    c:int, which input curve to deal with
    #    axis_type:int, an optional parameter, to define the type of the curve
    #        -> 0: Linear   | volts, kelvin
    #        -> 1: SemiLogT | volts, log_{10}(kelvin)
    #        -> 2: SemiLogV | log_{10}(volts), kelvin
    #        -> 3: LogLog   | log_{10}(volts), log_{10}(kelvin)
    #    name:str, an optional parameter to be given iff `axis_type` is given as well
    #    data:list, a list of float values that correspond to [sensor value, temperature], in the units
    #        specified for curve c. Multiple point pairs can be given, but the senor value must be in
    #        increasing order
    #
    #2 Things to note:erasing and more points the better
    chan.set_points(1,0,"testing",[0.444,293,0.99246,77])
    chan.view_points(1)
    chan.curve_type(1,1)
    chan.get_volt(2, 1)


'''
Average voltage at 77 K: 9.924571428571431 mV
'''