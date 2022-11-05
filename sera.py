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

def plot_3D(pos_final_x, pos_final_y, pos_final_z):
    ax.plot(pos_final_x, pos_final_y, pos_final_z)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


tkinter.mainloop()
'''

from random import randint

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# create empty lists for the x and y data
x = []
y = []

# create the figure and axes objects
fig, ax = plt.subplots()
# function that draws each frame of the animation
def animate(i):
    pt = randint(1,9) # grab a random integer to be the next y-value in the animation
    x.append(i)
    y.append(pt)

    ax.clear()
    ax.plot(x, y)
    ax.set_xlim([0,20])
    ax.set_ylim([0,10])

# run the animation
ani = FuncAnimation(fig, animate, frames=20, interval=500, repeat=False)

plt.show()