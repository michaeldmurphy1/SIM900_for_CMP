import matplotlib.pyplot as plt
import numpy as np
import scipy


def convert(volt:float)->float:
    #This is from both fitting_V(T)_curve.py (d1 & d2) and TeachSpin (d3)
    d1 = 1.1314 # [V/K]
    d2 = 0.00004501 # [V/K]
    d3 = 0.000405 # [V/K]

    temp = lambda volt: (d1 - volt)/(d3 * scipy.special.lambertw(np.exp(d2/d3)*(d1-volt)/d3))
    #voltage = lambda temp: d1 - (d2 * temp) - (d3 * temp * np.log(temp))
    return temp(volt)



if __name__ == "__main__":
    # open file in format of "mV across sample, mV across diode"
     with open("4-25-data.txt","r") as file:
          lines = file.readlines()

     x = list()
     y = list()
     for line in lines[1:]:
          y_data,x_data = line.strip().split(",")
          x.append(convert(float(x_data)*10**-3))
          y.append(float(y_data)/1000)

     fig = plt.figure()
     ax = fig.add_subplot(111)
     ax.set(title="Resistance vs temperature of superconductor sample")
     ax.set_xlabel("Temperature [K]")
     ax.set_ylabel("Resistance")


     ax.plot(x,y)

     plt.show()
