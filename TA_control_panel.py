import tkinter as tk
import tkinter.ttk as TTK
import TA_fn as TA

window=tk.Tk()
window.title("TA control panel")
window.geometry('400x200')

# add field labels
lbl1=tk.Label(window,text="Save directory:")
lbl1.grid(column=0,row=0)

lbl2=tk.Label(window,text="File name:")
lbl2.grid(column=0,row=1)

lbl3=tk.Label(window,text="Duration:")
lbl3.grid(column=0,row=2)

lbl4=tk.Label(window,text="Gain")
lbl4.grid(column=0,row=3)

lbl5=tk.Label(window,text="# of scans")
lbl5.grid(column=0,row=4)

# add text inputs
direct_entry=tk.Entry(window,width=30)
direct_entry.insert(0,'/home/pi/Documents')
direct_entry.grid(column=1,row=0)

file_name_entry=tk.Entry(window,width=30)
file_name_entry.insert(0,'sample.txt')
file_name_entry.grid(column=1,row=1)

duration_entry=tk.Entry(window,width=6)
duration_entry.insert(0,'2')
duration_entry.grid(column=1,row=2)

n_scan_entry=tk.Entry(window,width=6)
n_scan_entry.insert(0,'1')
n_scan_entry.grid(column=1,row=4)

# add gain options
gain_combo=TTK.Combobox(window,width=4)
gain_combo['values']=(1,2,4,8,16)
gain_combo.current(0)
gain_combo.grid(column=1,row=3)

# add checkboxes
plot_dOD_state=tk.BooleanVar()
plot_dOD_state.set(False)
plot_dOD_chk=tk.Checkbutton(window,text='Plot delta OD',var=plot_dOD_state)
plot_dOD_chk.grid(column=1,row=5)

save_full_data_state=tk.BooleanVar()
save_full_data_state.set(False)
save_full_data_chk=tk.Checkbutton(window,text='Save full data',var=save_full_data_state)
save_full_data_chk.grid(column=1,row=6)

# call flash_photolysis_fn when button is pressed
def pressed_go():
    save_full_data=save_full_data_state.get(); # if true, save full data. False, save binned data
    plot_deltaOD=plot_dOD_state.get(); # True: plot delta OD, false: plot intensity
    direct=direct_entry.get()
    fname=file_name_entry.get() # file name
    n_scan=int(n_scan_entry.get()) # number of scans to combine
    runtime=int(duration_entry.get()) # runtime in seconds
    GAIN=int(gain_combo.get())
    #(direct)
    #print(fname)
    #print(n_scan)
    #print(runtime)
    #print(GAIN)
    #print(save_full_data)
    #print(plot_deltaOD)
    #go_btn.configure(state='disabled')
    # run the actual program
    TA.run_TA(direct,fname,n_scan,runtime,GAIN,save_full_data,plot_deltaOD)
    #go_btn.configure(state='enabled')


# make go button
go_btn=tk.Button(window,text="GO!",bg="green",fg="white",command=pressed_go)
go_btn.grid(column=0,row=7)



window.mainloop()