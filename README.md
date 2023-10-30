# SIM900_for_CMP

This repository is for use in the Carnegie Mellon University Department of 
Physics Modern Physics lab on Condensed Matter Physics (CMP). Please see
[this manual](https://docs.google.com/document/d/1xsgqqERIqc8ZFpyFgtvWTSyZ0KbxUYtzTdAOM4_Ets4/edit?usp=sharing)
for a summary of the status of the physical experiment

There are two main "bulks" of work: the code to communicate with the SIM900 
from TeachSpin via `Pyvisa` as well as a  `Tkinker`-dependent temperature
visualization.

-------

### Communicating with the SIM900

Utilizing `Pyvisa`, one can interact with the SIM900, specifically the 
SIM922 Diode Temperature Monitor, by creating a `SRS_Device` 
object, as shown in my [example file](example_code.py), to be called from the 
command line.

The functions of `serial_talking.py` are well documented and easy to use.

There are two things a user can do: either get temperature/voltage data, or
configure things to get accurate data.

Code takes minimal input and takes no knowledge of RS-232 communication:
```python
from serial_talking import SRS_Device

if __name__ == "__main__":    
    #Creating obect representing commmunication channel to device
    chan = SRS_Device()
    #Who are we talking to?
    chan.get_idn()
    
    #Syntax for getting data goes as chan.get_temp(n) or chan.get_volt(n), where
    #   'n' represents the SIM922 channel in question (1-4)

    #Call to get temperature for diode on line 1
    chan.get_temp(1)
    #Call to get voltage for diode on line 2
    chan.get_volt(2)
```
All other functions are to store and maniluate "calibration curves," which the SIM
internally uses to read out temperatures from its measurement of voltage.

Note that one can manually determine voltage / temperature conversion, described in
[Chapter 4](https://drive.google.com/file/d/1KoboLt9d973GxG4DLJyS87Yn9WvwgvkH/view?usp=sharing)
of the TeachSpin Cryostat manual, or via the code in the `/temperature_fitting_code` directory. The [wind.py](wind.py) does have a
converter built in for quick PID conversions.

Look at [example_code.py](example_code.py) for an intro to using the command line.

To use the command line, open a terminal and `cd path.to.SIM_Code` (change
directory to the `SIM_Code` repository). From there, assuming you're on the computer
in MA326, one needs to active the `venv` virutal environment with the command 
`venv\Scripts\Activate`, and now all required libraries are accessible and one can simply call 
`python com_line.py` or `python wind.py` to have the desired files run.

### Visualizing Temperature

To give some functionality to this repository, [wind.py](wind.py) has been 
created to accomplish 2 tasks:
1. temperature to voltage conversion, to be used with the TeachSpin PI 
Temperature Controller.
2. live plot of temperature from diodes connected to the SIM922.
The `tkinker` program lives in `wind.py`, yet it is based on code from 
multiple other files, using the `SRS_Device` as described in the secion above.

The `wind.py` file is admitidly a mess as it is creating the required objects to 
populate the Tkinker, but one can understand and manipulate functionality via the
"command" functions at the top of the file, as well as the `graphing.py` file.

Note: the "user defined" curve, mentioned in the tkinker window, requires knowledge of the
`SRS_Device` handling to initially add points to.

-------

While a user of this code need only know how to use the command line to open the
`wind.py` application, it will take a little reading of documenation in the 
[serial_talking.py](serial_talking.py) to be comfortable with adding calibration curves,
and quite a bit more digging into the SIM922 manual to understand how you can manipulate the
`SRS_Device` code. However, a lot of future improvements can be
made though updating `wind.py` functionalities.

Specific Improvement Ideas:
 - Visualize Multiple Thermometers at the same time (really just storing two sets of data and plotting on the same axis twice)
 - Set up curve calibration points from tkinker window
 - update the name `wind.py` to `window.py` becuase two more characters really clears things up
