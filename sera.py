'''
import tkinter
 
F1 = tkinter.Frame()
s = tkinter.Scrollbar(F1)
L = tkinter.Listbox(F1)
 
s.pack(side=tkinter.RIGHT, fill=tkinter.Y)
L.pack(side=tkinter.LEFT, fill=tkinter.Y)
 
s['command'] = L.yview
L['yscrollcommand'] = s.set
 
for i in range(30): 
   L.insert(tkinter.END, str(i))
 
F1.pack(side=tkinter.TOP)
 
F2 = tkinter.Frame()
lab = tkinter.Label(F2)
 
def poll():
    lab.after(200, poll)
    sel = L.curselection()
    lab.config(text=str(sel))
 
lab.pack()
F2.pack(side=tkinter.TOP)
 
poll()
tkinter.mainloop()
'''

import tkinter
from turtle import end_fill
import numpy as np
import Calculos, interface_pestañas
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
ax = fig.add_subplot(111, projection="3d")

data=interface_pestañas.data_3D()


ax.plot(pos_final_x, pos_final_y, pos_final_z)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


tkinter.mainloop()