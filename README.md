# SIM900_for_CMP

This repository is for use in the Carnegie Mellon University Department of Physics Modern Physics lab on Condensed Matter Physics (CMP).

There are two main "bulks" of work: the code to communicate with the SIM900 from TeachSpin via ```Pyvisa``` as well as a 
```Tkinker```-dependent temperature visualization.

### Communicating with the SIM900

Utilizing ```Pyvisa```, one can interact with the SIM900, specifically the SIM922 Diode Temperature Monitor, by creating a ```SRS_Device``` 
object, as shown in my [example file](com_line.py), to be called from the command line.

The functions of '''serial_talking.py``` are well documented and easy to use.

### Visualizing Temperature

To give some functionality to this repository, [wind](wind.py) has been created to accomplish 2 tasks:
1. temperature to voltage conversion, to be used with the TeachSpin PI Temperature Controller
2. live plot of temperature from diodes connected to the SIM922
The ```tkinker``` program lives in ```wind.py```, yet it is based on code from multiple other files
