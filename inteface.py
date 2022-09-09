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

#Configuracion COM
board =serial.Serial(port='COM1', baudrate=19200)
#board.write( b'fine\r\n' )
sleep(5) #5 Segundos Para Que Establezca La Comunicacion


def matrices_T(angz,dz,angx,ax): #
    #Fila 1
    r11="{:.5f}".format(mt.cos(angz))
    r12="{:.5f}".format((-1)*mt.sin(angz)*mt.cos(angx))
    r13="{:.5f}".format(mt.sin(angz)*mt.sin(angx))
    r14="{:.5f}".format(ax*mt.cos(angz))
    #Fila 2
    r21="{:.5f}".format(mt.sin(angz))
    r22="{:.5f}".format(mt.cos(angz)*mt.cos(angx)) 
    r23="{:.5f}".format((-1)*mt.cos(angz)*mt.sin(angx))
    r24="{:.5f}".format(ax*mt.sin(angz))
    #Fila 3
    r31=0
    r32="{:.5f}".format(mt.sin(angx))
    r33="{:.5f}".format(mt.cos(angx))
    r34="{:.5f}".format(dz)
    #Fila 4
    r41=0
    r42=0 
    r43=0 
    r44=1
    matrix=np.array([[r11,r12,r13,r14],[r21,r22,r23,r24],[r31,r32,r33,r34],[r41,r42,r43,r44]],float)
    return matrix

def calculo(matrices_DH,n):
    MatrizFinal=np.eye(4)
    for j in range (0,n):
        MatrizFinal=np.dot(MatrizFinal,matrices_DH[j])          
    return MatrizFinal

def M1(n,d1,t2,t3,t4):
    matrices=[]
    z=[0, t2, t3,t4]
    d=[d1,0,0,0]
    x=[0,0,0,0] 
    a=[47.3,149.1,148.8,30]     
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

def M2(n,j1,j2,j3):
    matrices=[]
    z=[j1, j2, j3]
    d=[62.87,0,0]
    x=[mt.pi/2,0,0] 
    a=[14.5,67.5,88.28]         
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

#Creacion de variables en masa
def creacion():
    for n in range(1,11):
        for i in range(0,4):
            for j in range(0,4):
                globals()["arr"+str(n)+"_" + str(i) + str(j)]=StringVar()


def llenado1 (matri): #Llenado
    for n in range(6,9):
        for i in range(0,4):
            for j in range(0,4):                
                globals()["arr"+ str(n) +"_" + str(i) + str(j)].set(matri[1][n-6][i][j])             
                globals()["arr9" +"_" + str(i) + str(j)].set(matri[0][i][j]) 

def llenado2 (matri):
    for n in range(1,5):
        for i in range(0,4):
            for j in range(0,4):                
                globals()["arr"+ str(n) +"_" + str(i) + str(j)].set(matri[1][n-1][i][j]) 
                globals()["arr5" +"_" + str(i) + str(j)].set(matri[0][i][j])

def dato1(band):
    if band==1:
        mat=M2(3,Aangulo1.get(),Aangulo2.get(),Aangulo3.get())
    elif band==2:
        mat=M2(3,int(txt_edit_ang4.get(1.0, tk.END)),int(txt_edit_ang5.get(1.0, tk.END)),int(txt_edit_ang6.get(1.0, tk.END)))
    llenado1(mat)

def dato2(band):
    if band==1:
        mat2=M1(4,angulo1.get(),angulo2.get(),angulo3.get(),angulo4.get())
    elif band==2:
        mat2=M1(4,int(txt_edit_ang0.get(1.0, tk.END)),int(txt_edit_ang1.get(1.0, tk.END)),int(txt_edit_ang2.get(1.0, tk.END)),int(txt_edit_ang3.get(1.0, tk.END)))
    llenado2(mat2)

def servo1(posiciones1):
    #Escritura De Angulo
    board.write(b'Eb,')
    board.write(posiciones1.encode())
    board.write(b'\r\n')
    dato2(1)

def servo2(posiciones2):
    #Escritura De Angulo
    board.write(b'Ebr,')
    board.write(posiciones2.encode())
    board.write(b'\r\n')
    dato2(1)

def servo3(posiciones3):
    #Escritura De Angulo
    board.write(b'Eab,')
    board.write(posiciones3.encode())
    board.write(b'\r\n')
    dato2(1)

def servo4(posiciones4):
    #Escritura De Angulo
    board.write(b'Em,')
    board.write(posiciones4.encode())
    board.write(b'\r\n')
    dato2(1)

#Funciones de movimiento Antropomorfico

def Aservo1(Aposiciones1):
     #Escritura De Angulo
    board.write(b'Ab,')
    board.write(Aposiciones1.encode())
    board.write(b'\r\n')
    dato1(1)

def Aservo2(Aposiciones2):
    #Escritura De Angulo
    board.write(b'Abr,')
    board.write(Aposiciones2.encode())
    board.write(b'\r\n')
    dato1(1)

def Aservo3(Aposiciones3):
    #Escritura De Angulo
    board.write(b'Aab,')
    board.write(Aposiciones3.encode())
    board.write(b'\r\n')
    dato1(1)

#Gripper
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

#Info
def info():
    messagebox.showinfo("Informacion",
        "Modo de uso:\nDesplazar cada slider para mover las articulaciones del brazo robotico para realizar el movimiento de cada articulacion \n o digitar el valor de lo que se quiere mover para \n luego presionar el boton de envio correspondiente \n se pretende obtener las matrices individuales y totales en tiempo real"  )

#Serial
def close():
    board.write(b'bye\r\n')
    board.close()
    #Ejemplo de llenado
    for n in range(1,11):
        for i in range(0,4):
            for j in range(0,4):
                globals()["arr"+ str(n) +"_" + str(i) + str(j)].set(str(n)+"_"+str(i)+str(j)) 
#----------------------------

#Envio de datos por boton
def show_values1():
    board.write("Rojo".encode()) 
    # #Cuadro_Texto_1
    # board.write(b'Eb,')
    # board.write(txt_edit_ang0.get(1.0, tk.END).encode())    

    # #Cuadro_Texto_2
    # board.write(b'Ebr,')
    # board.write(txt_edit_ang1.get(1.0, tk.END).encode())

    # #Cuadro_Texto_3 
    # board.write(b'Eab,')
    # board.write(txt_edit_ang2.get(1.0, tk.END).encode())

    # #Cuadro_Texto_4
    # board.write(b'Em,')
    # board.write(txt_edit_ang3.get(1.0, tk.END).encode())
    # dato2(2)

def show_values2():
    
    #Cuadro_Texto_6
    board.write(b'Ab,')
    board.write(txt_edit_ang4.get(1.0, tk.END).encode())

    #Cuadro_Texto_7
    board.write(b'Abr,')
    board.write(txt_edit_ang5.get(1.0, tk.END).encode())

    #Cuadro_Texto_8
    board.write(b'Aab,')
    board.write(txt_edit_ang6.get(1.0, tk.END).encode())
    dato1(2)

root = Tk()

root.title("Control de Manipulador Robotico")
root.geometry("1366x768")
creacion()

#Logo
img= PhotoImage(file="LOGOUMNG.png")
widget = Label(root, image=img)


img1= PhotoImage(file="icon.png")
widget1 = Label(root, image=img1)


globals()["color_boton1"]=StringVar()
color_boton1='green'

#Etiqueta 1
var= StringVar()
etiqueta = Label(root, textvariable=var , relief=FLAT , pady=5)
var.set("Dario Delgado - 1802992 \n Brayan Ulloa - 1802861 \n Santiago Tobar - 1803015 \n Fernando Llanes - 1802878 \n Karla Baron - 1803648 \n Sebastian Niño - 1803558")

#Etiqueta Apoyo
var2= StringVar()
etiquetaAp = Label(root, textvariable=var2)
var2.set(" ")
etiquetaAp.grid(column=2, row=7)

#Etiqueta Apoyo
var3= StringVar()
etiquetaAy = Label(root, textvariable=var3)
var3.set(" ")
etiquetaAy.grid(column=2, row=5)

#Etiqueta Apoyo
var4= StringVar()
etiquetaAp1 = Label(root, textvariable=var4, background='black', width=30, height=1)
var4.set(" ")
etiquetaAp1.grid(column=1, row=6)

#Barra de posicion base
angulo1=Scale(root,
              command = servo1,
              from_=0,
              to=122,
              resolution=0.1,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Base Scara'  )
angulo1.grid(column=1,row=2)

txt_edit_ang0 = tk.Text(root, width = 5, height=2)
txt_edit_ang0.grid(column=2,row=2)
txt_edit_ang0.insert(tk.END, "0")

#Barra de posicion brazo
angulo2= Scale(root,
              command = servo2,
              from_=0,
              to=180,
              resolution=0.1,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Brazo Scara'  )
angulo2.grid(column=1,row=3)

txt_edit_ang1 = tk.Text(root, width = 5, height=2)
txt_edit_ang1.grid(column=2,row=3)
txt_edit_ang1.insert(tk.END, "0")

#Barra de posicion antebrazo
angulo3= Scale(root,
              command = servo3,
              from_=0,
              to=180,
              resolution=0.1,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion anteBrazo Scara'  )
angulo3.grid(column=1,row=4)

txt_edit_ang2 = tk.Text(root, width = 5, height=2)
txt_edit_ang2.grid(column=2,row=4)
txt_edit_ang2.insert(tk.END, "0")

#Barra de posicion Muñeca
angulo4= Scale(root,
              command = servo4,
              from_=0,
              to=180,
              resolution=0.1,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Muñeca Scara'  )
angulo4.grid(column=1,row=5)

txt_edit_ang3 = tk.Text(root, width = 5, height=2)
txt_edit_ang3.grid(column=2,row=5)
txt_edit_ang3.insert(tk.END, "0")

#Barra de posicion base
Aangulo1=Scale(root,
              command = Aservo1,
              from_=0,
              to=180,
              resolution=0.1,
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

#Posicion Brazo

#Slider
Aangulo2= Scale(root,
              command = Aservo2,
              from_=0,
              to=180,
              resolution=0.1,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Posicion Brazo Antropomorfo'  )
Aangulo2.grid(column=1,row=9)

#Text Box
txt_edit_ang5 = tk.Text(root, width = 5, height=2)
txt_edit_ang5.grid(column=2,row=9)
txt_edit_ang5.insert(tk.END, "0")

#Barra de posicion antebrazo
Aangulo3= Scale(root,
              command = Aservo3,
              from_=0,
              to=180,
              resolution=0.1,
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


#Gripper

#Abrir
BoA = Button(root,text="Gripper",command=abrir, bg='green', bd=3, height=2, width=10)
BoA.grid(column=30,row=5)

#Cerrar
BoC = Button(root,text="Gripper",command=cerrar,bg='green',bd=3,height=2,width=10)
BoC.grid(column=30,row=11)

#Boton Info
Binf = Button(root,
             text="Modo de uso",
             relief=GROOVE,
             command=info   )
Binf.grid(column=30,row=1)

#Boton COM Close

Bclose = Button(root,
             text="COM close",
             relief=GROOVE,
             command=close   )
Bclose.grid(column=1,row=11)

Envio1=Button(root, text='Envio1', activebackground='yellow', command=show_values1)
Envio1.grid(column=2,row=6)

Envio2=Button(root, text='Envio2', activebackground='yellow', command=show_values2)
Envio2.grid(column=2,row=11)


#Manipulador 1
height = 4
width = 4
largo=6

for i in range(height): #Rows
    for j in range(width): #Columns
        T11 = Entry(root, text='', width=largo, textvariable=globals()["arr1_" + str(i) + str(j)])
        T11.grid(row=i+2, column=j+3)

#Etiqueta Apoyo
var5= StringVar()
etiquetaAp2 = Label(root, textvariable=var4, background='black', width=1, height=1)
var5.set(" ")
etiquetaAp2.grid(column=8, row=2)

for i in range(height): #Rows
    for j in range(width): #Columns
        T12 = Entry(root, text='', width=largo, textvariable=globals()["arr2_" + str(i) + str(j)])
        T12.grid(row=i+2, column=j+9)

#Etiqueta Apoyo
var6= StringVar()
etiquetaAp3 = Label(root, textvariable=var4, background='black', width=1, height=1)
var6.set(" ")
etiquetaAp3.grid(column=13, row=2)

for i in range(height): #Rows
    for j in range(width): #Columns
        T13 = Entry(root, text='', width=largo, textvariable=globals()["arr3_" + str(i) + str(j)])
        T13.grid(row=i+2, column=j+14)

#Etiqueta Apoyo
var7= StringVar()
etiquetaAp4 = Label(root, textvariable=var4, background='black', width=1, height=1)
var7.set(" ")
etiquetaAp4.grid(column=18, row=2)

for i in range(height): #Rows
    for j in range(width): #Columns
        T14 = Entry(root, text='', width=largo, textvariable=globals()["arr4_" + str(i) + str(j)])
        T14.grid(row=i+2, column=j+19)

#Etiqueta Apoyo
var8= StringVar()
etiquetaAp5 = Label(root, textvariable=var4, background='black', width=1, height=1)
var8.set(" ")
etiquetaAp5.grid(column=23, row=2)

for i in range(height): #Rows
    for j in range(width): #Columns
        T13 = Entry(root, text='', width=largo, textvariable=globals()["arr5_" + str(i) + str(j)])
        T13.grid(row=i+2, column=j+24)

#Manipulador 2
height = 4
width = 4

for i in range(height): #Rows
    for j in range(width): #Columns
        T21 = Entry(root, text='', width=largo, textvariable=globals()["arr6_" + str(i) + str(j)])
        T21.grid(row=i+8, column=j+3)

#Etiqueta Apoyo
var52= StringVar()
etiquetaAp22 = Label(root, textvariable=var4, background='black', width=1, height=1)
var52.set(" ")
etiquetaAp22.grid(column=8, row=8)

for i in range(height): #Rows
    for j in range(width): #Columns
        T22 = Entry(root, text='', width=largo, textvariable=globals()["arr7_" + str(i) + str(j)])
        T22.grid(row=i+8, column=9+j)

#Etiqueta Apoyo
var62= StringVar()
etiquetaAp32 = Label(root, textvariable=var4, background='black', width=1, height=1)
var62.set(" ")
etiquetaAp32.grid(column=13, row=8)

for i in range(height): #Rows
    for j in range(width): #Columns
        T23 = Entry(root, text='', width=largo, textvariable=globals()["arr8_" + str(i) + str(j)])
        T23.grid(row=i+8, column=j+14)

#Etiqueta Apoyo
var72= StringVar()
etiquetaAp42 = Label(root, textvariable=var4, background='black', width=1, height=4)
var72.set(" ")
etiquetaAp42.grid(column=18, row=8)

for i in range(height): #Rows
    for j in range(width): #Columns
        T24 = Entry(root, text='', width=largo, textvariable=globals()["arr9_" + str(i) + str(j)])
        T24.grid(row=i+8, column=j+19)

#Etiqueta Apoyo
var82= StringVar()
etiquetaAp52 = Label(root, textvariable=var4, background='black', width=1, height=1)
var82.set(" ")
etiquetaAp52.grid(column=23, row=8)

root.mainloop()