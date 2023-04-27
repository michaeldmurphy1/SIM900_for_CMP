from serial_talking import SRS_Device

if __name__ == "__main__":
    
    #Creating obect representing commmunication channel to device
    chan = SRS_Device()
    #Who are we talking to?
    chan.get_idn()
    #Output: Stanford_Research_Systems,SIM922,s/n024290,ver2.70
    #chan.set_points(1,0,"real1",[0.444,293,0.99246,77])
    #chan.set_points(2,0,"real2",[0.444,293,0.99246,77])


    #chan.view_points(1)
    #chan.view_points(2)
    #Syntax for getting data goes as chan.get_temp(n) or chan.get_volt(n), where
    #   'n' represents the SIM922 channel in question (1-4)
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
    # Each diode channel has its own 256-point nonvolatile memory to store these calibration curves.
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
    #4 Things to remember:
    #   Setting a curve, as in givign it a name and type will ERASE the current curve, so be wary
    #   Data must be added in increasing voltage value, and at least 2 points must be added to be a
    #       valid curve. Even trying to read a curve with one point will cause an error
    #   The more points the better: at the time of writing this, we only have room temp and 77K accessible,
    #       but obviously adding another point will make the temperature data more accurate. (If a third is
    #       ever made, make sure to update the code wtihin `\temperature_fitting_code` as well)
    #   The SRS_Device defaults to the built in curve--one must manually update with chan.curve_type(n,1) to 
    #       set to a user-defined curve

    #Syntax for creating a cruve (deletes existing one)
    chan.set_points(1,0,"real data",[0.444,293,0.99246,77])

    #Syntax for setting a curve: chan.curve_type(c,n), c for diode channel, and n for type (default or user)
    chan.curve_type(1,1)
    #One can also just view the current type by only passing the first argument:
    chan.curve_type(1)

    #How to view the curve type, name, and all points in a diode currently
    chan.view_points(1)
    
    chan.get_volt(2)