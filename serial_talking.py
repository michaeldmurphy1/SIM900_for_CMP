import pyvisa
import serial
import numpy as np
from time import sleep
import logging
import sys

class SRS_Device():

    ESC = 'XYZ'
    temp_port = 4

    def __init__(self):
        logging.basicConfig(format="%(message)s", level=logging.INFO,
                            stream=sys.stdout)
        self.logger = logging.getLogger("SIM_Run")

        #Setting up pyvisa objects for the SIM900, which houses SIM922
        rm = pyvisa.ResourceManager()
        #TODO: figure out how to generalize ports?
        self.channel = rm.open_resource('ASRL1::INSTR')
        #A test to see if we are connected to something (if not, the SIM900 is not on)
        try:
            self.channel.query("*IDN?")
        except pyvisa.errors.VisaIOError as e:
            raise RuntimeError("Please turn on the SIM900") from e
        self.channel.read_termination = "\r\n" #This may need to be "\r\n"
        self.channel.write_termination = "\r"
        self.channel.write('SRST')
        #Note: not using set_points() here, making sure user is aware of the
        #   curve they are using (otherwise they may not understand)
        self.ping()
        self.logger.info("Connection to SIM900 established")
        #Now Interfacing with SIM922
        self.channel.write(f"CONN {self.temp_port},'{self.ESC}'")
        self._talk_to_SIM(self._set_error_masks)

    def end(self):
        #Closing communication with ASRL1::INSTR
        #TODO: should we be writing final things to tidy up?
        self.channel.write(f"'{self.ESC}'")
        self.ping()
        self.channel.close()
   
    def ping(self):
        if( self._ping() == False):
            raise ValueError("Problem connecting to SIM900")
    def _ping(self):
        #ONLY VALID FOR SIM900
        try:
            if( self.channel.query("ECHO? 'hello'") == 'hello' ):
                return True
            else:
                self.channel.write('SRST')
                self.channel.write('FLSH')
                return self.channel.query("ECHO? 'hello'").strip() == 'hello'
        except:
            #Our connection is with the SIM922, need to exit back to SIM900
            self.channel.write(f"'{self.ESC}'")
            self.channel.write('SRST')
            return self.ping()


    def _set_error_masks(self):
        #Setting the enable register's AND masks to 1 for values I care about /
        #   have implimented things to deal with -- Update as you see fit!!
        #self.channel.write("PSTA 1") <- what does this do?
        '''#Setting the Service Request Enable (SRE) register
        self.channel.write("*SRE 1,1")
        self.channel.write("*SRE 5,1")
        self.channel.write("*SRE 7,1")''' 
        #Setting the Standard Event Status Enable (ERE) register
        self.channel.write("*ERE 1,1")
        self.channel.write("*ERE 2,1")
        self.channel.write("*ERE 3,1")
        self.channel.write("*ERE 4,1")
        self.channel.write("*ERE 5,1")
        #Setting the Communication Error Status Enable (CESE) register
        self.channel.write("*CESE 2,1")
        self.channel.write("*CESE 3,1")
        self.channel.write("*CESE 4,1")
        #Setting the Overload Status Enable (OVSE) register
        self.channel.write("*OVSE 1,1")
        self.channel.write("*OVSE 2,1")
        self.channel.write("*OVSE 3,1")
        self.channel.write("*OVSE 4,1")
        self.channel.write("*OVSE 5,1")
        self.channel.write("*OVSE 6,1")
        self.channel.write("*OVSE 7,1")
        self.channel.write("*OVSE 8,1")

    def errors(self):
        sb = self.channel.query("*STB?")
        sb_bin = f"{int(sb):08b}"
        if( sb_bin[7-6] != '0'): #Do we have an error bit somewhere?
            if( sb_bin[7-5] == '1'): #Do we have a Standard Event Status Error?
                esr = self.channel.query("*ESR?")
                if(int(esr)!=0): #Always true
                    self.logger.error("*"*20)
                    esr_bin = f"{int(esr):08b}"
                    self.logger.error(f"*ESR:{esr}, {esr_bin}")
                    lexe_dict = {0:"No execution error",1:"Illegal value",2:"Wrong token",3:"Unvalid bit",\
                                    16:"Uninitialized curve",17:"Curve full",18:"Curve point out-of-order",\
                                    19:"Curve point past end"}
                    lcme_dict = {0:"No command error",1:"Illegal command",2:"Undefined command",3:"Illegal query",\
                                    4:"Illegal set",5:"Missing parameter(s)",6:"Extra parameter(s)",7:"Null parameter(s)",\
                                    8:"Parameter buffer overflow",9:"Bad floating-point",10:"Bad integer",\
                                    11:"Bad integer token",12:"Bad token value",13:"Bad hex block",14:"Unknown token"}
                    ldde_dict = {1:"Curve erased"}
                    for i in range(len(esr_bin)):#Change
                        if( esr_bin[i] == '1'):
                            bit_num = 7-i
                            self.logger.error(f"Error at bit {str(bit_num)}")
                            if(bit_num==3):
                                dde = self.channel.query("LDDE?")
                                self.logger.error(f"Device Dependent Error: {dde}, {ldde_dict[int(dde)]}")
                                self.logger.error("--Go to page 2-15 of manual")
                            elif(bit_num==4):
                                exe = self.channel.query("LEXE?")
                                self.logger.error(f"Execution Error: {exe}, {lexe_dict[int(exe)]}")
                                self.logger.error("--Go to page 2-14 of manual")
                            elif(bit_num==5):
                                cme = self.channel.query("LCME?")
                                self.logger.error(f"Device Error: {cme}, {lcme_dict[int(cme)]}")
                                self.logger.error("--Go to page 2-15 of manual")
                            else:
                                self.logger.info("Device Error: Look up Error on 2-19")
                    self.logger.error("*"*20)
            if( sb_bin[7-7] == '1' ): #Do we have a Communication Status Error?
                cesr = self.channel.query("CESR?")
                #There is a "Parity Error" every single time we connect from SIM900 to SIM922
                #  Not sure how serious this is, but everything seems to work despite
                if(int(cesr)!=0 and int(cesr)!=128): #Always true
                    cesr_bin = f"{int(cesr):08b}"
                    self.logger.error("*"*20)
                    self.logger.error(f"CESR: {cesr},{cesr_bin}")
                    self.logger.error("Go to page 2-20 of manual")
                    self.logger.error("*"*20)
            if( sb_bin[7-0] == '1' ): #Do we have an Overload Status Error?
                ovsr = self.channel.query("OVSR?")
                if(int(ovsr)!=0): #Always true
                    ovsr_bin = f"{int(ovsr):08b}"
                    self.logger.error("*"*20)
                    self.logger.error(f"OVSR: {ovsr}, {ovsr_bin}")
                    for i in range(len(ovsr_bin)):
                        if( ovsr_bin[i] == '1'):
                            bit_num = 7-i
                            self.logger.error("Error at bit "+str(bit_num))
                            if bit_num<4:
                                problem = "Hardward Overload (R >~ 1500 Ohms)"
                            else:
                                problem = "Curve Out-of-range (resistance measured is "\
                                    "ouside of slected calibration curve)"
                            n = (bit_num)%4 +1
                            self.logger.error(f"--{problem} for curve {n}")
                    self.logger.error("Go to page 2-21 of manual")
                    self.logger.error("*"*20)
            raise RuntimeError("Fix the above problem(s)")

    def get_idn(self):
        ''''Typical command to verify that we are communicating with correct instrument: prints
        SIM900 response to screen'''
        self.channel.write(f"'{self.ESC}'")
        idn = self.channel.query('*IDN?') 
        self.logger.info( idn )
        self.channel.write(f"CONN {self.temp_port},'{self.ESC}'")
        return idn


    def _talk_to_SIM(self, f, *args):
        '''A wrapper function to send messages to SIM922

        Parameters:
        `f` function: a function which interacts with SIM922 via `read()`, `write()`, and `query()`
        `*args`, additional arguments that `f` needs'''
        #-----------------------------------------------
        to_return = None
        try:
            to_return = f(*args)
        except pyvisa.errors.VisaIOError:
            self.logger.error("Error: unable to read SIM response.")
            self.errors()
            #The following should hopefully never run
            raise RuntimeError("A problem as slipped through the errors() function")
        self.errors()
        self.logger.info("-"*20)
        #-----------------------------------------------
        return to_return
 
    def get_temp(self, c: int, n:int=None)->float|np.ndarray:
        '''Prints and returns current temperature

        Parameters:
        `c`int: which input to deal with (1-4 only)
        `n`int: optional parameter, number of immediate readings

        Returns:
        float or np.adarray, for `n`=1 or `n`>1
        '''
        def _get_temp( c: int, n:int):
            if( n is None ):
                temp = self.channel.query(f'TVAL? {c}')
                self.logger.info(f"{temp} K")
                return temp
            else:
                if( n == 0 ):
                    self.logger.info("Indefinite Stream not implemented yet")
                    return 0
                self.channel.write(f'TVAL? {c},{n}')
                to_return = np.empty(n)
                for i in range(n):
                    #We may need to add sleep(0.1)?
                    temp = self.channel.read()
                    self.logger.info(f"{temp} K")
                    to_return[i]=temp
                return to_return
        return self._talk_to_SIM( _get_temp, c, n)

    def get_volt(self, c: int, n:int=None)->float|np.ndarray:
        '''Prints and returns current voltage

        Parameters:
        `c`int: which input to deal with (1-4 only)
        `n`int: optional parameter, number of immediate readings

        Returns:
        float or np.adarray, for `n`=1 or `n`>1
        '''
        def _get_volt( c: int, n:int):
            if( n is None ):
                volt = self.channel.query(f'VOLT? {c}')
                self.logger.info(f"{volt} V")
                return volt
            else:
                if( n == 0 ):
                    self.logger.info("Indefinite Stream not implemented yet")
                    return 0
                self.channel.write(f'VOLT? {c},{n}')
                to_return = np.empty(n)
                for i in range(n):
                    #We may need to add sleep(0.1)?
                    volt = self.channel.read()
                    self.logger.info(f"{volt} V")
                    to_return[i]=volt
                return to_return
        return self._talk_to_SIM( _get_volt, c, n)

    def view_points(self, c:int )->list:
        '''Prints curve attributes: type, name, number of inputs; as well as each data points

        Parameters:
        `c`:int, which input to deal with (1-4 only)

        Returns:
        list, a list of floats, representing the data points in the format [sensor value, temperature, sensor value,...]
            Note: the data is formatted in the same way the curve is (etiher linear or log_10)
        '''
        def _get_curv( c:int):
            curve_type,name,n = self.channel.query(f"CINI? {c}").split(',')
            names = ["Linear","SemiLogT","SemiLogV","LogLog"]
            self.logger.info(f"Curve namne: {name}, {names[int(n)-1]}")
            self.logger.info(f"Curve type: {curve_type}")
            self.logger.info(f"Number of Inputs: {n}")
            n = int(n.strip())
            if( n==1 ):
                self.logger.info("You cannot access data for a curve with one point (add a dummy to view)")
            else:
                for i in range(n):
                    self.logger.info(self.channel.query(f"CAPT? {c}, {i+1}"))
        return self._talk_to_SIM( _get_curv, c)

    def set_points(self, c:int, axis_type:int=None, name:str=None, data:list=None ):
        """
        Multi-purpose function, to initialize a sensor curve and / or add data to said curve
        Set `axis_type` (and `name`) to initialize sensor calibration, set `data` to add data points\n
        
        Parameters:
        `c`:int, which input curve to deal with
        `axis_type`:int, an optional parameter, to define the type of the curve
            -> 0: Linear | volts, kelvin
            -> 1: SemiLogT | volts, log_{10}(kelvin)
            -> 2: SemiLogV | log_{10}(volts), kelvin
            -> 3: LogLog | log_{10}(volts), log_{10}(kelvin)
        `name`:str, an optional parameter to be given iff `axis_type` is given as well
        `data`:list, a list of float values that correspond to [sensor value, temperature], in the units\
            specified for curve `c`. Multiple point pairs can be given, but the senor value must be in\
            increasing order
        """
        if( axis_type is not None ):
            if( axis_type in [0,1,2,3]):
                response = input("Notice: are you sure you want to change type of curve? (y/n)\
                                 \n\tDoing this will delete previous data ")
                if( response.lower() in ['y', 'yes']):
                    if name is None:
                        raise ValueError("Changing curve type requires a new name,\
                        please provide")
                    if( len(name)>15 or len(name)<1):
                        raise ValueError("The name can be 15 char max")
                    if( ','  in name or ';'  in name):
                        raise ValueError("The name can not have the \',\' or \';\' characters")
                    def _sensor_calibrate( c:int, axis_type:int, name:str):
                        self.channel.write(f"CINI {c},{axis_type},'{name}'")
                    self._talk_to_SIM( _sensor_calibrate, c, axis_type, name)
                    self.logger.info(f"Updated Channel {c} Curve Successfully")
                else:
                    return
        if( data is not None ):
            if( len(data) % 2 != 0):
                raise ValueError("Every data point requires 2 values: raw sensor \
                voltage and temerature")
            if( data[::2] != sorted(data[::2])):
                raise ValueError("Sensor points (voltage) must be added in increasing order")
            def _sensor_add_points( c:int, data:list):
                try:
                    for i in range(int(len(data)/2)):
                        self.channel.write(f"CAPT {c},{data[2*i]},{data[2*i+1]}")
                        sleep(0.20)
                except:
                    raise ValueError("Loading data failed--delete curve and try again\n" \
                    "Hint: make sure the data you ordered is in increasing order of sensor" \
                        " value (including preexisting data)")
                self.logger.info(f"Attempted to add {int(len(data)/2)} points")
            self._talk_to_SIM( _sensor_add_points, c, data )
       
    def set_curve(self, c:int, j:int=None)->int:
        '''Switches between build-in and user-defined calibration curves.
        
        Parameters:
        `c`:int, which input to deal with (1-4 only)
        `j`:int, optional parameter for setting curve `c` (0 or 1 only)
            -> 0: Standard, the built-in data
            -> 1: User defined, from previous user input
        While user data stored in a curve is non-volatile, the defult calibration curve is 0, Built-In
        Returns:
        int, the current value for curve `c`
        '''
        names = ["Built-In","User Defined"]
        def _set_curve( c:int, j:int ):
            if( j is None ):
                x = self.channel.query(f"CURV? {c}")
                self.logger.info(f"Curve type: {x}, {names[int(x)]}")
                return x
            else:
                self.channel.write(f"CURV {c},{j}")
                self.logger.info(f"Curve type: {str(j)}, {names[j]}")
                return j
        return self._talk_to_SIM( _set_curve, c,j )
    
    def update_file(self, c:int, interval_on_screen:int):
        with open('temperature_data.txt', 'r') as file:
            lines = file.readlines()
        with open('temperature_data.txt', 'w') as file:
            if( len(lines) > interval_on_screen ):
                lines.pop(0)
            start_time = int(lines[0].split(",")[0]) if( len(lines) > 0 ) else  0
        
            for i, line in enumerate(lines):
                lines[i] = line.strip().split(",")[1]
            try:
                temperature = self.channel.query(f'TVAL? {c}')
            except pyvisa.errors.VisaIOError:
                self.logger.error("Error: unable to read SIM response.")
                self.errors()
                #The following should hopefully never run
                raise RuntimeError("A problem as slipped through the errors() function")
            lines.append(f"{temperature}")
            file.write('\n'.join(f"{i+start_time},{temp}" for i,temp in enumerate(lines)))
