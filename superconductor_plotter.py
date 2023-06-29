import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit



if __name__ == "__main__":
    with open("data_from_4_25_run.txt","r") as file:
        lines = file.readlines()


    x = list()
    y = list()
    for line in lines[1:]:
        x_data,y_data = line.strip().split(",")
        x.append(int(x_data))
        y.append(float(y_data))


    popt, pcov = curve_fit(lambda t, a, b, c: a * np.exp(b * t) + c, x[500::], y[500::],p0=(100, -1/500, 77))

    a = popt[0]
    b = popt[1]
    c = popt[2]
    print(a)
    print(b)
    print(c)
    x_fitted = np.linspace(np.min(x[500::]), np.max(x[500::]), 100)
    y_fitted = a * np.exp(b * x_fitted) + c


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(title="Fitting Cool-down of baseplate with inner can\nand radiation shield (turned off)")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Temperature [K]")

    ax.plot(x,y,label="Measured Data")
    ax.plot(x_fitted, y_fitted, 'k', label='Fitted curve')


    plt.show()

    '''
    Fit Data:
    143.6143296470198
    -0.0016538231448511278
    79.03390250594735
    '''