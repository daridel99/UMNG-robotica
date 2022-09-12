#IMPORTAMOS "tkinter"
from tkinter import *
import tkinter
from tkinter import ttk
import tkinter.font as tkFont
import math as mt
from tkinter import HORIZONTAL, PhotoImage, StringVar, Widget
from ctypes import sizeof
import tkinter  as tk
from tkinter import *
import numpy as np
from time import sleep
from tkinter import messagebox
from PIL import Image, ImageTk
import serial, serial.tools.list_ports
from tkinter import ttk

#Info
def info():
    messagebox.showinfo("Informacion de uso",
"""
Modo de uso:\nDesplazar cada slider para mover
las articulaciones del brazo robotico o digitar el
valor de lo que se quiere mover para luego presionar
el boton de envio correspondiente, se pretende obtener
las matrices individuales y totales en tiempo real.\n
Digitar el valor del efector final y presionar el boton
de calcular para obtener los distintos valores de juntura.
""")

def show_values1():
    print("Calculando...")

#VENTANA PRINCIPAL.
root = tkinter.Tk()
root.title('Controles de Manipuladores Roboticos')
root.geometry("1366x768")
nombre = StringVar()
numero = IntVar()

#INCLUIMOS PANEL PARA LAS PESTAÑAS.
nb = ttk.Notebook(root)
nb.pack(fill='both',expand='yes')

#CREAMOS PESTAÑAS
pI = ttk.Frame(nb)
p1 = ttk.Frame(nb)
p2 = ttk.Frame(nb)   

####################### pestaña 1

#Frame Informacion (Contenedor)
fontStyle_T = tkFont.Font(family="Lucida Grande", size=12)
fi=LabelFrame(pI, 
text='Interfaz Grafica Para Controlar Manipuladores Roboticos', 
labelanchor='n', 
font=fontStyle_T)
fi.place(relwidth=1, relheight=1)

var= StringVar()
fontStyle = tkFont.Font(family="Lucida Grande", size=15)
etiqueta = Label(fi, textvariable=var , relief=FLAT , pady=10, font=fontStyle)
var.set("""
Dario Delgado - 1802992 \n 
Brayan Ulloa - 1802861 \n 
Santiago Tobar - 1803015 \n
Fernando Llanes - 1802878 \n
Karla Baron - 1803648 \n 
Sebastian Niño - 1803558
""")
etiqueta.place(relwidth=0.97,relheight=0.7)

#Logos
img= PhotoImage(file='./LOGOUMNG.png')
img_zoom=img.zoom(2)
widget = Label(fi, image=img_zoom)
widget.place(relwidth=0.3,relheight=0.6)

img1= PhotoImage(file='./icon.png')
img1_zoom=img1.zoom(2)
widget1 = Label(fi, image=img1_zoom)
widget1.place(x=1050, y=150)

#Boton Info
Binf = Button(fi,
             text="Modo de uso",
             relief=GROOVE,
             command=info   )
Binf.grid(column=1,row=1)

######################## pestaña 2

#Frame Manipuladores (Contenedor)
frm=LabelFrame(p1,relief="raised")
frm.place(relwidth=1, relheight=1)

#Frame Manipulador1 Scara (Contenedor)
frm1=LabelFrame(frm,text='DK', labelanchor='n')
frm1.place(relwidth=1, relheight=0.64)

#Base
#Slider
angulo1=Scale(frm1,
                from_=0,
                to=122,
                orient = HORIZONTAL,
                length=300,
                troughcolor='gray',
                width = 30,
                cursor='dot',
                label = 'Desplazamiento Base',
                  ).place(rely=0, relwidth=1/5, relheight=1/4)
#Text_Box
txt_edit_ang0 = tk.Text(frm1,width=3)
txt_edit_ang0.place(relx=1/5, rely=0.13, relheight=1/8-0.03)
txt_edit_ang0.insert(tk.END, "0")
        
#Brazo
#Slider
angulo2= Scale(frm1,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Brazo'  )
angulo2.place(rely=((1/5)+0.05), relwidth=1/5, relheight=1/4)
#Text_Box
txt_edit_ang1 = tk.Text(frm1, width = 3)
txt_edit_ang1.place(relx=1/5, rely=2/8+0.13, relheight=1/8-0.03)
txt_edit_ang1.insert(tk.END, "0")

#Antebrazo
#Slider
angulo3= Scale(frm1,              
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Codo'  )
angulo3.place(rely=((3/5)-0.1), relwidth=1/5, relheight=1/4)
#Text_Box
txt_edit_ang2 = tk.Text(frm1, width = 3)
txt_edit_ang2.place(relx=1/5, rely=4/8+0.13, relheight=1/8-0.03)
txt_edit_ang2.insert(tk.END, "0")

#Muñeca
#Slider
angulo4= Scale(frm1,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Muñeca'  )
angulo4.place(rely=((4/5)-0.05), relwidth=1/5, relheight=1/4)
#Text_Box
txt_edit_ang3 = tk.Text(frm1, width = 3)
txt_edit_ang3.place(relx=1/5, rely=6/8+0.13, relheight=1/8-0.03)
txt_edit_ang3.insert(tk.END, "0")



#Frame Manipulador2 Antropomorfico (Contenedor)
frm2=LabelFrame(frm,text='IK', labelanchor='n')
frm2.place(rely=0.65, relwidth=1, relheight=0.35)

#Text_Box
txt_edit_xS = tk.Text(frm2, width=3)
txt_edit_xS.place(relx=1/10,rely=1/10+0.01, relheight=1/6-0.05)
txt_edit_xS.insert(tk.END, "0")
        
#Text_Box
txt_edit_yS = tk.Text(frm2, width = 3)
txt_edit_yS.place(relx=1/10, rely=3/10+0.01, relheight=1/6-0.05)
txt_edit_yS.insert(tk.END, "0")

#Text_Box
txt_edit_zS = tk.Text(frm2, width = 3, height=1.8)
txt_edit_zS.place(relx=1/10, rely=5/10+0.01, relheight=1/6-0.05)
txt_edit_zS.insert(tk.END, "0")
        
Calcular1=Button(frm2, text='Calcular', activebackground='yellow', command=show_values1)
Calcular1.place(relx=1/10-0.01, rely=7/10+0.01, relheight=1/6-0.05)

frmdh2=LabelFrame(frm2,relief="raised")
frmdh2.place(relx=0.35, rely=0.15, relwidth=0.42, relheight=0.39)

etiqueta1 = tk.Label(frmdh2, text="Link 1", fg="black", bg="yellow").grid(column=0, row=0)
text1 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2, orient="horizontal", command=text1.xview)
text1.configure(xscrollcommand=textHsb.set)
text1.grid(row=0, column=1, sticky="nsew")
textHsb.grid(row=1, column=1, sticky="ew")

etiqueta2 = tk.Label(frmdh2, text="Link 2", fg="black", bg="yellow").grid(column=0, row=3)
text2 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2, orient="horizontal", command=text2.xview)
text2.configure(xscrollcommand=textHsb.set)
text2.grid(row=3, column=1, sticky="nsew")
textHsb.grid(row=4, column=1, sticky="ew")

blanco = Label(frmdh2, width=10)
blanco.grid(column=2, row=0)
blanco = Label(frmdh2, width=10)
blanco.grid(column=2, row=1)

etiqueta3 = tk.Label(frmdh2, text="Link 3", fg="black", bg="yellow").grid(column=3, row=0)
text3 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2, orient="horizontal", command=text3.xview)
text3.configure(xscrollcommand=textHsb.set)
text3.grid(row=0, column=4, sticky="nsew")
textHsb.grid(row=1, column=4, sticky="ew")

etiqueta4 = tk.Label(frmdh2, text="Link 4", fg="black", bg="yellow").grid(column=3, row=3)
text4 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2, orient="horizontal", command=text4.xview)
text4.configure(xscrollcommand=textHsb.set)
text4.grid(row=3, column=4, sticky="nsew")
textHsb.grid(row=4, column=4, sticky="ew")

def blanco(n):
    blanco = Label(frmdh1, width=6)
    blanco.grid(column=4+n, row=0)

#Frame Matrices Manipulador 1 Scara (Contenedor)
frmdh1=LabelFrame(frm1,relief="raised")
frmdh1.place(relx=0.24, relwidth=1.1, relheight=1)

for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1, width=12)
        cell.grid(row=r, column=c, ipady=4)

blanco(0)

blanco(5)

for r in range(0, 4):
    for c in range(11, 15):
        cell = Entry(frmdh1, width=12)
        cell.grid(row=r, column=c, ipady=4)
        
blanco = Label(frmdh1, width=10)
blanco.grid(column=1, row=6)

for r in range(8, 12):
    for c in range(5, 9):
        cell = Entry(frmdh1, width=12)
        cell.grid(row=r, column=c, ipady=4)
 
blanco = Label(frmdh1, width=10)
blanco.grid(column=1, row=14)

for r in range(16, 20):
    for c in range(0, 4):
        cell = Entry(frmdh1, width=12)
        cell.grid(row=r, column=c, ipady=4)

for r in range(16, 20):
    for c in range(11, 15):
        cell = Entry(frmdh1, width=12)
        cell.grid(row=r, column=c, ipady=4)

#########################
Titulos_l1 = Label(frmdh1, width=10,text="Link 1")
Titulos_l1.grid(column=1, row=6)
Titulos_l2 = Label(frmdh1, width=10,text="Link 2")
Titulos_l2.grid(column=12, row=6)
Titulos_l3 = Label(frmdh1, width=10,text="Link 3")
Titulos_l3.grid(column=1, row=22)
Titulos_l4 = Label(frmdh1, width=10,text="Link 4")
Titulos_l4.grid(column=12, row=22)
Titulos_lT = Label(frmdh1, width=10,text="Total")
Titulos_lT.grid(column=6, row=14)
###########################
Envio1=Button(frmdh1, text='Envio', activebackground='yellow', command=show_values1)
Envio1.grid(column=6,row=22)

###################### pestaña 3

#Frame Manipuladores (Contenedor)
frmA=LabelFrame(p2,relief="raised")
frmA.place(relwidth=1, relheight=1)

#Frame Manipulador1 Scara (Contenedor)
frm1A=LabelFrame(frmA,text='DK', labelanchor='n')
frm1A.place(relwidth=1, relheight=0.64)

#Base
#Slider
angulo1A=Scale(frm1A,
                from_=0,
                to=180,
                orient = HORIZONTAL,
                length=300,
                troughcolor='gray',
                width = 30,
                cursor='dot',
                label = 'Rotación Base',
                  ).place(rely=0, relwidth=1/5, relheight=0.3)
#Text_Box
txt_edit_ang0A = tk.Text(frm1A,width=3)
txt_edit_ang0A.place(relx=1/5, rely=0.13, relheight=1/8-0.03)
txt_edit_ang0A.insert(tk.END, "0")
        
#Brazo
#Slider
angulo2A= Scale(frm1A,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Brazo'  
              ).place(rely=((1/5)+0.05), relwidth=1/5, relheight=0.3)
#Text_Box
txt_edit_ang1A = tk.Text(frm1A, width = 3)
txt_edit_ang1A.place(relx=1/5, rely=2/8+0.13, relheight=1/8-0.03)
txt_edit_ang1A.insert(tk.END, "0")

#Antebrazo
#Slider
angulo3A= Scale(frm1A,              
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Codo'  
              ).place(rely=((3/5)-0.1), relwidth=1/5, relheight=0.3)
#Text_Box
txt_edit_ang2A = tk.Text(frm1A, width = 3)
txt_edit_ang2A.place(relx=1/5, rely=4/8+0.13, relheight=1/8-0.03)
txt_edit_ang2A.insert(tk.END, "0")

#Frame Manipulador2 Antropomorfico (Contenedor)
frm2A=LabelFrame(frmA,text='IK', labelanchor='n')
frm2A.place(rely=0.65, relwidth=1, relheight=0.35)

#Text_Box
txt_edit_xA = tk.Text(frm2A, width=3)
txt_edit_xA.place(relx=1/10,rely=1/10+0.01, relheight=1/6-0.05)
txt_edit_xA.insert(tk.END, "0")
        
#Text_Box
txt_edit_yA = tk.Text(frm2A, width = 3)
txt_edit_yA.place(relx=1/10, rely=3/10+0.01, relheight=1/6-0.05)
txt_edit_yA.insert(tk.END, "0")

#Text_Box
txt_edit_zA = tk.Text(frm2A, width = 3, height=1.8)
txt_edit_zA.place(relx=1/10, rely=5/10+0.01, relheight=1/6-0.05)
txt_edit_zA.insert(tk.END, "0")
        
Calcular2=Button(frm2A, text='Calcular', activebackground='yellow', command=show_values1)
Calcular2.place(relx=1/10-0.01, rely=7/10+0.01, relheight=1/6-0.05)

frmdh2A=LabelFrame(frm2A,relief="raised")
frmdh2A.place(relx=0.4, rely=0.1, relwidth=0.25, relheight=0.8)

etiqueta1 = tk.Label(frmdh2A, text="Link 1", fg="black", bg="yellow").grid(column=0, row=0)
text1A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2A, orient="horizontal", command=text1A.xview)
text1A.configure(xscrollcommand=textHsb.set)
text1A.grid(row=0, column=1, sticky="nsew")
textHsb.grid(row=1, column=1, sticky="ew")

etiqueta2 = tk.Label(frmdh2A, text="Link 2", fg="black", bg="yellow").grid(column=0, row=3)
text2A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2A, orient="horizontal", command=text2A.xview)
text2A.configure(xscrollcommand=textHsb.set)
text2A.grid(row=3, column=1, sticky="nsew")
textHsb.grid(row=4, column=1, sticky="ew")

blanco = Label(frmdh2A, width=10)
blanco.grid(column=0, row=2)

etiqueta3 = tk.Label(frmdh2A, text="Link 3", fg="black", bg="yellow").grid(column=0, row=6)
text3A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2A, orient="horizontal", command=text3A.xview)
text3A.configure(xscrollcommand=textHsb.set)
text3A.grid(row=6, column=1, sticky="nsew")
textHsb.grid(row=7, column=1, sticky="ew")

blanco = Label(frmdh2A, width=10)
blanco.grid(column=0, row=5)

def blancoA(n):
    blanco = Label(frmdh1A, width=6)
    blanco.grid(column=4+n, row=0)

#Frame Matrices Manipulador 1 Scara (Contenedor)
frmdh1A=LabelFrame(frm1A,relief="raised")
frmdh1A.place( relx=0.35, rely=0.01, relwidth=0.53, relheight=0.9)

for r in range(1, 5):
    for c in range(1, 5):
        cell = Entry(frmdh1A, width=12)
        cell.grid(row=r, column=c, ipady=4)

blancoA(0)

blancoA(5)

for r in range(1, 5):
    for c in range(10, 14):
        cell = Entry(frmdh1A, width=12)
        cell.grid(row=r, column=c, ipady=4)
        
blanco = Label(frmdh1A, width=10)
blanco.grid(column=1, row=6)

blanco = Label(frmdh1A, width=10)
blanco.grid(column=10, row=7)
blanco = Label(frmdh1A, width=10)
blanco.grid(column=1, row=14)

for r in range(15, 19):
    for c in range(1, 5):
        cell = Entry(frmdh1A, width=12)
        cell.grid(row=r, column=c, ipady=4)

for r in range(15, 19):
    for c in range(10, 14):
        cell = Entry(frmdh1A, width=12)
        cell.grid(row=r, column=c, ipady=4)

#########################
Titulos_l1 = Label(frmdh1A, width=10,text="Link 1")
Titulos_l1.grid(column=2, row=6)
Titulos_l2 = Label(frmdh1A, width=10,text="Link 2")
Titulos_l2.grid(column=11, row=6)
Titulos_l3 = Label(frmdh1A, width=10,text="Link 3")
Titulos_l3.grid(column=2, row=20)
Titulos_lT = Label(frmdh1A, width=10,text="Total")
Titulos_lT.grid(column=11, row=20)
###########################

Envio2=Button(frmdh1A, text='Envio', activebackground='yellow', command=show_values1)
Envio2.grid(column=7,row=22)

#AGREGAMOS PESTAÑAS CREADAS
nb.add(pI,text='Portada')
nb.add(p1,text='Robot Scara')
nb.add(p2,text='Robot Antropomorfico (RRR)')

root.mainloop()