import tkinter 
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import HORIZONTAL, PhotoImage, StringVar, Widget
from time import sleep
from warnings import catch_warnings
import numpy as np

import serial, serial.tools.list_ports
import Calculos

#Configuracion COM
board =serial.Serial(port='COM1', baudrate=19200)
sleep(5) #5 Segundos Para Que Establezca La Comunicacion

def fila_vacia(donde,cuantas,frame,tamaño): #Crear Filas Vacias    
    for n in range (0,cuantas):
        fila = Label(frame,width=tamaño)
        fila.grid(column=0, row=donde+n)

def columna_vacia(donde,cuantas,frame,tamano):
    for n in range (0,cuantas):
        blanco = Label(frame, width=tamano)
        blanco.grid(column=donde+n, row=0)

#Creacion de variables en masa
def creacion():

    globals()["txt_edit_yS_var"] = StringVar()

    for n in range(1,17):
        for i in range(0,4):
            for j in range(0,4):
                globals()["arr"+str(n)+"_" + str(i) + str(j)]=StringVar()
    
    for i in range(0,6):
        for j in range(0,4):
            globals()["jacoS_" + str(i) + str(j)]=StringVar()

    for i in range(0,6):
        for j in range(0,3):
            globals()["jacoA_" + str(i) + str(j)]=StringVar()

    for i in range(0,6):
        for j in range(0,6):
            globals()["jacoR_" + str(i) + str(j)]=StringVar()

def matrices(m,f,k,frame):
    for r in range(0, 4):
        for c in range(0, 4):
            cell = Entry(frame, width=13,  textvariable=globals()["arr" + str(m) + "_" + str(r) + str(c)], state= DISABLED)
            cell.grid(row=r+f, column=c+k, ipady=4)

def llenado (matri,M,K): #Llenado Matrices Antropomórfico (R3)            
    for n in range(M,K):
        for i in range(0,4):
            for j in range(0,4):                
                globals()["arr"+ str(n) +"_" + str(i) + str(j)].set(matri[1][n-M][i][j])             
                globals()["arr"+ str(K) +"_"+ str(i) + str(j)].set(matri[0][i][j]) 

def llenado_JACO (JA,JS): #Llenado Matrices JACO
    for i in range(0,2):
        i=i*3
        for j in range(0,4):           
            for k in range(0,3):                
                globals()["jacoS_" + str(i+k) + str(j)].set(JS[i-2][j][k]) 

    for i in range(0,2):
        i=i*3
        for j in range(0,3): 
            for k in range(0,3):               
                globals()["jacoA_" + str(i+k) + str(j)].set(JA[i-2][j][k]) 

    for i in range(0,6):
        for j in range(0,6):                
            globals()["jacoR_" + str(i) + str(j)].set("matri[1][n-10][i][j]") 


def Button_IK_Scara_P3R():

    M=Calculos.IK_Scara_P3R(float(txt_edit_xS.get()), float(txt_edit_yS.get()), float(txt_edit_zS.get()), float(txt_edit_phiS.get()))

    if M[7] == 1:
        messagebox.showinfo(title="error",
        message="El valor de alguna variable de juntura supera los limites mecanicos. \n \t \t Varie el valor de ϕ  ")

    text1.delete("1.0","end")
    text1.insert( tk.END,str(M[0]))
    text1Ar.delete("1.0","end")
    text1Ar.insert(tk.END, str(M[0]))
    text2.delete("1.0","end")
    text2.insert( tk.END,str(M[1]))
    text2Ar.delete("1.0","end")
    text2Ar.insert(tk.END, str(M[4]))
    text3.delete("1.0","end")
    text3.insert( tk.END,str(M[2]))
    text3Ar.delete("1.0","end")
    text3Ar.insert(tk.END, str(M[5]))
    text4.delete("1.0","end")
    text4.insert( tk.END,str(M[3]))
    text4Ar.delete("1.0","end")
    text4Ar.insert(tk.END, str(M[6]))
    llenado(Calculos.M1(4, M[0], M[1], M[2], M[3]),1,5)

def Button_IK_Antropo_3R():

    M=Calculos.IK_Antropo_3R(float(txt_edit_xA.get(1.0, tk.END)), float(txt_edit_yA.get(1.0, tk.END)), float(txt_edit_zA.get(1.0, tk.END)))
   
    if np.size(M) == 1:
        messagebox.showinfo(title="error", message="Varie el valor de Phi")

    else:
        text1A.delete("1.0","end")
        text1A.insert( tk.END,str(M[0]))
        text1AAr.delete("1.0","end")
        text1AAr.insert(tk.END, str(M[0]))
        text2A.delete("1.0","end")
        text2A.insert( tk.END,str(M[1]))
        text2AAr.delete("1.0","end")
        text2AAr.insert(tk.END, str(M[4]))
        text3A.delete("1.0","end")
        text3A.insert( tk.END,str(M[2]))
        text3AAr.delete("1.0","end")
        text3AAr.insert(tk.END, str(M[5]))
        '''text4.delete("1.0","end")
        text4.insert( tk.END,str(M[3]))
        text4Ar.delete("1.0","end")
        text4Ar.insert(tk.END, str(M[6]))'''
        llenado(Calculos.M2(3, M[0], M[1], M[2]),6,9)

def Button_CalcularJACO():

    J_A=Calculos.JG_A(3,Aangulo1.get(),Aangulo2.get(),Aangulo3.get())
    J_S=Calculos.JG_S(4,angulo1.get(),angulo2.get(),angulo3.get(),angulo4.get())
    llenado_JACO(J_A,J_S)

def re_def_SLIDER(IKxS):

    LimitY=Calculos.varX_scara(txt_edit_xS.get())
    txt_edit_yS.place(relx=0.035, rely=0.225)

    supe=LimitY[0]
    infe=LimitY[1]
    txt_edit_yS['state']='active'
    

    if LimitY[2]== 0 :
        checkbox.place_forget()
        globals() ["txt_edit_yS_var"] = txt_edit_yS.get()
        txt_edit_yS['from_']=str(infe)
        txt_edit_yS['to']=str(supe)
    else:
        checkbox.place(relx=0.21, rely=0.33)
        if checkbox_value.get():
            #globals() ["txt_edit_yS_var"] = -1*txt_edit_yS.get()
            txt_edit_yS['from_']=str(float(-1)*supe)
            txt_edit_yS['to']=str(float(-1)*infe)
        else:
            #globals() ["txt_edit_yS_var"] = txt_edit_yS.get()
            txt_edit_yS['from_']=str(infe)
            txt_edit_yS['to']=str(supe)

def re_def_SLIDER_clk():
    re_def_SLIDER(0)

def selection_changed(event):
    selection = combo.get()
    if selection == "DK":
        frm6Rik.place_forget()
        frm6Rdk.place(rely=0.05, relwidth=1, relheight=0.95)
    else:
        frm6Rdk.place_forget()
        frm6Rik.place(rely=0.05, relwidth=1, relheight=0.95)
    messagebox.showinfo(
        title="Nuevo elemento seleccionado",
        message=selection
    )

def dato1(band):
    if band==1:
        mat=Calculos.M2(3,Aangulo1.get(),Aangulo2.get(),Aangulo3.get())
    elif band==2:
        mat=Calculos.M2(3,float(txt_edit_ang4.get(1.0, tk.END)),float(txt_edit_ang5.get(1.0, tk.END)),float(txt_edit_ang6.get(1.0, tk.END)))
    llenado(mat,6,9)

def dato2(band):
    if band==1:
        mat2=Calculos.M1(4,angulo1.get(),angulo2.get(),angulo3.get(),angulo4.get())
    elif band==2:
        mat2=Calculos.M1(4,float(txt_edit_ang0.get(1.0, tk.END)),float(txt_edit_ang1.get(1.0, tk.END)),float(txt_edit_ang2.get(1.0, tk.END)),int(txt_edit_ang3.get(1.0, tk.END)))
    llenado(mat2,1,5)

def dato3(band):
    if band==1:
        mat3=Calculos.M3(6,Rangulo1.get(),Rangulo2.get(),Rangulo3.get(),Rangulo4.get(),Rangulo5.get(),Rangulo6.get())
    elif band==2:
        mat3=Calculos.M3(6,float(txt_edit_ang7.get(1.0, tk.END)),float(txt_edit_ang8.get(1.0, tk.END)),float(txt_edit_ang9.get(1.0, tk.END)),float(txt_edit_ang10.get(1.0, tk.END))),float(txt_edit_ang11.get(1.0, tk.END)),float(txt_edit_ang12.get(1.0, tk.END))
    llenado(mat3,10,16)

#Funciones De Movimiento Scara (PR3)

def servo1(posiciones1):
    #Escritura De Angulo
    #print(b'Eb,'+posiciones1.encode()+b'\r\n')
    board.write(b'Eb,'+posiciones1.encode()+b'\r\n')
    #board.write(posiciones1.encode())
    #board.write(b'\r\n')
    sleep(0.2)
    dato2(1)

def servo2(posiciones2):
    #Escritura De Angulo
    board.write(b'Ebr,'+posiciones2.encode()+b'\r\n')
    sleep(0.2)
    #board.write(posiciones2.encode())
    #board.write(b'\r\n')
    dato2(1)

def servo3(posiciones3):
    #Escritura De Angulo
    board.write(b'Eab,'+posiciones3.encode()+b'\r\n')
    sleep(0.2)
    #board.write(posiciones3.encode())
    #board.write(b'\r\n')
    dato2(1)

def servo4(posiciones4):
    #Escritura De Angulo
    board.write(b'Em,'+posiciones4.encode()+b'\r\n')
    sleep(0.2)
    #board.write(posiciones4.encode())
    #board.write(b'\r\n')
    dato2(1)

#Funciones De Movimiento Antropomórfico (R3)

def Aservo1(Aposiciones1):
     #Escritura De Angulo
    board.write(b'Ab,'+Aposiciones1.encode()+b'\r\n')
    sleep(0.2)
    #board.write(Aposiciones1.encode())
    #board.write(b'\r\n')
    dato1(1)

def Aservo2(Aposiciones2):
    #Escritura De Angulo
    board.write(b'Abr,'+Aposiciones2.encode()+b'\r\n')
    sleep(0.2)
    #board.write(Aposiciones2.encode())
    #board.write(b'\r\n')
    dato1(1)

def Aservo3(Aposiciones3):
    #Escritura De Angulo
    board.write(b'Aab,'+Aposiciones3.encode()+b'\r\n')
    sleep(0.2)
    #board.write(Aposiciones3.encode())
    #board.write(b'\r\n')
    dato1(1)

#Funciones De Movimiento Antropomórfico (R6)

def Rservo1(posiciones1):
    #Escritura De Angulo
    #print(b'Eb,'+posiciones1.encode()+b'\r\n')
    board.write(b'Rb1,'+posiciones1.encode()+b'\r\n')
    #board.write(posiciones1.encode())
    #board.write(b'\r\n')
    sleep(0.2)
    dato3(1)

def Rservo2(posiciones2):
    #Escritura De Angulo
    board.write(b'Rbr1,'+posiciones2.encode()+b'\r\n')
    sleep(0.2)
    #board.write(posiciones2.encode())
    #board.write(b'\r\n')
    dato3(1)

def Rservo3(posiciones3):
    #Escritura De Angulo
    board.write(b'Rbr2,'+posiciones3.encode()+b'\r\n')
    sleep(0.2)
    #board.write(posiciones3.encode())
    #board.write(b'\r\n')
    dato3(1)

def Rservo4(posiciones4):
    #Escritura De Angulo
    board.write(b'Rb2,'+posiciones4.encode()+b'\r\n')
    sleep(0.2)
    #board.write(posiciones4.encode())
    #board.write(b'\r\n')
    dato3(1)

def Rservo5(posiciones5):
    #Escritura De Angulo
    board.write(b'Rab,'+posiciones5.encode()+b'\r\n')
    sleep(0.2)
    #board.write(posiciones4.encode())
    #board.write(b'\r\n')
    dato3(1)

def Rservo6(posiciones6):
    #Escritura De Angulo
    board.write(b'Rm,'+posiciones6.encode()+b'\r\n')
    sleep(0.2)
    #board.write(posiciones4.encode())
    #board.write(b'\r\n')
    dato3(1)


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
valor de lo que se desea mover. Luego presionar
el boton de envio correspondiente, se pretende obtener
las matrices individuales y totales de la cinematica 
directa en tiempo real.\n
""")

def info2():
    messagebox.showinfo("Informacion de uso",
"""
Modo de uso:\nDeslizar cada slider para darle
la posicion del efector final, para ello
se establecieron los limites mecanicos y del
espacio del trabajo del manipulador; Esto mediante
la descripcion y planteamiento de una ecuacion de 
circunferencia.
""")

#Serial
def close():
    board.write(b'bye\r\n')
    board.close()

def Envio_CAB_IK_Scara():
    #print("envio")
    board.write(b'Eb,'+"{:.3f}".format(float(text1.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Ebr,'+"{:.3f}".format(float(text2.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Eab,'+"{:.3f}".format(float(text3.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Em,'+"{:.3f}".format(float(text4.get(1.0, tk.END))).encode()+b'\r\n')

def Envio_CAR_IK_Scara():
    #print("envio")
    board.write(b'Eb,'+"{:.3f}".format(float(text1Ar.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Ebr,'+"{:.3f}".format(float(text2Ar.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Eab,'+"{:.3f}".format(float(text3Ar.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Em,'+"{:.3f}".format(float(text4Ar.get(1.0, tk.END))).encode()+b'\r\n')

#Envio de datos Scara (P3R)
def show_values1():
    print("Calculando...")

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

#Envio de datos Antropomórfico Bioloid (3R)
def show_values2():
    #Cuadro_Texto_1
    board.write(b'Ab,')
    board.write(txt_edit_ang4.get(1.0, tk.END).encode())

    #Cuadro_Texto_2
    board.write(b'Abr,')
    board.write(txt_edit_ang5.get(1.0, tk.END).encode())

    #Cuadro_Texto_3
    board.write(b'Aab,')
    board.write(txt_edit_ang6.get(1.0, tk.END).encode())

    dato1(2)

#Envio de datos Antropomorfico Kinova (6R)
def show_values3():
    #Cuadro_Texto_1
    board.write(b'Rb1,')
    board.write(txt_edit_ang7.get(1.0, tk.END).encode())

    #Cuadro_Texto_2
    board.write(b'Rbr1,')
    board.write(txt_edit_ang8.get(1.0, tk.END).encode())

    #Cuadro_Texto_3
    board.write(b'Rbr2,')
    board.write(txt_edit_ang9.get(1.0, tk.END).encode())

    #Cuadro_Texto_4
    board.write(b'Rb2,')
    board.write(txt_edit_ang10.get(1.0, tk.END).encode())

    #Cuadro_Texto_5
    board.write(b'Rab,')
    board.write(txt_edit_ang11.get(1.0, tk.END).encode())

     #Cuadro_Texto_6
    board.write(b'Rm,')
    board.write(txt_edit_ang12.get(1.0, tk.END).encode())

    dato3(2)

#VENTANA PRINCIPAL.
root = tkinter.Tk()
root.title('Controles de Manipuladores Roboticos')
#root.iconbitmap('../UMNG-robotica/two-sword.png')
root.geometry("1320x660")
creacion()
nombre = StringVar()
numero = IntVar()

#INCLUIMOS PANEL PARA LAS PESTAÑAS.
nb = ttk.Notebook(root)
nb.pack(fill='both',expand='yes')

#CREAMOS PESTAÑAS
pI = ttk.Frame(nb)#Pestaña De Información
p1 = ttk.Frame(nb)#Pestaña Robot Scara (P3R)
p2 = ttk.Frame(nb)#Pestaña Robot Antropomorfico Bioloid (3R)
p3 = ttk.Frame(nb)#Pestaña Robot Antropomorfico Kinova (6R)     
p4 = ttk.Frame(nb)#Pestaña Jacobiano

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
                resolution=0.5,
                orient = HORIZONTAL,
                length=266,
                troughcolor='gray',
                width = 30,
                cursor='dot',
                label = 'Desplazamiento Base',
                )
angulo1.place(rely=0)
#Text_Box
txt_edit_ang0 = tk.Text(frm1,width=6)
txt_edit_ang0.place(relx=1/5, rely=1/12+0.01, relheight=1/8-0.045)
txt_edit_ang0.insert(tk.END, "0")
        
#Brazo
#Slider
angulo2= Scale(frm1,
              command = servo2,
              from_=-90,
              to=90,
              resolution=0.5,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Brazo'  )
angulo2.place(rely=1/4)
#Text_Box
txt_edit_ang1 = tk.Text(frm1, width = 6)
txt_edit_ang1.place(relx=1/5, rely=4/12+0.01, relheight=1/8-0.045)
txt_edit_ang1.insert(tk.END, "0")

#Antebrazo
#Slider
angulo3= Scale(frm1,     
              command = servo3,         
              from_=-90,
              to=90,
              resolution=0.5,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Codo'  )
angulo3.place(rely=2/4)
#Text_Box
txt_edit_ang2 = tk.Text(frm1, width = 6)
txt_edit_ang2.place(relx=1/5, rely=7/12+0.011, relheight=1/8-0.045)
txt_edit_ang2.insert(tk.END, "0")

#Muñeca
#Slider
angulo4= Scale(frm1,
              command = servo4,
              from_=-90,
              to=90,
              resolution=0.5,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Muñeca'  )
angulo4.place(rely=3/4)
#Text_Box
txt_edit_ang3 = tk.Text(frm1, width = 6)
txt_edit_ang3.place(relx=1/5, rely=10/12+0.011, relheight=1/8-0.045)
txt_edit_ang3.insert(tk.END, "0")

#Frame Matrices Cinematica Directa DK (Contenedor)
frmdh1=LabelFrame(frm1,relief="raised")
frmdh1.place(relx=1/4+0.01, relwidth=1, relheight=1)

matrices(1,1,0,frmdh1)  #Matriz Link 1
matrices(2,1,8,frmdh1)  #Matriz Link 2
matrices(3,11,0,frmdh1) #Matriz Link 3
matrices(4,11,8,frmdh1) #Matriz Link 4
matrices(5,6,4,frmdh1)  #Matriz Total

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
txt_edit_xS =Scale(frm2,
                command = re_def_SLIDER,
                from_=-131.5,
                to=375.5,
                resolution=0.5,
                orient = HORIZONTAL,
                length=220,
                troughcolor='gray',
                width = 25,
                cursor='dot'
                )#tk.Text(frm2, width =8 , height=1)
txt_edit_xS.place(relx=0.035, rely=1/10-0.125)
        
#Text_Box Py
txt_edit_yS = Scale(frm2,
                command = re_def_SLIDER,
                from_=0,
                to=122.5,
                resolution=0.5,
                orient = HORIZONTAL,
                length=220,
                troughcolor='gray',
                width = 25,
                cursor='dot',
                digits=5,
                #state= DISABLED
                )#tk.Text(frm2, width =8 , height=1)
txt_edit_yS.place(relx=0.035, rely=0.225)

checkbox_value = BooleanVar()
checkbox = ttk.Checkbutton(frm2, 
                           text="-", 
                           variable=checkbox_value, 
                           command = re_def_SLIDER_clk)
checkbox.place(relx=0.21, rely=0.33)

#Text_Box Pz
txt_edit_zS =Scale(frm2,
                #command = re_def_SLIDER,
                from_=0,
                to=122.5,
                resolution=0.5,
                orient = HORIZONTAL,
                length=220,
                troughcolor='gray',
                width = 25,
                cursor='dot'
                )#tk.Text(frm2, width =8 , height=1)
txt_edit_zS.place(relx=0.035, rely=0.48)

#Text_Box Phi
txt_edit_phiS = Scale(frm2,
                from_=-270,
                to=270,
                resolution=0.5,
                orient = HORIZONTAL,
                length=220,
                troughcolor='gray',
                width = 25,
                cursor='dot'
                )#tk.Text(frm2, width =8 , height=1)#tk.Text(frm2, width =8 , height=1)
txt_edit_phiS.place(relx=0.035, rely=0.75)

#Boton Calcular Cinematica Inversa        
Calcular1=Button(frm2, text='Calcular', activebackground='yellow', command=Button_IK_Scara_P3R)
Calcular1.place(relx=2.5/10-0.01, rely=0.85, relheight=1/6-0.05)

info2_uso = Button(frm2,
             text="Modo de Uso",
             relief=GROOVE,
             command=info2   )
info2_uso.place(relx=0.9, rely=0.5)

#Frame Variables de Juntura Codo Abajo (Contenedor)
frmdh2=LabelFrame(frm2,relief="raised", text='Codo Abajo', labelanchor='n')
frmdh2.place(relx=0.3, rely=0.04, relwidth=0.22, relheight=0.78)

EnvioC_AB_S=Button(frm2, text='Enviar', activebackground='yellow', command=Envio_CAB_IK_Scara)
EnvioC_AB_S.place(relx=2.5/10+0.1, rely=0.85)

#Variable de Juntura 1
etiqueta1 = tk.Label(frmdh2, width=5, text="d₁", fg="black", bg="yellow").grid(column=0, row=0)
text1 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
text1.grid(row=0, column=1, sticky="nsew")

fila_vacia(1,1,frmdh2,10)

#Variable de Juntura 2
etiqueta2 = tk.Label(frmdh2, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=2)
text2 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
text2.grid(row=2, column=1, sticky="ew")

fila_vacia(3,1,frmdh2,10)

#Variable de Juntura 3
etiqueta3 = tk.Label(frmdh2, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=4)
text3 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
text3.grid(row=4, column=1, sticky="nsew")

fila_vacia(5,1,frmdh2,10)

#Variable de Juntura 4
etiqueta4 = tk.Label(frmdh2, width=5, text="θ₄", fg="black", bg="yellow").grid(column=0, row=6)
text4 = tk.Text(frmdh2, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
text4.grid(row=6, column=1, sticky="nsew")


#Frame Variables de Juntura Codo Arriba(Contenedor)
frmdh2Ar=LabelFrame(frm2,relief="raised", text='Codo Arriba', labelanchor='n')
frmdh2Ar.place(relx=0.6, rely=0.04, relwidth=0.22, relheight=0.78)

EnvioC_AR_S=Button(frm2, text='Enviar', activebackground='yellow', command=Envio_CAR_IK_Scara)
EnvioC_AR_S.place(relx=2.5/10+0.4, rely=0.85)

#Variable de Juntura 1
etiqueta1 = tk.Label(frmdh2Ar, width=5, text="d₁", fg="black", bg="yellow").grid(column=0, row=0)
text1Ar = tk.Text(frmdh2Ar, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
text1Ar.grid(row=0, column=1, sticky="nsew")

fila_vacia(1,1,frmdh2Ar,10)

#Variable de Juntura 2
etiqueta2 = tk.Label(frmdh2Ar, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=2)
text2Ar = tk.Text(frmdh2Ar, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
text2Ar.grid(row=2, column=1, sticky="ew")

fila_vacia(3,1,frmdh2Ar,10)

#Variable de Juntura 3
etiqueta3 = tk.Label(frmdh2Ar, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=4)
text3Ar = tk.Text(frmdh2Ar, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
text3Ar.grid(row=4, column=1, sticky="nsew")

fila_vacia(5,1,frmdh2Ar,10)

#Variable de Juntura 4
etiqueta4 = tk.Label(frmdh2Ar, width=5, text="θ₄", fg="black", bg="yellow").grid(column=0, row=6)
text4Ar = tk.Text(frmdh2Ar, padx= 20, pady=2, width=20, height=1, wrap="none", borderwidth=0)
text4Ar.grid(row=6, column=1, sticky="nsew")

fila_vacia(0,1,frmdh1,6)
fila_vacia(5,1,frmdh1,6)
fila_vacia(10,1,frmdh1,6)

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

Titulos_px = Label(frm2, width=2,text="Px")
Titulos_px.place(relx=0.009,rely=1/10-0.011)
Titulos_py = Label(frm2, width=2,text="Py")
Titulos_py.place(relx=0.009,rely=3/10+0.011)
Titulos_pz = Label(frm2, width=2,text="Pz")
Titulos_pz.place(relx=0.009,rely=6/10-0.012)
Titulos_pphi = Label(frm2, width=2,text="ϕ")
Titulos_pphi.place(relx=0.009,rely=8/10+0.05)

#####Pestaña 3#####

#Frame Manipulador Antropomorfico R3 (Contenedor)
frmA=LabelFrame(p2,relief="raised")
frmA.place(relwidth=1, relheight=1)

#Frame Cinematica Directa DK (Contenedor)
frm1A=LabelFrame(frmA,text='DK', labelanchor='n')
frm1A.place(relwidth=1, relheight=0.64)

#Base
#Slider
Aangulo1=Scale(frm1A,
                command = Aservo1,
                resolution=0.5,
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
txt_edit_ang4 = tk.Text(frm1A,width= 6)
txt_edit_ang4.place(relx=1/5, rely=1/12+0.01, relheight=1/8-0.045)
txt_edit_ang4.insert(tk.END, "0")
        
#Brazo
#Slider
Aangulo2= Scale(frm1A,
              command = Aservo2,
              resolution=0.5,
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
txt_edit_ang5 = tk.Text(frm1A, width = 6)
txt_edit_ang5.place(relx=1/5, rely=4/12+0.01, relheight=1/8-0.045)
txt_edit_ang5.insert(tk.END, "0")

#Antebrazo
#Slider
Aangulo3= Scale(frm1A,  
              command = Aservo3,  
              resolution=0.5,          
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
txt_edit_ang6 = tk.Text(frm1A, width = 6)
txt_edit_ang6.place(relx=1/5, rely=7/12+0.011, relheight=1/8-0.045)
txt_edit_ang6.insert(tk.END, "0")

#Frame Matrices Cinematica Directa DK (Contenedor)
frmdh1A=LabelFrame(frm1A,relief="raised")
frmdh1A.place(relx=0.35, relwidth=0.525, relheight=1)

matrices(6,1,0,frmdh1A)  #Matriz Link 1
columna_vacia(5,1,frmdh1A,6)
matrices(7,1,8,frmdh1A) #Matriz Link 2
columna_vacia(9,1,frmdh1A,6)
fila_vacia(5,4,frmdh1A,10)
matrices(8,9,0,frmdh1A) #Matriz Link 3
matrices(9,9,8,frmdh1A)  #Matriz Total

#Boton Envio Cinematica Directa Antropomorfico
Envio2=Button(frmdh1A, width=12, height=2, text='Envio', activebackground='yellow', command=show_values2)
Envio2.place(relx=4/9-0.05,rely=0.83)

#Boton Gripper Antropomorfico
BoC = Button(frm1A,text="Gripper",command=cerrar,bg='green',bd=3,height=2,width=10)
BoC.place(x=110,rely=3/4)

#Frame Cinematica Inversa IK (Contenedor)
frm2A=LabelFrame(frmA,text='IK', labelanchor='n')
frm2A.place(rely=0.65, relwidth=1, relheight=0.35)

#Text_Box Px
txt_edit_xA = tk.Text(frm2A, width=8, height=1)
txt_edit_xA.place(relx=1/10,rely=1/10+0.01)
txt_edit_xA.insert(tk.END, "0")
        
#Text_Box Py
txt_edit_yA = tk.Text(frm2A, width = 8, height=1)
txt_edit_yA.place(relx=1/10, rely=3/10+0.01)
txt_edit_yA.insert(tk.END, "0")

#Text_Box Pz
txt_edit_zA = tk.Text(frm2A, width = 8, height=1)
txt_edit_zA.place(relx=1/10, rely=5/10+0.01)
txt_edit_zA.insert(tk.END, "0")

#Boton Calcular Cinematica Inversa Antropomorfico        
Calcular2=Button(frm2A, text='Calcular', activebackground='yellow',command=Button_IK_Antropo_3R)
Calcular2.place(relx=1/10-0.01, rely=7/10+0.01, relheight=1/6-0.05)
###############
frmdh2A=LabelFrame(frm2A,relief="raised",text='Codo Abajo',labelanchor='n')
frmdh2A.place(relx=0.3, rely=0.1, relwidth=0.25, relheight=0.7)

#Variable de Juntura 1
etiqueta1 = tk.Label(frmdh2A, width=5, text="θ₁", fg="black", bg="yellow").grid(column=0, row=0)
text1A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text1A.grid(row=0, column=1, sticky="nsew")

#Variable de Juntura 2
etiqueta2 = tk.Label(frmdh2A, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=3)
text2A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text2A.grid(row=3, column=1, sticky="nsew")

fila_vacia(2,1,frmdh2A,10)

#Variable de Juntura 3
etiqueta3 = tk.Label(frmdh2A, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=6)
text3A = tk.Text(frmdh2A, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text3A.grid(row=6, column=1, sticky="nsew")

fila_vacia(5,1,frmdh2A,10)

###############
frmdh2AAr=LabelFrame(frm2A,relief="raised",text='Codo Arriba',labelanchor='n')
frmdh2AAr.place(relx=0.6, rely=0.1, relwidth=0.25, relheight=0.7)

#Variable de Juntura 1
etiqueta1 = tk.Label(frmdh2AAr, width=5, text="θ₁", fg="black", bg="yellow").grid(column=0, row=0)
text1AAr = tk.Text(frmdh2AAr, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text1AAr.grid(row=0, column=1, sticky="nsew")

#Variable de Juntura 2
etiqueta2 = tk.Label(frmdh2AAr, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=3)
text2AAr = tk.Text(frmdh2AAr, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text2AAr.grid(row=3, column=1, sticky="nsew")

fila_vacia(2,1,frmdh2AAr,10)

#Variable de Juntura 3
etiqueta3 = tk.Label(frmdh2AAr, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=6)
text3AAr = tk.Text(frmdh2AAr, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text3AAr.grid(row=6, column=1, sticky="nsew")

fila_vacia(5,1,frmdh2AAr,10)

#Titulos Antropomorfico (Label)
Titulos_l1 = Label(frmdh1A, width=11,text="Link 1")
Titulos_l1.place(relx=3/18-0.01,rely=0)
Titulos_l2 = Label(frmdh1A, width=11,text="Link 2")
Titulos_l2.place(relx=12/18-0.01,rely=0)
Titulos_l3 = Label(frmdh1A, width=11,text="Link 3")
Titulos_l3.place(relx=3/18-0.01,rely=7/14-0.03)
Titulos_lT = Label(frmdh1A, width=11,text="Total")
Titulos_lT.place(relx=12/18-0.01,rely=7/14-0.03)
Titulos_px = Label(frm2A, width=5,text="Px")
Titulos_px.place(relx=1/15,rely=1/10+0.01)
Titulos_py = Label(frm2A, width=5,text="Py")
Titulos_py.place(relx=1/15,rely=3/10+0.01)
Titulos_pz = Label(frm2A, width=5,text="Pz")
Titulos_pz.place(relx=1/15,rely=5/10+0.01)

#####Pestaña 4#####

#Combo Manipulador Antropomorfico R6 (Ventanas)
combo = ttk.Combobox(p4,
        state="readonly",
        values=["DK", "IK"]
)
combo.bind("<<ComboboxSelected>>", selection_changed)
combo.place(x=10, y=10)

#Frame Cinematica Directa DK (Contenedor)
frm6Rdk=LabelFrame(p4,text='DK', labelanchor='n')
frm6Rdk.place(rely=0.63, relwidth=1, relheight=0.37)
frm6Rdk.place_forget()

#Base1
#Slider
Rangulo1=Scale(frm6Rdk,
                command = Rservo1,
                resolution=0.5,
                from_=0,
                to=360,
                orient = HORIZONTAL,
                length=266,
                troughcolor='gray',
                width = 30,
                cursor='dot',
                label = 'Rotación Primera Base')
Rangulo1.place(rely=0)
#Text_Box
txt_edit_ang7 = tk.Text(frm6Rdk,width= 6)
txt_edit_ang7.place(relx=1/5, rely=1/21+0.015, relheight=1/10-0.05)
txt_edit_ang7.insert(tk.END, "0")
        
#Brazo1
#Slider
Rangulo2= Scale(frm6Rdk,
              command = Rservo2,
              resolution=0.5,
              from_=0,
              to=360,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Primer Brazo')
Rangulo2.place(rely=1/7)
#Text_Box
txt_edit_ang8 = tk.Text(frm6Rdk, width = 6)
txt_edit_ang8.place(relx=1/5, rely=4/21+0.015, relheight=1/10-0.05)
txt_edit_ang8.insert(tk.END, "0")

#Brazo2
#Slider
Rangulo3= Scale(frm6Rdk,  
              command = Rservo3,  
              resolution=0.5,          
              from_=0,
              to=360,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Segundo Brazo')
Rangulo3.place(rely=2/7)
#Text_Box
txt_edit_ang9 = tk.Text(frm6Rdk, width = 6)
txt_edit_ang9.place(relx=1/5, rely=7/21+0.015, relheight=1/10-0.05)
txt_edit_ang9.insert(tk.END, "0")

#Base2
#Slider
Rangulo4= Scale(frm6Rdk,  
              command = Rservo4,  
              resolution=0.5,          
              from_=0,
              to=360,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Segunda Base')
Rangulo4.place(rely=3/7)
#Text_Box
txt_edit_ang10 = tk.Text(frm6Rdk, width = 6)
txt_edit_ang10.place(relx=1/5, rely=10/21+0.015, relheight=1/10-0.05)
txt_edit_ang10.insert(tk.END, "0")

#Antebrazo
#Slider
Rangulo5= Scale(frm6Rdk,  
              command = Rservo5,  
              resolution=0.5,          
              from_=0,
              to=360,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Antebrazo')
Rangulo5.place(rely=4/7)
#Text_Box
txt_edit_ang11 = tk.Text(frm6Rdk, width = 6)
txt_edit_ang11.place(relx=1/5, rely=13/21+0.015, relheight=1/10-0.05)
txt_edit_ang11.insert(tk.END, "0")

#Muñeca
#Slider
Rangulo6= Scale(frm6Rdk,  
              command = Rservo6,  
              resolution=0.5,          
              from_=0,
              to=360,
              orient = HORIZONTAL,
              length=266,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Muñeca')
Rangulo6.place(rely=5/7)
#Text_Box
txt_edit_ang12 = tk.Text(frm6Rdk, width = 6)
txt_edit_ang12.place(relx=1/5, rely=16/21+0.015, relheight=1/10-0.05)
txt_edit_ang12.insert(tk.END, "0")

#Frame Matrices Cinematica Directa DK (Contenedor)
frmdh1R=LabelFrame(frm6Rdk,relief="raised")
frmdh1R.place(relx=1/4+0.01, relwidth=1, relheight=1)

fila_vacia(0,1,frmdh1R,10)
matrices(10,1,0,frmdh1R)   #Matriz Link 1
matrices(11,1,8,frmdh1R)   #Matriz Link 2
matrices(12,5,4,frmdh1R)   #Matriz Link 3
matrices(13,9,0,frmdh1R)   #Matriz Link 4
matrices(14,9,8,frmdh1R)   #Matriz Link 5
matrices(15,13,4,frmdh1R)  #Matriz Link 6
fila_vacia(17,2,frmdh1R,6) 
matrices(16,19,4,frmdh1R)  #Matriz Total

#Titulos Antropomórfico (R6) (Label)
Titulos_l1 = Label(frmdh1R, width=11,text="Link 1")
Titulos_l1.place(relx=2/24+0.01,rely=0)
Titulos_l2 = Label(frmdh1R, width=11,text="Link 2")
Titulos_l2.place(relx=14/24-0.005,rely=0)
Titulos_l3 = Label(frmdh1R, width=11,text="Link 3")
Titulos_l3.place(relx=5/15,rely=4/23)
Titulos_l4 = Label(frmdh1R, width=11,text="Link 4")
Titulos_l4.place(relx=2/24+0.01,rely=8/23)
Titulos_l5 = Label(frmdh1R, width=11,text="Link 5")
Titulos_l5.place(relx=14/24-0.005,rely=8/23)
Titulos_l6 = Label(frmdh1R, width=11,text="Link 6")
Titulos_l6.place(relx=5/15,rely=12/23-0.01)
Titulos_lT = Label(frmdh1R, width=11,text="Total")
Titulos_lT.place(relx=5/15,rely=17/23+0.01)

frm6Rik=LabelFrame(p4,text='IK', labelanchor='n')
frm6Rik.place(rely=0.63, relwidth=1, relheight=0.37)
frm6Rik.place_forget()

#Jacobiano
frmJACO=LabelFrame(p3, labelanchor='n')
frmJACO.place(relwidth=1, relheight=1)

fila_vacia(0,2,frmJACO,10)

#Matriz Jaco S
for r in range(0, 6):
    for c in range(0, 4):
        cell = Entry(frmJACO, width=12,  textvariable=globals()["jacoS_" + str(r) + str(c)], state= DISABLED)
        cell.grid(row=r+2, column=c+1, ipady=4)

columna_vacia(9,1,frmJACO,10)

#Matriz Jaco A
for r in range(0, 6):
    for c in range(0, 3):
        cell = Entry(frmJACO, width=12,  textvariable=globals()["jacoA_" + str(r) + str(c)], state= DISABLED)
        cell.grid(row=r+2, column=c+10, ipady=4)

fila_vacia(9,1,frmJACO,10)

#Matriz Jaco R
for r in range(0, 6):
    for c in range(0, 6):
        cell = Entry(frmJACO, width=12,  textvariable=globals()["jacoR_" + str(r) + str(c)], state= DISABLED)
        cell.grid(row=r+10, column=c+6, ipady=4)

#Titulos Jacobianos (Label)
Titulos_JS = Label(frmJACO, width=15,text="Jacobiano Scara")
Titulos_JS.place(relx=2/24+0.01,rely=0.005)
Titulos_JA = Label(frmJACO, width=20,text="Jacobiano Antropomorfico")
Titulos_JA.place(relx=14/24+0.005,rely=0.005)
Titulos_JR = Label(frmJACO, width=11,text="Jacobiano 6R")
Titulos_JR.place(relx=12/18-0.2,rely=7/14+0.08)

CalcularJACO=Button(frmJACO, text='Calcular', activebackground='yellow', command=Button_CalcularJACO, width=12)
CalcularJACO.place(relx=2.5/10-0.01, rely=0.85, relheight=1/6-0.05)

#AGREGAMOS PESTAÑAS CREADAS
nb.add(pI,text='Portada')
nb.add(p1,text='Robot Scara (P3R)')
nb.add(p2,text='Robot Antropomorfico (3R)')
nb.add(p4,text='Antropomorfico (6R)')
nb.add(p3,text='Jacobiano')

root.mainloop()