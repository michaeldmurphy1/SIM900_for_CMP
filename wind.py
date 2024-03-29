#!/usr/bin/env python

import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Sizegrip
import graphing
import temperature_fitting_code.what_volt_for_temp as k_to_v

def kelvin_to_voltage():
    #For top button--converting temperature to voltage
    try:
        kelvin = int(ent_temperature.get())
        assert (kelvin >= 77 and kelvin <= 350)
        voltage = k_to_v.convert(kelvin)
        output = f"{round(voltage*1000, 1)} mV"
    except AssertionError:
        output = "Please enter a valid temperature"
    except ValueError:
        return
    lbl_result["text"] = output

def set_up_graph():    
    #Getting all input from main window
    thermometer_number = int(therm_str.get())
    try:
        curve_type = int(var_switch.get())
        interval_length = int(ent_intv.get())
        range_displayed = int(ent_dure.get())
        name_of_run = ent_nor.get()
        pattern = ("\\","/","?","%","*",":","|","\"","<",">",".",",",";","="," ")
        assert any(i in name_of_run for i in pattern) == False
    except ValueError:
        showerror("Error","Please make sure you are inputing valid integers.")
        return
    except AssertionError:
        showerror("Error","Please input a valid file name.")
        return
    result = graphing.create_animation(thermometer_number,
                      curve_type, interval_length, range_displayed,
                      name_of_run)
    if( result is not None ):
        #There was a problem opening something
        showerror("Error",result)

if __name__ == "__main__":
    # Set up the window
    window = tk.Tk()
    window.title("Diode Thermometer")
    #window.resizable(width=False, height=False)
    #window.minsize(window.winfo_width(), window.winfo_height())

    #Setting up Temperature Conversion Things
    frm_conversion = tk.Frame(master=window)
    frm_temp_entry = tk.Frame(master=frm_conversion)
    ent_temperature = tk.Entry(master=frm_temp_entry, width=15)
    lbl_temp = tk.Label(master=frm_temp_entry, text="K")

    ent_temperature.grid(row=0, column=0, sticky="e")
    lbl_temp.grid(row=0, column=1, sticky="w")
    # Create the conversion Button and result display Label
    btn_convert = tk.Button(
        master=frm_conversion,
        text="\N{RIGHTWARDS BLACK ARROW}",
        command=kelvin_to_voltage
    )
    lbl_result = tk.Label(master=frm_conversion, text="V")
    
    frm_temp_entry.grid(row=0, column=0, padx=10)
    btn_convert.grid(row=0, column=1, pady=10)
    lbl_result.grid(row=0, column=2, padx=10)
    #-------------------------------------------------------------------------
    #Creating dark line
    sep = tk.Frame(master=window, bg="black", height=2, bd=0)
    #-------------------------------------------------------------------------
    #Setting up graph input things
    frm_graph_entry = tk.Frame(master=window)

    #Choosing with Diode
    lbl_therm = tk.Label(master=frm_graph_entry, text="Thermometer:")
    therm_str = tk.StringVar(frm_graph_entry)
    therm_nums = [1,2,3,4]
    therm_str.set(therm_nums[0]) # default value
    therm_drop_down = tk.OptionMenu(frm_graph_entry, therm_str, *therm_nums)
    
    lbl_therm.grid(row=0, column=0, sticky="e")
    therm_drop_down.grid(row=0, column=1, sticky="e")

    #Choosing Curve
    lbl_switch = tk.Label(master=frm_graph_entry, text="Curve:")
    var_switch = tk.StringVar(frm_graph_entry)
    btn_switch_built = tk.Radiobutton(frm_graph_entry, text="Built-In", variable=var_switch,
                                indicatoron=False, value="0", width=10)
    btn_switch_user = tk.Radiobutton(frm_graph_entry, text="User-Defined", variable=var_switch,
                                indicatoron=False, value="1", width=10)
    var_switch.set("0")
    lbl_switch.grid(row=1, column=0, sticky="e")
    btn_switch_built.grid(row=1, column=1, sticky="e")
    btn_switch_user.grid(row=1, column=2, padx=2, sticky="w")

    #Setting Ping intervals
    lbl_intv_l = tk.Label(master=frm_graph_entry, text="Ping intervals:")
    ent_intv = tk.Entry(master=frm_graph_entry, width=15)
    ent_intv.insert(0, "500")
    lbl_intv_r = tk.Label(master=frm_graph_entry, text="ms (min=200)")

    lbl_intv_l.grid(row=2, column=0, sticky="e")
    ent_intv.grid(row=2, column=1, sticky="e")
    lbl_intv_r.grid(row=2, column=2, sticky="w")

    #Setting Range Displayed
    lbl_dure_l = tk.Label(master=frm_graph_entry, text="Range Displayed")
    ent_dure = tk.Entry(master=frm_graph_entry, width=15)
    ent_dure.insert(0, "15")
    lbl_dure_r = tk.Label(master=frm_graph_entry, text="s     (0 for \N{INFINITY})")

    lbl_dure_l.grid(row=3, column=0, sticky="e")
    ent_dure.grid(row=3, column=1, sticky="e")
    lbl_dure_r.grid(row=3, column=2, sticky="w")

    #Setting Name of Run
    lbl_nor_l = tk.Label(master=frm_graph_entry, text="Optional Name of Run:")
    ent_nor = tk.Entry(master=frm_graph_entry, width=15)
    lbl_nor_r = tk.Label(master=frm_graph_entry, text="(leave empty to not save)")

    lbl_nor_l.grid(row=4, column=0, sticky="e")
    ent_nor.grid(row=4, column=1, sticky="e")
    lbl_nor_r.grid(row=4, column=2, sticky="w")


    #Button to create graph
    btn_convert = tk.Button(
        master=frm_graph_entry,
        text="Generate Graph",
        command=set_up_graph,
        bg = "#7E64C2"#"#6F689F"
    )
    btn_convert.grid(row=5, column=1, pady=[5,0])
    #------------------------------------------------------------------------------
    #Section Labels
    lbl_head_convert = tk.Label(master=window, text=" Converting Temperature into Diode Voltage ",
                                font=("bold"), bg = "#A0A0A0", )
    lbl_head_graph = tk.Label(master=window, text="Plotting Temperature", font=("bold"),
                              bg = "#A0A0A0", )

    # Set up the layout using the .pack() geometry manager
    lbl_head_convert.pack(fill=tk.X)
    frm_conversion.pack(fill=tk.Y, expand=tk.TRUE)
    sep.pack(fill=tk.X)
    lbl_head_graph.pack(fill=tk.X)
    frm_graph_entry.pack(fill=tk.Y, expand=tk.TRUE)

    #Finishing touches
    my_sizegrip = Sizegrip(master=window)
    my_sizegrip.pack(side="right", anchor="se")

    window.update()
    window.minsize(window.winfo_width(), window.winfo_height())
    # Run the application
    window.mainloop()
