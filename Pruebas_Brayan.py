import math as mt
import numpy as np
from sympy import  *
import Widgets as Wd
import tkinter as tk


Ventana = tk.Tk()
Ventana.title('Controles de Manipuladores Roboticos')
width=Ventana.winfo_screenwidth()  
height= Ventana.winfo_screenheight() 
Ventana.geometry("%dx%d" % (width, height))

Gr1=Wd.Grafica(Ventana, r'Posición $q_1$', "q[°]", 0, 0)
Gr1.Linea(5, 0, 50, 20, [1,2,3,4,5])


Ventana.mainloop()


fig4,ax4=plt.subplots(facecolor='#B5B2B2')
ax4.set_ylabel('[V]')
ax4.set_xlabel('[seg]')
plt.title("Velocidad q1",color='k',size=12,family="Arial")
ax4.set_xlim(0, timeing)
ax4.set_ylim(0, ampl+(Fnc.Signo(ampl)*0.5))
canvas4=FigureCanvasTkAgg(fig4,master=frmGraf)
canvas4.get_tk_widget().place(rely=1/3+0.04, relwidth=1/3+0.02, relheight=1/3+0.05)    
line4,=ax4.plot([],[],color='k',linestyle='solid',linewidth=2)
paso=timeing/res
line4.set_data(np.arange(0, timeing, paso, dtype=float), data)

fig3,ax3=plt.subplots(facecolor='#85888A')   
ax3.set_ylabel('[q]')
ax3.set_xlabel('[seg]')
plt.title("Posición q3",color='k',size=12,family="Arial")
ax3.set_xlim(0, timeing)
ax3.set_ylim(ampin, ampl+(Fnc.Signo(ampl)*0.5))
canvas3=FigureCanvasTkAgg(fig3,master=frmGraf)
canvas3.get_tk_widget().place(relx=2/3+0.01, rely=0, relwidth=1/3+0.02, relheight=1/3+0.05)    
line3,=ax3.plot([],[],color='k',linestyle='solid',linewidth=2)
paso=timeing/res
line3.set_data(np.arange(0, timeing, paso, dtype=float), data)