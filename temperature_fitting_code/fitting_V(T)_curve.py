import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def func( temp, d1, d2 ):
    d3 = 0.000405 # [V/K]
    return d1 - (d2 * temp) - (d3 * temp * np.log(temp))

if __name__ == "__main__":
    #Data points
    p1 = [ 77.0, 0.9925] # [V/K]
    p2 = [295.9, 0.4362] # [V/K]
    #Rearranging data
    x = [p1[0],p2[0]]
    y = [p1[1],p2[1]]
    #Fitting parameters using scipy
    popt, pcov = curve_fit(func,x,y)
    print(f"Parameters of best fit: {popt}")

    #Visualizing Curve and points
    xf=np.linspace(1,350,num=349)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot( x, y, 'ko', label="Temperature Data")
    ax.plot(xf, func(xf, *popt), 'r-', label="Fitted Curve")
    ax.set(xlabel="Temperature [K]",ylabel="Volage Drop [V]",
              title="Fitting Diode to Temperatures")
    ax.legend()
    plt.show()

    """
    The code produces the following fit:
    d1 = 1.1314 [V/K]
    d2 = 0.00004501 [V/K]
    """
