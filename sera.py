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
w=Calculos.CI_MPRR(data[0],data[1],data[2],data[7])
wf=Calculos.CI_MPRR(data[3],data[4],data[5],data[7])
t = np.arange(t1, t2, (t2-t1)/(n-1))

for i in range(0,3):
    M=Calculos.pos_vel_as(0,float(data[6]),float(wf[i]),float(w[i]),0,0)
    if i==1:
        pos_final_x= M[3]*t**3 + M[2]*t**2 + M[1]*t + M[0]
        vel_final_x = 3*M[3]*t**2 + 2*M[2]*t + M[1]
    if i==2:
        pos_final_y = M[3]*t**3 + M[2]*t**2 + M[1]*t + M[0]
        vel_final_y = 3*M[3]*t**2 + 2*M[2]*t + M[1]
    else:
        pos_final_z = M[3]*t**3 + M[2]*t**2 + M[1]*t + M[0]
        vel_final_z = 3*M[3]*t**2 + 2*M[2]*t + M[1]

ax.plot(pos_final_x, pos_final_y, pos_final_z)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


tkinter.mainloop()