import numpy as np


def convert(temperature:float)->float:
    #This is from both fitting_V(T)_curve.py (d1 & d2) and TeachSpin (d3)
    d1 = 1.1314 # [V/K]
    d2 = 0.00004501 # [V/K]
    d3 = 0.000405 # [V/K]

    voltage = lambda temp: d1 - (d2 * temp) - (d3 * temp * np.log(temp))
    return voltage(temperature)

    again = True
    print("To exit program, enter something not a number.")
    print("The given voltage is mutliplied by 10 to match the PI "
            "Temperature Controller output.")
    while( again ):
        x = input("Type a temperature in Kelvin for a voltage set point: ")
        try:
            x = float(x)
            assert (x >= 77 and x <= 350)
            print(f"{voltage(x)*10} V * 10")
        except AssertionError:
            print("BAD INPUT: please enter a valid temperature")
        except ValueError:
            again = False