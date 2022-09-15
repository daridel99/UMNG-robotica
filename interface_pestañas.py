#IMPORTAMOS "tkinter"
from pickletools import float8
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


#Configuracion COM
board =serial.Serial(port='COM1', baudrate=19200)
#board.write( b'fine\r\n' )
sleep(5) #5 Segundos Para Que Establezca La Comunicacion

def fila_vacia(n): #Crear Filas Vacias
    for j in range (0,n):
        fila = Label(frmdh1)
        fila.grid(column=0, row=(5*j))


def matrices_T(angz,dz,angx,ax): #Matriz Homogenea DH
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

def calculo(matrices_DH,n): #Calculo de matriz Cinematica Directa
    MatrizFinal=np.eye(4)
    for j in range (0,n):
        MatrizFinal=np.dot(MatrizFinal,matrices_DH[j]) 
        MatrizFinal=np.round(MatrizFinal,decimals=5)    
    return MatrizFinal

def M1(n,d1,t2,t3,t4): #Definicion Parametros Scara
    matrices=[]
    z=[0, t2, t3,t4]
    d=[d1,0,0,0]
    x=[0,0,0,0] 
    a=[47.3,149.1,148.8,30]     
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

def M2(n,j1,j2,j3): #Definicion Parametros Antropomorfico
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


def llenado1 (matri): #Llenado Matrices Antropomorfico
    for n in range(6,9):
        for i in range(0,4):
            for j in range(0,4):                
                globals()["arr"+ str(n) +"_" + str(i) + str(j)].set(matri[1][n-6][i][j])             
                globals()["arr9" +"_" + str(i) + str(j)].set(matri[0][i][j]) 

def llenado2 (matri): #Llenado Matrices Scara
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

#Funciones De Movimiento Scara

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

#Funciones De Movimiento Antropomorfico

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

#Serial
def close():
    board.write(b'bye\r\n')
    board.close()


#Envio de datos Scara
def show_values1():
    print("Calculando...")
    board.write("Rojo".encode()) 
    #Cuadro_Texto_1
    board.write(b'Eb,')
    board.write(txt_edit_ang0.get(1.0, tk.END).encode())    

    #Cuadro_Texto_2
    board.write(b'Ebr,')
    board.write(txt_edit_ang1.get(1.0, tk.END).encode())

    #Cuadro_Texto_3 
    board.write(b'Eab,')
    board.write(txt_edit_ang2.get(1.0, tk.END).encode())

    #Cuadro_Texto_4
    board.write(b'Em,')
    board.write(txt_edit_ang3.get(1.0, tk.END).encode())
    dato2(2)

#Envio de datos Antropomorfico
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

#VENTANA PRINCIPAL.
root = tkinter.Tk()
root.title('Controles de Manipuladores Roboticos')
root.geometry("1366x768")
creacion()
nombre = StringVar()
numero = IntVar()

#INCLUIMOS PANEL PARA LAS PESTAÑAS.
nb = ttk.Notebook(root)
nb.pack(fill='both',expand='yes')

#CREAMOS PESTAÑAS
pI = ttk.Frame(nb)
p1 = ttk.Frame(nb)
p2 = ttk.Frame(nb)   

#####Pestaña 1#####

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
#Boton COM Close
Bclose = Button(fi,
             text="COM close",
             relief=GROOVE,
             command=close   )
Bclose.grid(column=2,row=1)

#####Pestaña 2#####

#Frame Manipulador Scara (Contenedor)
frm=LabelFrame(p1,relief="raised")
frm.place(relwidth=1, relheight=1)

#Frame Cinematica Directa DK (Contenedor)
frm1=LabelFrame(frm,text='DK', labelanchor='n')
frm1.place(relwidth=1, relheight=0.64)

#Base
#Slider
angulo1=Scale(frm1,
                command = servo1,
                from_=0,
                to=122,
                resolution=0.1,
                orient = HORIZONTAL,
                length=266,
                troughcolor='gray',
                width = 30,
                cursor='dot',
                label = 'Desplazamiento Base',
                )
angulo1.place(rely=0)
#Text_Box
txt_edit_ang0 = tk.Text(frm1,width=4)
txt_edit_ang0.place(relx=1/5, rely=1/12+0.01, relheight=1/8-0.045)
txt_edit_ang0.insert(tk.END, "0")
        
#Brazo
#Slider
angulo2= Scale(frm1,
              command = servo2,
              from_=0,
              to=180,
              resolution=0.1,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Brazo'  )
angulo2.place(rely=1/4)
#Text_Box
txt_edit_ang1 = tk.Text(frm1, width = 4)
txt_edit_ang1.place(relx=1/5, rely=4/12+0.01, relheight=1/8-0.045)
txt_edit_ang1.insert(tk.END, "0")

#Antebrazo
#Slider
angulo3= Scale(frm1,     
              command = servo3,         
              from_=0,
              to=180,
              resolution=0.1,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Codo'  )
angulo3.place(rely=2/4)
#Text_Box
txt_edit_ang2 = tk.Text(frm1, width = 4)
txt_edit_ang2.place(relx=1/5, rely=7/12+0.011, relheight=1/8-0.045)
txt_edit_ang2.insert(tk.END, "0")

#Muñeca
#Slider
angulo4= Scale(frm1,
              command = servo4,
              from_=0,
              to=180,
              resolution=0.1,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Muñeca'  )
angulo4.place(rely=3/4)
#Text_Box
txt_edit_ang3 = tk.Text(frm1, width = 4)
txt_edit_ang3.place(relx=1/5, rely=10/12+0.011, relheight=1/8-0.045)
txt_edit_ang3.insert(tk.END, "0")

#Frame Matrices Cinematica Directa DK (Contenedor)
frmdh1=LabelFrame(frm1,relief="raised")
frmdh1.place(relx=1/4+0.02, relwidth=1, relheight=1)

#Matriz Link 1
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1, width=13, textvariable=globals()["arr1_" + str(r) + str(c)])
        cell.grid(row=r+1, column=c, ipady=4)

#Matriz Link 2
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1, width=13, textvariable=globals()["arr2_" + str(r) + str(c)])
        cell.grid(row=r+1, column=c+8, ipady=4)

#Matriz Total
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1, width=13, textvariable=globals()["arr5_" + str(r) + str(c)])
        cell.grid(row=r+6, column=c+4, ipady=4)
 
#Matriz Link 3
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1, width=13, textvariable=globals()["arr3_" + str(r) + str(c)])
        cell.grid(row=r+11, column=c, ipady=4)

#Matriz Link 4
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1, width=13, textvariable=globals()["arr4_" + str(r) + str(c)])
        cell.grid(row=r+11, column=c+8, ipady=4)

#Boton Envio Cinematica Directa Scara
Envio1=Button(frmdh1, width=10, height=2, text='Envio', activebackground='yellow', command=show_values1)
Envio1.place(relx=2/6,rely=14/16)

#Boton Gripper Scara
BoA = Button(frmdh1,text="Gripper",command=abrir, bg='green', bd=3, height=2, width=10)
BoA.place(relx=2/6,rely=11/16)

#Frame Cinematica Inversa IK (Contenedor)
frm2=LabelFrame(frm,text='IK', labelanchor='n')
frm2.place(rely=0.63, relwidth=1, relheight=0.37)

#Text_Box Px
txt_edit_xS = tk.Text(frm2, width=4, height=1)
txt_edit_xS.place(relx=1/10,rely=1/10+0.01)
txt_edit_xS.insert(tk.END, "0")
        
#Text_Box Py
txt_edit_yS = tk.Text(frm2, width = 4, height=1)
txt_edit_yS.place(relx=1/10, rely=3/10+0.01)
txt_edit_yS.insert(tk.END, "0")

#Text_Box Pz
txt_edit_zS = tk.Text(frm2, width = 4, height=1)
txt_edit_zS.place(relx=1/10, rely=5/10+0.01)
txt_edit_zS.insert(tk.END, "0")

#Text_Box Phi
txt_edit_phiS = tk.Text(frm2, width = 4, height=1)
txt_edit_phiS.place(relx=1/10, rely=7/10+0.01)
txt_edit_phiS.insert(tk.END, "0")

#Boton Calcular Cinematica Inversa        
Calcular1=Button(frm2, text='Calcular', activebackground='yellow')
Calcular1.place(relx=1/10-0.01, rely=9/10-0.03, relheight=1/6-0.05)

#Frame Variables de Juntura (Contenedor)
frmdh2=LabelFrame(frm2,relief="raised")
frmdh2.place(relx=0.35, rely=0.15, relwidth=0.42, relheight=0.5)

#Variable de Juntura 1
etiqueta1 = tk.Label(frmdh2, width=5, text="d₁", fg="black", bg="yellow").grid(column=0, row=0)
text1 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2, orient="horizontal", command=text1.xview)
text1.configure(xscrollcommand=textHsb.set)
text1.grid(row=0, column=1, sticky="nsew")
textHsb.grid(row=1, column=1, sticky="ew")

blanco = Label(frmdh2, width=10)
blanco.grid(column=1, row=2)

#Variable de Juntura 2
etiqueta2 = tk.Label(frmdh2, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=3)
text2 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2, orient="horizontal", command=text2.xview)
text2.configure(xscrollcommand=textHsb.set)
text2.grid(row=3, column=1, sticky="nsew")
textHsb.grid(row=4, column=1, sticky="ew")

blanco = Label(frmdh2, width=10)
blanco.grid(column=2, row=0)

#Variable de Juntura 3
etiqueta3 = tk.Label(frmdh2, width=5, text="θ₃", fg="black", bg="yellow").grid(column=3, row=0)
text3 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2, orient="horizontal", command=text3.xview)
text3.configure(xscrollcommand=textHsb.set)
text3.grid(row=0, column=4, sticky="nsew")
textHsb.grid(row=1, column=4, sticky="ew")

#Variable de Juntura 4
etiqueta4 = tk.Label(frmdh2, width=5, text="θ₄", fg="black", bg="yellow").grid(column=3, row=3)
text4 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2, orient="horizontal", command=text4.xview)
text4.configure(xscrollcommand=textHsb.set)
text4.grid(row=3, column=4, sticky="nsew")
textHsb.grid(row=4, column=4, sticky="ew")

fila_vacia(3)
#Titulos Scara (Label)
Titulos_l1 = Label(frmdh1, width=11,text="Link 1")
Titulos_l1.place(relx=2/24+0.01,rely=0)
Titulos_l2 = Label(frmdh1, width=11,text="Link 2")
Titulos_l2.place(relx=14/24-0.005,rely=0)
Titulos_l3 = Label(frmdh1, width=11,text="Link 3")
Titulos_l3.place(relx=2/24+0.01,rely=10/16)
Titulos_l4 = Label(frmdh1, width=11,text="Link 4")
Titulos_l4.place(relx=14/24-0.005,rely=10/16)
Titulos_lT = Label(frmdh1, width=11,text="Total")
Titulos_lT.place(relx=5/15,rely=5/16)
Titulos_px = Label(frm2, width=5,text="Px")
Titulos_px.place(relx=1/15,rely=1/10+0.01)
Titulos_py = Label(frm2, width=5,text="Py")
Titulos_py.place(relx=1/15,rely=3/10+0.01)
Titulos_pz = Label(frm2, width=5,text="Pz")
Titulos_pz.place(relx=1/15,rely=5/10+0.01)
Titulos_pphi = Label(frm2, width=5,text="Phi")
Titulos_pphi.place(relx=1/15,rely=7/10+0.01)
#####Pestaña 3#####

#Frame Manipulador Antropomorfico (Contenedor)
frmA=LabelFrame(p2,relief="raised")
frmA.place(relwidth=1, relheight=1)

#Frame Cinematica Directa DK (Contenedor)
frm1A=LabelFrame(frmA,text='DK', labelanchor='n')
frm1A.place(relwidth=1, relheight=0.64)

#Base
#Slider
Aangulo1=Scale(frm1A,
                command = Aservo1,
                resolution=0.1,
                from_=0,
                to=180,
                orient = HORIZONTAL,
                length=266,
                troughcolor='gray',
                width = 30,
                cursor='dot',
                label = 'Rotación Base')
Aangulo1.place(rely=0)
#Text_Box
txt_edit_ang4 = tk.Text(frm1A,width=4)
txt_edit_ang4.place(relx=1/5, rely=1/12+0.01, relheight=1/8-0.045)
txt_edit_ang4.insert(tk.END, "0")
        
#Brazo
#Slider
Aangulo2= Scale(frm1A,
              command = Aservo2,
              resolution=0.1,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Brazo')
Aangulo2.place(rely=1/4)
#Text_Box
txt_edit_ang5 = tk.Text(frm1A, width = 4)
txt_edit_ang5.place(relx=1/5, rely=4/12+0.01, relheight=1/8-0.045)
txt_edit_ang5.insert(tk.END, "0")

#Antebrazo
#Slider
Aangulo3= Scale(frm1A,  
              command = Aservo3,  
              resolution=0.1,          
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Codo')
Aangulo3.place(rely=2/4)
#Text_Box
txt_edit_ang6 = tk.Text(frm1A, width = 4)
txt_edit_ang6.place(relx=1/5, rely=7/12+0.011, relheight=1/8-0.045)
txt_edit_ang6.insert(tk.END, "0")

def blancoA(n):
    blanco = Label(frmdh1A, width=6)
    blanco.grid(column=4+n, row=0)

#Frame Matrices Cinematica Directa DK (Contenedor)
frmdh1A=LabelFrame(frm1A,relief="raised")
frmdh1A.place(relx=0.35, relwidth=0.525, relheight=1)

#Matriz Link 1
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1A, width=12,  textvariable=globals()["arr6_" + str(r) + str(c)])
        cell.grid(row=r+1, column=c, ipady=4)

blancoA(0)

blancoA(5)

#Matriz Link 2
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1A, width=12,  textvariable=globals()["arr7_" + str(r) + str(c)])
        cell.grid(row=r+1, column=c+8, ipady=4)
        
blanco = Label(frmdh1A)
blanco.grid(column=0, row=5)
blanco1 = Label(frmdh1A)
blanco1.grid(column=0, row=6)
blanco2 = Label(frmdh1A)
blanco2.grid(column=0, row=7)
blanco3 = Label(frmdh1A)
blanco3.grid(column=0, row=8)

#Matriz Link 3
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1A, width=12, textvariable=globals()["arr8_" + str(r) + str(c)])
        cell.grid(row=r+9, column=c, ipady=4)

#Matriz Total
for r in range(0, 4):
    for c in range(0, 4):
        cell = Entry(frmdh1A, width=12,  textvariable=globals()["arr9_" + str(r) + str(c)])
        cell.grid(row=r+9, column=c+8, ipady=4)

#Boton Envio Cinematica Directa Antropomorfico
Envio2=Button(frmdh1A, width=12, height=2, text='Envio', activebackground='yellow', command=show_values2)
Envio2.grid(column=4,row=13)

#Boton Gripper Antropomorfico
BoC = Button(frm1A,text="Gripper",command=cerrar,bg='green',bd=3,height=2,width=10)
BoC.place(x=110,rely=3/4)

#Frame Cinematica Inversa IK (Contenedor)
frm2A=LabelFrame(frmA,text='IK', labelanchor='n')
frm2A.place(rely=0.65, relwidth=1, relheight=0.35)

#Text_Box Px
txt_edit_xA = tk.Text(frm2A, width=4, height=1)
txt_edit_xA.place(relx=1/10,rely=1/10+0.01)
txt_edit_xA.insert(tk.END, "0")
        
#Text_Box Py
txt_edit_yA = tk.Text(frm2A, width = 4, height=1)
txt_edit_yA.place(relx=1/10, rely=3/10+0.01)
txt_edit_yA.insert(tk.END, "0")

#Text_Box Pz
txt_edit_zA = tk.Text(frm2A, width = 4, height=1)
txt_edit_zA.place(relx=1/10, rely=5/10+0.01)
txt_edit_zA.insert(tk.END, "0")

#Boton Calcular Cinematica Inversa Antropomorfico        
Calcular2=Button(frm2A, text='Calcular', activebackground='yellow')
Calcular2.place(relx=1/10-0.01, rely=7/10+0.01, relheight=1/6-0.05)

frmdh2A=LabelFrame(frm2A,relief="raised")
frmdh2A.place(relx=0.4, rely=0.1, relwidth=0.25, relheight=0.8)

#Variable de Juntura 1
etiqueta1 = tk.Label(frmdh2A, width=5, text="θ₁", fg="black", bg="yellow").grid(column=0, row=0)
text1A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2A, orient="horizontal", command=text1A.xview)
text1A.configure(xscrollcommand=textHsb.set)
text1A.grid(row=0, column=1, sticky="nsew")
textHsb.grid(row=1, column=1, sticky="ew")

#Variable de Juntura 2
etiqueta2 = tk.Label(frmdh2A, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=3)
text2A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2A, orient="horizontal", command=text2A.xview)
text2A.configure(xscrollcommand=textHsb.set)
text2A.grid(row=3, column=1, sticky="nsew")
textHsb.grid(row=4, column=1, sticky="ew")

blanco = Label(frmdh2A, width=10)
blanco.grid(column=0, row=2)

#Variable de Juntura 3
etiqueta3 = tk.Label(frmdh2A, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=6)
text3A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
textHsb = tk.Scrollbar(frmdh2A, orient="horizontal", command=text3A.xview)
text3A.configure(xscrollcommand=textHsb.set)
text3A.grid(row=6, column=1, sticky="nsew")
textHsb.grid(row=7, column=1, sticky="ew")

blanco = Label(frmdh2A, width=10)
blanco.grid(column=0, row=5)

#Titulos Antropomorfico (Label)
Titulos_l1 = Label(frmdh1A, width=11,text="Link 1")
Titulos_l1.place(relx=3/18-0.01,rely=0)
Titulos_l2 = Label(frmdh1A, width=11,text="Link 2")
Titulos_l2.place(relx=13/18-0.01,rely=0)
Titulos_l3 = Label(frmdh1A, width=11,text="Link 3")
Titulos_l3.place(relx=3/18-0.01,rely=7/14-0.03)
Titulos_lT = Label(frmdh1A, width=11,text="Total")
Titulos_lT.place(relx=13/18-0.01,rely=7/14-0.03)
Titulos_px = Label(frm2A, width=5,text="Px")
Titulos_px.place(relx=1/15,rely=1/10+0.01)
Titulos_py = Label(frm2A, width=5,text="Py")
Titulos_py.place(relx=1/15,rely=3/10+0.01)
Titulos_pz = Label(frm2A, width=5,text="Pz")
Titulos_pz.place(relx=1/15,rely=5/10+0.01)

#AGREGAMOS PESTAÑAS CREADAS
nb.add(pI,text='Portada')
nb.add(p1,text='Robot Scara')
nb.add(p2,text='Robot Antropomorfico (RRR)')

root.mainloop()