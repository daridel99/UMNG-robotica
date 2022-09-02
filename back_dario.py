#librerias
import math
from tkinter import HORIZONTAL, PhotoImage, StringVar, Widget
#from guizero import App, Slider, TextBox
from ctypes import sizeof
import tkinter  as tk
from tkinter import *
import numpy as np
from time import sleep
from tkinter import messagebox
#from pyfirmata import Arduino, util, SERVO
from PIL import Image, ImageTk
import serial, serial.tools.list_ports
from tkinter import ttk

#configuracion COM
board =serial.Serial(port='COM1', baudrate=9600)
board.write( b'fine\r\n' )
sleep(5) #5 segundos para que establezca la comunicacion

#Funciones de movimiento scada

def servo1(posiciones1):
    #escritura de angulo
    board.write(b'Eb')
    board.write(posiciones1.encode())
    board.write(b'\r\n')

def servo2(posiciones2):
    #escritura de angulo
    board.write(b'Ebr')
    board.write(posiciones2.encode())
    board.write(b'\r\n')

def servo3(posiciones3):
    #escritura de angulo
    board.write(b'Eab')
    board.write(posiciones3.encode())
    board.write(b'\r\n')

def servo4(posiciones4):
    #escritura de angulo
    board.write(b'Em')
    board.write(posiciones4.encode())
    board.write(b'\r\n')

#Funciones de movimiento atropomorfico

def Aservo1(Aposiciones1):
    #escritura de angulo
    board.write(b'Ab')
    board.write(Aposiciones1.encode())
    board.write(b'\r\n')

def Aservo2(Aposiciones2):
    #escritura de angulo
    board.write(b'Abr')
    board.write(Aposiciones2.encode())
    board.write(b'\r\n')

def Aservo3(Aposiciones3):
    #escritura de angulo
    board.write(b'Aab')
    board.write(Aposiciones3.encode())
    board.write(b'\r\n')

#gripper
globals()["clickeo"]=True
def abrir():
    if  globals()["clickeo"]:
        globals()["clickeo"]=globals()["clickeo"]^1
        BoA["bg"]="red"
        board.write(b'E0 \r\n')
    
    else:
        globals()["clickeo"]=globals()["clickeo"]^1
        BoA["bg"]="green"
        board.write(b'E1 \r\n')

globals()["clickeo1"]=True
def cerrar():
    if  globals()["clickeo1"]:
        globals()["clickeo1"]=globals()["clickeo1"]^1
        BoC["bg"]="red"
        board.write(b'A0 \r\n')
    else:
        globals()["clickeo1"]=globals()["clickeo1"]^1
        BoC["bg"]="green"
        board.write(b'A1 \r\n')

#-------------------------info
def info():
    messagebox.showinfo("Informacion",
                          "Modo de uso:\nDesplazar cada slider para mover las articulaciones del brazo robotico para realizar el movimiento de cada articulacion \n o digitar el valor de lo que se quiere mover para \n luego presionar el boton de envio correspondiente \n se pretende obtener las matrices individuales y totales en tiempo real"  )

#----------------------------serial
def close():
    board.write(b'bye\r\n')
    board.close()
    #----------- ejemplo de llenado
    for n in range(1,11):
        for i in range(0,4):
            for j in range(0,4):
                globals()["arr"+ str(n) +"_" + str(i) + str(j)].set(str(n)+"_"+str(i)+str(j)) #globals()
#----------------------------
####################################
#----------------------------envio de datos por boton
def show_values1():

    #ang1 
    board.write(b'Eb')
    board.write(txt_edit_ang1.get(1.0, tk.END).encode())

    #ang2 
    board.write(b'Ebr')
    board.write(txt_edit_ang2.get(1.0, tk.END).encode())

    #ang3 
    board.write(b'Eab')
    board.write(txt_edit_ang3.get(1.0, tk.END).encode())

def show_values2():
    
    #ang1 
    board.write(b'Ab')
    board.write(txt_edit_ang4.get(1.0, tk.END).encode())

    #ang2 
    board.write(b'Abr')
    board.write(txt_edit_ang5.get(1.0, tk.END).encode())

    #ang3 
    board.write(b'Aab')
    board.write(txt_edit_ang6.get(1.0, tk.END).encode())




root = Tk()

root.title("Control de Manipulador Robotico")
root.minsize(1366,768)

#Widgets ############################
#scrollbar = tk.Scrollbar(root)
#scrollbar.config(command=root.yview)
#root.scrollbar = tk.Scrollbar(root)
#root.scrollbar.pack(side="right", fill="y")
####################################

#logo
img= PhotoImage(file="LOGOUMNG.png")
widget = Label(root, image=img)
#widget.grid(column=1, row=1)

img1= PhotoImage(file="icon.png")
widget1 = Label(root, image=img1)
#widget1.grid(column=3, row=1)

globals()["color_boton1"]=StringVar()
color_boton1='green'

#etiqueta 1
var= StringVar()
etiqueta = Label(root, textvariable=var , relief=FLAT , pady=5)
var.set("Dario Delgado - 1802992 \n Brayan Ulloa - 1802861 \n Santiago Tobar - 1803015 \n Fernando Llanes - 1802878 \n Karla Baron - 1803648 \n Sebastian Niño - 1803558")
#etiqueta.grid(column=2, row=1)

#etiqueta apoyo
var2= StringVar()
etiquetaAp = Label(root, textvariable=var2)
var2.set(" ")
etiquetaAp.grid(column=2, row=7)

#etiqueta 2 apoyo
var3= StringVar()
etiquetaAy = Label(root, textvariable=var3)
var3.set(" ")
etiquetaAy.grid(column=2, row=5)

#etiqueta apoyo
var4= StringVar()
etiquetaAp1 = Label(root, textvariable=var4, background='black', width=30, height=1)
var4.set(" ")
etiquetaAp1.grid(column=1, row=6)

#Barra de posicion base
angulo1=Scale(root,
              command = servo1,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Base Scara'  )
angulo1.grid(column=1,row=2)

txt_edit_ang1 = tk.Text(root, width = 5, height=2)
txt_edit_ang1.grid(column=2,row=2)
txt_edit_ang1.insert(tk.END, "0")

#Barra de posicion brazo
angulo2= Scale(root,
              command = servo2,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Brazo Scara'  )
angulo2.grid(column=1,row=3)

txt_edit_ang2 = tk.Text(root, width = 5, height=2)
txt_edit_ang2.grid(column=2,row=3)
txt_edit_ang2.insert(tk.END, "0")

#Barra de posicion antebrazo
angulo3= Scale(root,
              command = servo3,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion anteBrazo Scara'  )
angulo3.grid(column=1,row=4)

txt_edit_ang3 = tk.Text(root, width = 5, height=2)
txt_edit_ang3.grid(column=2,row=4)
txt_edit_ang3.insert(tk.END, "0")

#Barra de posicion Muñeca
angulo4= Scale(root,
              command = servo4,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Muñeca Scara'  )
angulo4.grid(column=1,row=5)

txt_edit_ang4 = tk.Text(root, width = 5, height=2)
txt_edit_ang4.grid(column=2,row=5)
txt_edit_ang4.insert(tk.END, "0")

################################

#Barra de posicion base
Aangulo1=Scale(root,
              command = Aservo1,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Base Antropomorfo'  )
Aangulo1.grid(column=1,row=8)

txt_edit_ang4 = tk.Text(root, width = 5, height=2)
txt_edit_ang4.grid(column=2,row=8)
txt_edit_ang4.insert(tk.END, "0")

#Barra de posicion brazo
Aangulo2= Scale(root,
              command = Aservo2,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Brazo Antropomorfo'  )
Aangulo2.grid(column=1,row=9)

txt_edit_ang5 = tk.Text(root, width = 5, height=2)
txt_edit_ang5.grid(column=2,row=9)
txt_edit_ang5.insert(tk.END, "0")

#Barra de posicion antebrazo
Aangulo3= Scale(root,
              command = Aservo3,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion anteBrazo Antropomorfo'  )
Aangulo3.grid(column=1,row=10)

txt_edit_ang6 = tk.Text(root, width = 5, height=2)
txt_edit_ang6.grid(column=2,row=10)
txt_edit_ang6.insert(tk.END, "0")

####################################

#Gripper

#abrir
BoA = Button(root,text="Gripper",command=abrir, bg='green', bd=3, height=2, width=10)
BoA.grid(column=30,row=5)
#activebackground='green',

#Cerrar
BoC = Button(root,text="Gripper",command=cerrar,bg='green',bd=3,height=2,width=10)
BoC.grid(column=30,row=11)

#boton info
Binf = Button(root,
             text="Modo de uso",
             relief=GROOVE,
             command=info   )
Binf.grid(column=30,row=1)

#boton com close

Bclose = Button(root,
             text="COM close",
             relief=GROOVE,
             command=close   )
Bclose.grid(column=1,row=11)

Envio1=Button(root, text='Envio1', activebackground='yellow', command=show_values1)
Envio1.grid(column=2,row=6)

Envio2=Button(root, text='Envio2', activebackground='yellow', command=show_values2)
Envio2.grid(column=2,row=11)

####################################

#------------creacion de variables en masa
for n in range(1,11):
    for i in range(0,4):
        for j in range(0,4):
            globals()["arr"+str(n)+"_" + str(i) + str(j)]=StringVar()

####################################
#---------------manipulador 1
height = 4
width = 4

for i in range(height): #Rows
    for j in range(width): #Columns
        T11 = Entry(root, text='', width=5, textvariable=globals()["arr1_" + str(i) + str(j)])
        T11.grid(row=i+2, column=j+3)

#etiqueta apoyo
var5= StringVar()
etiquetaAp2 = Label(root, textvariable=var4, background='black', width=1, height=1)
var5.set(" ")
etiquetaAp2.grid(column=8, row=2)

for i in range(height): #Rows
    for j in range(width): #Columns
        T12 = Entry(root, text='', width=5, textvariable=globals()["arr2_" + str(i) + str(j)])
        T12.grid(row=i+2, column=9+j)

#etiqueta apoyo
var6= StringVar()
etiquetaAp3 = Label(root, textvariable=var4, background='black', width=1, height=1)
var6.set(" ")
etiquetaAp3.grid(column=13, row=2)

for i in range(height): #Rows
    for j in range(width): #Columns
        T13 = Entry(root, text='', width=5, textvariable=globals()["arr3_" + str(i) + str(j)])
        T13.grid(row=i+2, column=j+14)

#etiqueta apoyo
var7= StringVar()
etiquetaAp4 = Label(root, textvariable=var4, background='black', width=1, height=1)
var7.set(" ")
etiquetaAp4.grid(column=18, row=2)

for i in range(height): #Rows
    for j in range(width): #Columns
        T14 = Entry(root, text='', width=5, textvariable=globals()["arr4_" + str(i) + str(j)])
        T14.grid(row=i+2, column=j+19)

#etiqueta apoyo
var8= StringVar()
etiquetaAp5 = Label(root, textvariable=var4, background='black', width=1, height=1)
var8.set(" ")
etiquetaAp5.grid(column=23, row=2)

for i in range(height): #Rows
    for j in range(width): #Columns
        T13 = Entry(root, text='', width=5, textvariable=globals()["arr5_" + str(i) + str(j)])
        T13.grid(row=i+2, column=j+24)

#---------------manipulador 2
height = 4
width = 4

for i in range(height): #Rows
    for j in range(width): #Columns
        T21 = Entry(root, text='', width=5, textvariable=globals()["arr6_" + str(i) + str(j)])
        T21.grid(row=i+8, column=j+3)

#etiqueta apoyo
var52= StringVar()
etiquetaAp22 = Label(root, textvariable=var4, background='black', width=1, height=1)
var52.set(" ")
etiquetaAp22.grid(column=8, row=8)

for i in range(height): #Rows
    for j in range(width): #Columns
        T22 = Entry(root, text='', width=5, textvariable=globals()["arr7_" + str(i) + str(j)])
        T22.grid(row=i+8, column=9+j)

#etiqueta apoyo
var62= StringVar()
etiquetaAp32 = Label(root, textvariable=var4, background='black', width=1, height=1)
var62.set(" ")
etiquetaAp32.grid(column=13, row=8)

for i in range(height): #Rows
    for j in range(width): #Columns
        T23 = Entry(root, text='', width=5, textvariable=globals()["arr8_" + str(i) + str(j)])
        T23.grid(row=i+8, column=j+14)

#etiqueta apoyo
var72= StringVar()
etiquetaAp42 = Label(root, textvariable=var4, background='black', width=1, height=1)
var72.set(" ")
etiquetaAp42.grid(column=18, row=8)

for i in range(height): #Rows
    for j in range(width): #Columns
        T24 = Entry(root, text='', width=5, textvariable=globals()["arr9_" + str(i) + str(j)])
        T24.grid(row=i+8, column=j+19)

#etiqueta apoyo
var82= StringVar()
etiquetaAp52 = Label(root, textvariable=var4, background='black', width=1, height=1)
var82.set(" ")
etiquetaAp52.grid(column=23, row=8)


#var44=StringVar()
#for i in range(height): #Rows
#    for j in range(width): #Columns
#        T23 = Entry(root, text='', width=5, textvariable=globals()["arr10_" + str(i) + str(j)] )
#        T23.grid(row=i+8, column=j+24)


#########################

#----------- ejemplo de llenado

for n in range(1,10):
    for i in range(0,4):
        for j in range(0,4):
            globals()["arr"+ str(n) +"_" + str(i) + str(j)].set(str(n)+"_"+str(i)+str(j)) #globals()

#globals()["arr"+str(n)+"_" + str(i) + str(j)].set(str(matrices[n][i][j]))

grados = 60
radianes = (grados* math.pi)/180
globals()["arr9_33"].set(radianes)

root.mainloop()