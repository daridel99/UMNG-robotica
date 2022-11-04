import tkinter 
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import HORIZONTAL, PhotoImage, StringVar, Widget
from time import sleep
import numpy as np
import serial, serial.tools.list_ports
import Calculos
import Funciones as Fnc
from threading import Thread

#Configuracion COM
board =serial.Serial(port='COM1', baudrate=19200)
sleep(5) #5 Segundos Para Que Establezca La Comunicacion

# def data_3D():
#     return 1,1,1,6,7,9,7,2 #xi yi zi xf yf zf tf codo

def But_Perfiles():#Funcion Para Calcular La Generación de Trayectorias
    Vectores=Fnc.Perfil(get.tipe,get.manipulador,get.codo,get.tfinal,get.xini,get.yini,get.ziini,get.xfin,get.yfin,get.zfin,get.resolucion,get.variable)
    if Vectores[0]==1:
        messagebox.showinfo(title="error", message="La magnitud de la velocidad supera la condición. \n \t Varie el los valores de la velocidad crucero")
    elif Vectores[0]==2:
        messagebox.showinfo(title="error", message="La magnitud de la aceleración supera la condición. \n \t Varie el los valores de la aceleración crucero")
    else:  
        Posq1.plot(Vectores[1])
        Posq2.plot(Vectores[2])
        Posq3.plot(Vectores[3])
        Velq1.plot(Vectores[4])
        Velq2.plot(Vectores[5])
        Velq3.plot(Vectores[6])
        posx=np.array([],float)
        posy=np.array([],float)
        posz=np.array([],float)
        for n in range(0,get.resolucion):
            if get.manipulador==1:
                mat=Calculos.M1(3,Vectores[1][n],Vectores[2][n],Vectores[3][n])
                vect_pos=Calculos.Vec(4,mat[0])
                posx[n]=vect_pos[0]
                posy[n]=vect_pos[1]
                posz[n]=vect_pos[2]
            else:
                mat=Calculos.M2(3,Vectores[1][n],Vectores[2][n],Vectores[3][n])
                vect_pos=Calculos.Vec(4,mat[0])
                posx[n]=vect_pos[0]
                posy[n]=vect_pos[1]
                posz[n]=vect_pos[2]
        #Enviar (posx,posy,posz) a grafica 3D y graficar.
    
def But_IK_S(): #Función Para Calcular Cinematica Inversa Del Scara

    M=Calculos.IK_Scara_P3R(float(PX_S.get()), float(PY_S.get()), float(PZ_S.get()))
    #Boton Envio Codo Abajo
    EnvioC_AB_S.place(relx=2.5/10+0.1, rely=0.85)
    #Boton Envio Codo Arriba
    EnvioC_AR_S.place(relx=2.5/10+0.4, rely=0.85)
    
    #Desabilitación de Botones de Envio Cinematica Inversa
    if M[5] == 1 or M[6] == 1: #indar indab
        if  M[6] == 1:#indab
            EnvioC_AB_S.place_forget()
        if  M[5] == 1:#indar
            EnvioC_AR_S.place_forget()
        messagebox.showinfo(title="error",
        message="Una o ambas soluciones supera los limites mecanicos. \n \t \t Varie el valor del punto")

    #Inserta Valores de Variables de Juntura en La Interfaz (Codo Abajo y Codo Arriba)
    text1.delete("1.0","end")
    text1.insert( tk.END,str(M[0]))
    text1Ar.delete("1.0","end")
    text1Ar.insert(tk.END, str(M[0]))
    text2.delete("1.0","end")
    text2.insert( tk.END,str(M[1]))
    text2Ar.delete("1.0","end")
    text2Ar.insert(tk.END, str(M[3]))
    text3.delete("1.0","end")
    text3.insert( tk.END,str(M[2]))
    text3Ar.delete("1.0","end")
    text3Ar.insert(tk.END, str(M[4]))
    #Re-Llenado de Matrices DK (Corroborar que la solución Es Correcta)
    Fnc.llenado(Calculos.M1(3, M[0], M[1], M[2]),1,4) 

def But_IK_R3(): #Función Para Calcular Cinematica Inversa Del Antropomórfico (R3)

    M=Calculos.IK_Antropo_3R(float(txt_edit_xA.get()), float(txt_edit_yA.get()),float( txt_edit_zA.get()))
    #Boton Envio Codo Abajo
    EnvioC_AB_A.place(relx=2.5/10+0.1, rely=0.85)
    #Boton Envio Codo Arriba
    EnvioC_AR_A.place(relx=2.5/10+0.4, rely=0.85)

    #Desabilitación de Botones de Envio Cinematica Inversa
    if M[6] == 1 or M[5] == 1: #indar indab
        if  M[5] == 1:#indab
            EnvioC_AB_A.place_forget()
        if  M[6] == 1:#indar
            EnvioC_AR_A.place_forget()
        messagebox.showinfo(title="error", message="Una o ambas soluciones supera los limites mecanicos. \n \t \t Varie el valor del punto")

     #Inserta Valores de Variables de Juntura en La Interfaz (Codo Abajo y Codo Arriba)
    text1A.delete("1.0","end")
    text1A.insert( tk.END,str(M[0]))
    text1AAr.delete("1.0","end")
    text1AAr.insert(tk.END, str(M[0]))
    text2A.delete("1.0","end")
    text2A.insert( tk.END,str(M[1]))
    text2AAr.delete("1.0","end")
    text2AAr.insert(tk.END, str(M[3]))
    text3A.delete("1.0","end")
    text3A.insert( tk.END,str(M[2]))
    text3AAr.delete("1.0","end")
    text3AAr.insert(tk.END, str(M[4]))
    #Re-Llenado de Matrices DK (Corroborar que la solución Es Correcta)
    Fnc.llenado(Calculos.M2(3, M[0], M[1], M[2]),5,8) 

def Button_CalcularJACO(): #Función Para Calcular Jacobianos 
    J_A=Calculos.JG_A(3,Aangulo1.get(),Aangulo2.get(),Aangulo3.get())
    J_S=Calculos.JG_S(4,angulo1.get(),angulo2.get(),angulo3.get())
    J_R=Calculos.JG_R()
    Fnc.llenado_JACO(J_A,J_S,J_R)

def re_def_SLIDER(IKxS): #Función Para Redefinir Sliders
    LimitY=Calculos.varX_scara(PX_S.get())
    PY_S.place(relx=1/10, rely=3/10-0.1)
    supe=LimitY[0]
    infe=LimitY[1]
    PY_S['state']='active'
    
    if LimitY[2]== 0 :
        checkbox.place_forget()
        globals() ["PY_S_var"] = PY_S.get()
        PY_S['from_']=str(infe)
        PY_S['to']=str(supe)
    else:
        checkbox.place(relx=0.25, rely=0.3)
        if checkbox_value.get():           
            PY_S['from_']=str(float(-1)*supe)
            PY_S['to']=str(float(-1)*infe)
        else:           
            PY_S['from_']=str(infe)
            PY_S['to']=str(supe)

def re_def_SLIDER_clk():#Función Para Actualizar Slider Al Clickear el Check_Box
    re_def_SLIDER(0)

def selection_changed(event):#Función Mensaje Para Ventanas Pestaña 4
    selection = combo.get()
    if selection == "DK":
        FrIKR6.place_forget()
        FrDKR6.place(rely=0.05, relwidth=1, relheight=0.95)
    else:
        FrDKR6.place_forget()
        FrIKR6.place(rely=0.05, relwidth=1, relheight=0.95)
    #messagebox.showinfo(
     #   title="Nuevo elemento seleccionado",
      #  message=selection
    #)

def dato1(band):#Función Para Calcular DK Antropomórfico (R3)
    if band==1:
        mat=Calculos.M2(3,Aangulo1.get(),Aangulo2.get(),Aangulo3.get())
    elif band==2:
        mat=Calculos.M2(3,float(txt_edit_ang4.get(1.0, tk.END)),float(txt_edit_ang5.get(1.0, tk.END)),float(txt_edit_ang6.get(1.0, tk.END)))
    Fnc.llenado(mat,5,8)

def dato2(band):#Función Para Calcular DK Scara (PR3)
    if band==1:
        mat2=Calculos.M1(3,angulo1.get(),angulo2.get(),angulo3.get())
    elif band==2:
        mat2=Calculos.M1(3,float(txt_edit_ang0.get(1.0, tk.END)),float(txt_edit_ang1.get(1.0, tk.END)),float(txt_edit_ang2.get(1.0, tk.END)))
    Fnc.llenado(mat2,1,4)

def dato3(band):#Función Para Calcular DK Antropomórfico (R6)
    if band==1:
        mat3=Calculos.M3(6,Rangulo1.get(),Rangulo2.get(),Rangulo3.get(),Rangulo4.get(),Rangulo5.get(),Rangulo6.get())
    elif band==2:
        mat3=Calculos.M3(6,float(txt_edit_ang7.get(1.0, tk.END)),float(txt_edit_ang8.get(1.0, tk.END)),float(txt_edit_ang9.get(1.0, tk.END)),float(txt_edit_ang10.get(1.0, tk.END))),float(txt_edit_ang11.get(1.0, tk.END)),float(txt_edit_ang12.get(1.0, tk.END))
    Fnc.llenado(mat3,9,15)

def contar():
    while pbr_tarea['value'] < 100:
        pbr_tarea['value'] += 10
        sleep(0.02)
    pbr_tarea['value'] = 0

#Funciones De Sliders Scara (PR3)
def servo1(posiciones1):
    if board.isOpen():
        #pbr_tarea["background"]='green'
        pbr_tarea['value'] = 0
        Thread(target=contar).start()
        board.write(b'Eb,'+posiciones1.encode()+b'\r\n')
    else:
        pbr_tarea['value'] = 100
        pbr_tarea.configure(style='red.Horizontal.TProgressbar')
    dato2(1)

def servo2(posiciones2):
    Thread(target=contar).start()
    board.write(b'Ebr,'+posiciones2.encode()+b'\r\n')
    dato2(1)

def servo3(posiciones3):
    Thread(target=contar).start()
    board.write(b'Eab,'+posiciones3.encode()+b'\r\n')
    dato2(1)

#Funciones De Sliders Antropomórfico (R3)
def Aservo1(Aposiciones1):
    #Thread(target=contar).start()
    board.write(b'Ab,'+Aposiciones1.encode()+b'\r\n')
    dato1(1)

def Aservo2(Aposiciones2):
    #Thread(target=contar).start()
    board.write(b'Abr,'+Aposiciones2.encode()+b'\r\n')
    dato1(1)

def Aservo3(Aposiciones3):
    #Thread(target=contar).start()
    board.write(b'Aab,'+Aposiciones3.encode()+b'\r\n')
    dato1(1)

#Funciones De Sliders Antropomórfico (R6)
def Rservo1(posiciones1):
    #Thread(target=contar).start()
    board.write(b'Rb1,'+posiciones1.encode()+b'\r\n')
    sleep(0.2)
    dato3(1)

def Rservo2(posiciones2):
    #Thread(target=contar).start()
    board.write(b'Rbr1,'+posiciones2.encode()+b'\r\n')
    sleep(0.2)
    dato3(1)

def Rservo3(posiciones3):
    #Thread(target=contar).start()
    board.write(b'Rbr2,'+posiciones3.encode()+b'\r\n')
    sleep(0.2)
    dato3(1)

def Rservo4(posiciones4):
    #Thread(target=contar).start()
    board.write(b'Rb2,'+posiciones4.encode()+b'\r\n')
    sleep(0.2)
    dato3(1)

def Rservo5(posiciones5):
    #Thread(target=contar).start()
    board.write(b'Rab,'+posiciones5.encode()+b'\r\n')
    sleep(0.2)
    dato3(1)

def Rservo6(posiciones6):
    #Thread(target=contar).start()
    board.write(b'Rm,'+posiciones6.encode()+b'\r\n')
    sleep(0.2)
    dato3(1)

#Gripper
globals()["clickeo"]=True
def abrir():#Función Abrir Gripper
    if  globals()["clickeo"]:
        globals()["clickeo"]=globals()["clickeo"]^1
        BoA["bg"]="red"
        board.write(b'E0 \r\n')
    
    else:
        globals()["clickeo"]=globals()["clickeo"]^1
        BoA["bg"]="green"
        board.write(b'E1 \r\n')

globals()["clickeo1"]=True
def cerrar():#Función Cerrar Gripper
    if  globals()["clickeo1"]:
        globals()["clickeo1"]=globals()["clickeo1"]^1
        BoC["bg"]="red"
        board.write(b'A0 \r\n')
    else:
        globals()["clickeo1"]=globals()["clickeo1"]^1
        BoC["bg"]="green"
        board.write(b'A1 \r\n')

def info():#Función Información DK
    messagebox.showinfo("Informacion de uso",
"""
Modo de uso:\nDesplazar cada slider para mover
las articulaciones del brazo robotico o digitar el
valor de lo que se desea mover. Luego presionar
el boton de envio correspondiente, se pretende obtener
las matrices individuales y totales de la cinematica 
directa en tiempo real.\n
""")

def info2():#Función Información IK
    #pbr_tarea['value'] = 0
    messagebox.showinfo("Informacion de uso",
"""
Modo de uso:\nDeslizar cada slider para darle
la posicion del efector final, para ello
se establecieron los limites mecanicos y del
espacio del trabajo del manipulador; Esto mediante
la descripcion y planteamiento de una ecuacion de 
circunferencia.
""")

def close(): #Cerrar Puerto Serial
    #board.write(b'bye\r\n')
    board.close()
    root.destroy()

def Envio_DK_S():#Función Envio Text-Box DK Scara (P3R)
    #Cuadro_Texto_1
    board.write(b'Eb,'+txt_edit_ang0.get(1.0, tk.END).encode()+b'\r\n')  
    sleep(0.2)
    #Cuadro_Texto_2
    board.write(b'Ebr,'+txt_edit_ang1.get(1.0, tk.END).encode()+b'\r\n')
    sleep(0.2)
    #Cuadro_Texto_3 
    board.write(b'Eab,'+txt_edit_ang2.get(1.0, tk.END).encode()+b'\r\n')
    sleep(0.2)
    dato2(2)

def Envio_DK_R3():#Función Envio Text-Box DK Antropomórfico (R3)
    #Cuadro_Texto_1
    board.write(b'Ab,'+txt_edit_ang4.get(1.0, tk.END).encode()+b'\r\n')

    #Cuadro_Texto_2
    board.write(b'Abr,'+txt_edit_ang5.get(1.0, tk.END).encode()+b'\r\n')

    #Cuadro_Texto_3
    board.write(b'Aab,'+txt_edit_ang6.get(1.0, tk.END).encode()+b'\r\n')

    dato1(2)

def show_values3():#Función Envio Text-Box DK Antropomórfico (R6)
    #Cuadro_Texto_1
    board.write(b'Rb1,'+txt_edit_ang7.get(1.0, tk.END).encode())

    #Cuadro_Texto_2
    board.write(b'Rbr1,'+txt_edit_ang8.get(1.0, tk.END).encode()+b'\r\n')

    #Cuadro_Texto_3
    board.write(b'Rbr2,'+txt_edit_ang9.get(1.0, tk.END).encode()+b'\r\n')

    #Cuadro_Texto_4
    board.write(b'Rb2,'+txt_edit_ang10.get(1.0, tk.END).encode()+b'\r\n')

    #Cuadro_Texto_5
    board.write(b'Rab,'+txt_edit_ang11.get(1.0, tk.END).encode()+b'\r\n')

    #Cuadro_Texto_6
    board.write(b'Rm,'+txt_edit_ang12.get(1.0, tk.END).encode()+b'\r\n')

    dato3(2)

def Envio_CD_A(): #Envio Codo Abajo Antropomorfico R3
    #insertar condicion
    board.write(b'Ab,'+"{:.1f}".format(float(text1A.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Abr,'+"{:.1f}".format(float(text2A.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Aab,'+"{:.1f}".format(float(text3A.get(1.0, tk.END))).encode()+b'\r\n')

def Envio_CD_S(): #Envio Codo Abajo Scara
    #insertar condicion
    board.write(b'Eb,'+"{:.1f}".format(float(text1.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Ebr,'+"{:.1f}".format(float(text2.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.02)
    board.write(b'Eab,'+"{:.1f}".format(float(text3.get(1.0, tk.END))).encode()+b'\r\n')

def Envio_CU_A():#Envio Codo Arriba Antropomorfico R3
    #insertar condicion
    board.write(b'Ab,'+"{:.1f}".format(float(text1AAr.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.2)
    board.write(b'Abr,'+"{:.1f}".format(float(text2AAr.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.2)
    board.write(b'Aab,'+"{:.1f}".format(float(text3AAr.get(1.0, tk.END))).encode()+b'\r\n')

def Envio_CU_S():#Envio Codo Arriba Scara
    board.write(b'Eb,'+"{:.1f}".format(float(text1Ar.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.2)
    board.write(b'Ebr,'+"{:.1f}".format(float(text2Ar.get(1.0, tk.END))).encode()+b'\r\n')
    sleep(0.2)
    board.write(b'Eab,'+"{:.1f}".format(float(text3Ar.get(1.0, tk.END))).encode()+b'\r\n')

##################### VENTANA PRINCIPAL #########################
root = tkinter.Tk()
root.title('Controles de Manipuladores Roboticos')
#root.iconbitmap('../UMNG-robotica/two-sword.png')
root.geometry("1320x660")
Fnc.creacion()
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
p5 = ttk.Frame(nb)#Planeación de trayectorias

######hilo
#hilo1 = threading.Thread(target=contar)
#####Pestaña 1: Información#####

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

#Logo UMNG
img= PhotoImage(file='./LOGOUMNG.png')
img_zoom=img.zoom(2)
widget = Label(fi, image=img_zoom)
widget.place(relwidth=0.3,relheight=0.6)

#Logo Robot
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

#####Pestaña 2: Scara (PR3)#####

#Frame Global (Contenedor)
FrS=LabelFrame(p1,relief="raised")
FrS.place(relwidth=1, relheight=1)

#Frame Cinematica Directa DK (Contenedor)
FrDKS=LabelFrame(FrS,text='DK', labelanchor='n')
FrDKS.place(relwidth=1, relheight=0.64)

#Base
#Slider
angulo1=Scale(FrDKS,
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
txt_edit_ang0 = tk.Text(FrDKS,width=6)
txt_edit_ang0.place(relx=1/5, rely=1/12+0.01, relheight=1/8-0.045)
txt_edit_ang0.insert(tk.END, "0")
        
#Brazo
#Slider
angulo2= Scale(FrDKS,
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
txt_edit_ang1 = tk.Text(FrDKS, width = 6)
txt_edit_ang1.place(relx=1/5, rely=4/12+0.01, relheight=1/8-0.045)
txt_edit_ang1.insert(tk.END, "0")

#Antebrazo
#Slider
angulo3= Scale(FrDKS,     
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
txt_edit_ang2 = tk.Text(FrDKS, width = 6)
txt_edit_ang2.place(relx=1/5, rely=7/12+0.011, relheight=1/8-0.045)
txt_edit_ang2.insert(tk.END, "0")

#Frame Matrices (Contenedor)
FrMaS=LabelFrame(FrDKS,relief="raised")
FrMaS.place(relx=0.35, relwidth=0.525, relheight=1)

Fnc.matrices(1,1,0,FrMaS)  #Matriz Link 1
Fnc.matrices(2,1,8,FrMaS)  #Matriz Link 2
Fnc.matrices(3,9,0,FrMaS) #Matriz Link 3
Fnc.matrices(4,9,8,FrMaS)  #Matriz Total

#Frame Cinematica Inversa IK (Contenedor)
FrIKS=LabelFrame(FrS,text='IK', labelanchor='n')
FrIKS.place(rely=0.65, relwidth=1, relheight=0.35)

#Slider PX
PX_S =Scale(FrIKS,
                command = re_def_SLIDER,
                from_=-131.5,
                to=375.5,
                resolution=0.5,
                orient = HORIZONTAL,
                length=180,
                troughcolor='gray',
                width = 20,
                cursor='dot'
                )
PX_S.place(relx=1/10,rely=1/10-0.1)
        
#Slider Py
PY_S = Scale(FrIKS,
                command = re_def_SLIDER,
                from_=0,
                to=122.5,
                resolution=0.5,
                orient = HORIZONTAL,
                length=180,
                troughcolor='gray',
                width = 20,
                cursor='dot',
                digits=5,
                )
PY_S.place(relx=1/10, rely=3/10-0.1)

#Slider Pz
PZ_S =Scale(FrIKS,
                #command = re_def_SLIDER,
                from_=0,
                to=122.5,
                resolution=0.5,
                orient = HORIZONTAL,
                length=180,
                troughcolor='gray',
                width = 20,
                cursor='dot'
                )
PZ_S.place(relx=1/10, rely=5/10-0.1)

#CheckBox Para Valores Negativos
checkbox_value = BooleanVar()
checkbox = ttk.Checkbutton(FrIKS, 
                           text="-", 
                           variable=checkbox_value, 
                           command = re_def_SLIDER_clk)
checkbox.place(relx=0.25, rely=0.3)

#Frame Variables de Juntura Codo Abajo (Contenedor)
FrSCD=LabelFrame(FrIKS,relief="raised", text='Codo Abajo', labelanchor='n')
FrSCD.place(relx=0.3, rely=0.1, relwidth=0.25, relheight=0.7)

#Variable de Juntura 1
etiqueta1 = tk.Label(FrSCD, width=5, text="d₁", fg="black", bg="yellow").grid(column=0, row=0)
text1 = tk.Text(FrSCD, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text1.grid(row=0, column=1, sticky="nsew")

#Variable de Juntura 2
etiqueta2 = tk.Label(FrSCD, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=2)
text2 = tk.Text(FrSCD, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text2.grid(row=2, column=1, sticky="ew")

#Variable de Juntura 3
etiqueta3 = tk.Label(FrSCD, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=4)
text3 = tk.Text(FrSCD, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text3.grid(row=4, column=1, sticky="nsew")

#Frame Variables de Juntura Codo Arriba(Contenedor)
FrSCU=LabelFrame(FrIKS,relief="raised", text='Codo Arriba', labelanchor='n')
FrSCU.place(relx=0.6, rely=0.1, relwidth=0.25, relheight=0.7)

#Variable de Juntura 1
etiqueta1 = tk.Label(FrSCU, width=5, text="d₁", fg="black", bg="yellow").grid(column=0, row=0)
text1Ar = tk.Text(FrSCU, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text1Ar.grid(row=0, column=1, sticky="nsew")

#Variable de Juntura 2
etiqueta2 = tk.Label(FrSCU, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=2)
text2Ar = tk.Text(FrSCU, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text2Ar.grid(row=2, column=1, sticky="ew")

#Variable de Juntura 3
etiqueta3 = tk.Label(FrSCU, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=4)
text3Ar = tk.Text(FrSCU, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text3Ar.grid(row=4, column=1, sticky="nsew")

#Filas Vacias Para Variables De Juntura
Fnc.fila_vacia(1,1,FrSCD,10)
Fnc.fila_vacia(3,1,FrSCD,10)
Fnc.fila_vacia(1,1,FrSCU,10)
Fnc.fila_vacia(3,1,FrSCU,10)

#Filas Vacias Para Matrices
Fnc.columna_vacia(5,1,FrMaS,6)
Fnc.columna_vacia(9,1,FrMaS,6)
Fnc.fila_vacia(5,4,FrMaS,10)


#Titulos Scara (Label)
Titulos_l1 = Label(FrMaS, width=11,text="Link 1")
Titulos_l1.place(relx=3/18-0.01,rely=0)
Titulos_l2 = Label(FrMaS, width=11,text="Link 2")
Titulos_l2.place(relx=12/18-0.01,rely=0)
Titulos_l3 = Label(FrMaS, width=11,text="Link 3")
Titulos_l3.place(relx=3/18-0.01,rely=7/14-0.03)
Titulos_lT = Label(FrMaS, width=11,text="Total")
Titulos_lT.place(relx=12/18-0.01,rely=7/14-0.03)
Titulos_px = Label(FrIKS, width=2,text="Px")
Titulos_px.place(relx=1/15,rely=1/10+0.01)
Titulos_py = Label(FrIKS, width=2,text="Py")
Titulos_py.place(relx=1/15,rely=3/10+0.01)
Titulos_pz = Label(FrIKS, width=2,text="Pz")
Titulos_pz.place(relx=1/15,rely=5/10+0.01)

#Boton Envio DK
Envio1=Button(FrMaS, width=12, height=2, text='Envio', activebackground='yellow', command=Envio_DK_S)
Envio1.place(relx=4/9-0.05,rely=0.83)

#Boton Gripper Scara
BoA = Button(FrDKS,text="Gripper",command=abrir, bg='green', bd=3, height=2, width=10)
BoA.place(x=110,rely=3/4)

#Boton Calcular IK        
Calcular1=Button(FrIKS, text='Calcular', activebackground='yellow', command=But_IK_S)
Calcular1.place(relx=1/10-0.01, rely=7/10+0.01, relheight=1/6-0.05)

#Boton Envio Codo Abajo
EnvioC_AB_S=Button(FrIKS, text='Enviar', activebackground='yellow', command=Envio_CD_S)
EnvioC_AB_S.place(relx=2.5/10+0.1, rely=0.85)

#Boton Envio Codo Arriba
EnvioC_AR_S=Button(FrIKS, text='Enviar', activebackground='yellow', command=Envio_CU_S)
EnvioC_AR_S.place(relx=2.5/10+0.4, rely=0.85)

s = ttk.Style()
s.theme_use('alt')
s.configure("red.Horizontal.TProgressbar", background='red')
s.configure("green.Horizontal.TProgressbar", background='green')
pbr_tarea = ttk.Progressbar(FrIKS, length=150, style='green.Horizontal.TProgressbar', maximum=100)
pbr_tarea['value'] = 0
pbr_tarea.place(relx=0.87, rely=0.25)
#Boton Información IK
info2_uso = Button(FrIKS,
             text="Modo de Uso",
             relief=GROOVE,
             command=info2   )
info2_uso.place(relx=0.879, rely=0.5)

#####Pestaña 3: Antropomórfico (R3)#####

#Frame Global (Contenedor)
FrR3=LabelFrame(p2,relief="raised")
FrR3.place(relwidth=1, relheight=1)

#Frame Cinemática Directa DK (Contenedor)
FrDKR3=LabelFrame(FrR3,text='DK', labelanchor='n')
FrDKR3.place(relwidth=1, relheight=0.64)

#Base
#Slider
Aangulo1=Scale(FrDKR3,
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
txt_edit_ang4 = tk.Text(FrDKR3,width= 6)
txt_edit_ang4.place(relx=1/5, rely=1/12+0.01, relheight=1/8-0.045)
txt_edit_ang4.insert(tk.END, "0")
        
#Brazo
#Slider
Aangulo2= Scale(FrDKR3,
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
txt_edit_ang5 = tk.Text(FrDKR3, width = 6)
txt_edit_ang5.place(relx=1/5, rely=4/12+0.01, relheight=1/8-0.045)
txt_edit_ang5.insert(tk.END, "0")

#Antebrazo
#Slider
Aangulo3= Scale(FrDKR3,  
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
txt_edit_ang6 = tk.Text(FrDKR3, width = 6)
txt_edit_ang6.place(relx=1/5, rely=7/12+0.011, relheight=1/8-0.045)
txt_edit_ang6.insert(tk.END, "0")

#Frame Matrices (Contenedor)
FrMaR3=LabelFrame(FrDKR3,relief="raised")
FrMaR3.place(relx=0.35, relwidth=0.525, relheight=1)

Fnc.matrices(5,1,0,FrMaR3)  #Matriz Link 1
Fnc.matrices(6,1,8,FrMaR3)  #Matriz Link 2
Fnc.matrices(7,9,0,FrMaR3)  #Matriz Link 3
Fnc.matrices(8,9,8,FrMaR3)  #Matriz Total

#Boton Envio Cinematica Directa Antropomorfico
Envio2=Button(FrMaR3, width=12, height=2, text='Envio', activebackground='yellow', command=Envio_DK_R3)
Envio2.place(relx=4/9-0.05,rely=0.83)

#Boton Gripper Antropomorfico
BoC = Button(FrDKR3,text="Gripper",command=cerrar,bg='green',bd=3,height=2,width=10)
BoC.place(x=110,rely=3/4)

#Frame Cinematica Inversa IK (Contenedor)
FrIKR3=LabelFrame(FrR3,text='IK', labelanchor='n')
FrIKR3.place(rely=0.65, relwidth=1, relheight=0.35)

#Text_Box Px
txt_edit_xA = Scale(FrIKR3,
                #command = servo1,
                from_=-90,
                to=90,
                resolution=0.5,
                orient = HORIZONTAL,
                length=180,
                troughcolor='gray',
                width = 20,
                cursor='dot',
                #label = 'Desplazamiento Base',
                )#tk.Text(FrIKR3, width=8, height=1)
txt_edit_xA.place(relx=1/10,rely=1/10-0.1)
#txt_edit_xA.insert(tk.END, "0")
        
#Text_Box Py
txt_edit_yA = Scale(FrIKR3,
                #command = servo1,
                from_=-90,
                to=90,
                resolution=0.5,
                orient = HORIZONTAL,
                length=180,
                troughcolor='gray',
                width = 20,
                cursor='dot',
                #label = 'Desplazamiento Base',
                )#tk.Text(FrIKR3, width=8, height=1)#tk.Text(FrIKR3, width = 8, height=1)
txt_edit_yA.place(relx=1/10, rely=3/10-0.1)
#txt_edit_yA.insert(tk.END, "0")

#Text_Box Pz
txt_edit_zA = Scale(FrIKR3,
                #command = servo1,
                from_=-90,
                to=90,
                resolution=0.5,
                orient = HORIZONTAL,
                length=180,
                troughcolor='gray',
                width = 20,
                cursor='dot',
                #label = 'Desplazamiento Base',
                )#tk.Text(FrIKR3, width=8, height=1)#tk.Text(FrIKR3, width = 8, height=1)
txt_edit_zA.place(relx=1/10, rely=5/10-0.1)
#txt_edit_zA.insert(tk.END, "0")

#Boton Calcular Cinematica Inversa Antropomórfico (R3)      
Calcular2=Button(FrIKR3, text='Calcular', activebackground='yellow',command=But_IK_R3)
Calcular2.place(relx=1/10-0.01, rely=7/10+0.01, relheight=1/6-0.05)

#Boton Envio Codo Abajo
EnvioC_AB_A=Button(FrIKR3, text='Enviar', activebackground='yellow', command=Envio_CD_A)
EnvioC_AB_A.place(relx=2.5/10+0.1, rely=0.85)

#Boton Envio Codo Arriba
EnvioC_AR_A=Button(FrIKR3, text='Enviar', activebackground='yellow', command=Envio_CU_A)#, command=Envio_CU_A
EnvioC_AR_A.place(relx=2.5/10+0.4, rely=0.85)

#Frame Variables de Juntura Codo Abajo (Contenedor)
FrR3CD=LabelFrame(FrIKR3,relief="raised",text='Codo Abajo',labelanchor='n')
FrR3CD.place(relx=0.3, rely=0.1, relwidth=0.25, relheight=0.7)

#Variable de Juntura 1
etiqueta1 = tk.Label(FrR3CD, width=5, text="θ₁", fg="black", bg="yellow").grid(column=0, row=0)
text1A = tk.Text(FrR3CD, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text1A.grid(row=0, column=1, sticky="nsew")

#Variable de Juntura 2
etiqueta2 = tk.Label(FrR3CD, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=2)
text2A = tk.Text(FrR3CD, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text2A.grid(row=2, column=1, sticky="nsew")

#Variable de Juntura 3
etiqueta3 = tk.Label(FrR3CD, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=4)
text3A = tk.Text(FrR3CD, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text3A.grid(row=4, column=1, sticky="nsew")

#Frame Variables De Juntura Codo Arriba (Contenedor)
FrR3CU=LabelFrame(FrIKR3,relief="raised",text='Codo Arriba',labelanchor='n')
FrR3CU.place(relx=0.6, rely=0.1, relwidth=0.25, relheight=0.7)

#Variable de Juntura 1
etiqueta1 = tk.Label(FrR3CU, width=5, text="θ₁", fg="black", bg="yellow").grid(column=0, row=0)
text1AAr = tk.Text(FrR3CU, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text1AAr.grid(row=0, column=1, sticky="nsew")

#Variable de Juntura 2
etiqueta2 = tk.Label(FrR3CU, width=5, text="θ₂", fg="black", bg="yellow").grid(column=0, row=2)
text2AAr = tk.Text(FrR3CU, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text2AAr.grid(row=2, column=1, sticky="nsew")

#Variable de Juntura 3
etiqueta3 = tk.Label(FrR3CU, width=5, text="θ₃", fg="black", bg="yellow").grid(column=0, row=4)
text3AAr = tk.Text(FrR3CU, padx= 20, pady=2, width=25, height=1, wrap="none", borderwidth=0)
text3AAr.grid(row=4, column=1, sticky="nsew")

#Filas Vacias Para Varibales De Juntura
Fnc.fila_vacia(1,1,FrR3CD,10)
Fnc.fila_vacia(3,1,FrR3CD,10)
Fnc.fila_vacia(1,1,FrR3CU,10)
Fnc.fila_vacia(3,1,FrR3CU,10)

#Filas y Columnas Vacias Para Matrices
Fnc.columna_vacia(5,1,FrMaR3,6)
Fnc.columna_vacia(9,1,FrMaR3,6)
Fnc.fila_vacia(5,4,FrMaR3,10)

#Titulos Antropomorfico (R3) (Label)
Titulos_l1 = Label(FrMaR3, width=11,text="Link 1")
Titulos_l1.place(relx=3/18-0.01,rely=0)
Titulos_l2 = Label(FrMaR3, width=11,text="Link 2")
Titulos_l2.place(relx=12/18-0.01,rely=0)
Titulos_l3 = Label(FrMaR3, width=11,text="Link 3")
Titulos_l3.place(relx=3/18-0.01,rely=7/14-0.03)
Titulos_lT = Label(FrMaR3, width=11,text="Total")
Titulos_lT.place(relx=12/18-0.01,rely=7/14-0.03)
Titulos_px = Label(FrIKR3, width=5,text="Px")
Titulos_px.place(relx=1/15,rely=1/10+0.01)
Titulos_py = Label(FrIKR3, width=5,text="Py")
Titulos_py.place(relx=1/15,rely=3/10+0.01)
Titulos_pz = Label(FrIKR3, width=5,text="Pz")
Titulos_pz.place(relx=1/15,rely=5/10+0.01)

#####Pestaña 4: Antropomórfico (R6)#####

#Ventanas DK-IK (Combobox)
combo = ttk.Combobox(p4,
        state="readonly",
        values=["DK", "IK"]
)
combo.bind("<<ComboboxSelected>>", selection_changed)
combo.place(x=10, y=10)

#Frame Cinematica Directa DK (Contenedor)
FrDKR6=LabelFrame(p4,text='DK', labelanchor='n')
FrDKR6.place(rely=0.63, relwidth=1, relheight=0.37)
FrDKR6.place_forget()

#Base1
#Slider
Rangulo1=Scale(FrDKR6,
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
txt_edit_ang7 = tk.Text(FrDKR6,width= 6)
txt_edit_ang7.place(relx=1/5, rely=1/21+0.015, relheight=1/10-0.05)
txt_edit_ang7.insert(tk.END, "0")
        
#Brazo1
#Slider
Rangulo2= Scale(FrDKR6,
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
txt_edit_ang8 = tk.Text(FrDKR6, width = 6)
txt_edit_ang8.place(relx=1/5, rely=4/21+0.015, relheight=1/10-0.05)
txt_edit_ang8.insert(tk.END, "0")

#Brazo2
#Slider
Rangulo3= Scale(FrDKR6,  
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
txt_edit_ang9 = tk.Text(FrDKR6, width = 6)
txt_edit_ang9.place(relx=1/5, rely=7/21+0.015, relheight=1/10-0.05)
txt_edit_ang9.insert(tk.END, "0")

#Base2
#Slider
Rangulo4= Scale(FrDKR6,  
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
txt_edit_ang10 = tk.Text(FrDKR6, width = 6)
txt_edit_ang10.place(relx=1/5, rely=10/21+0.015, relheight=1/10-0.05)
txt_edit_ang10.insert(tk.END, "0")

#Antebrazo
#Slider
Rangulo5= Scale(FrDKR6,  
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
txt_edit_ang11 = tk.Text(FrDKR6, width = 6)
txt_edit_ang11.place(relx=1/5, rely=13/21+0.015, relheight=1/10-0.05)
txt_edit_ang11.insert(tk.END, "0")

#Muñeca
#Slider
Rangulo6= Scale(FrDKR6,  
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
txt_edit_ang12 = tk.Text(FrDKR6, width = 6)
txt_edit_ang12.place(relx=1/5, rely=16/21+0.015, relheight=1/10-0.05)
txt_edit_ang12.insert(tk.END, "0")

#Frame Matrices (Contenedor)
FrMaR6=LabelFrame(FrDKR6,relief="raised")
FrMaR6.place(relx=1/4+0.01, relwidth=1, relheight=1)

Fnc.matrices(9,1,0,FrMaR6)   #Matriz Link 1
Fnc.matrices(10,1,8,FrMaR6)   #Matriz Link 2
Fnc.matrices(11,5,4,FrMaR6)   #Matriz Link 3
Fnc.matrices(12,9,0,FrMaR6)   #Matriz Link 4
Fnc.matrices(13,9,8,FrMaR6)   #Matriz Link 5
Fnc.matrices(14,13,4,FrMaR6)  #Matriz Link 6
Fnc.matrices(15,19,4,FrMaR6)  #Matriz Total

#Filas Vacias Para Matrices
Fnc.fila_vacia(0,1,FrMaR6,10)
Fnc.fila_vacia(16,2,FrMaR6,6) 

#Titulos Antropomórfico (R6) (Label)
Titulos_l1 = Label(FrMaR6, width=11,text="Link 1")
Titulos_l1.place(relx=2/24+0.01,rely=0)
Titulos_l2 = Label(FrMaR6, width=11,text="Link 2")
Titulos_l2.place(relx=14/24-0.005,rely=0)
Titulos_l3 = Label(FrMaR6, width=11,text="Link 3")
Titulos_l3.place(relx=5/15,rely=4/23)
Titulos_l4 = Label(FrMaR6, width=11,text="Link 4")
Titulos_l4.place(relx=2/24+0.01,rely=8/23)
Titulos_l5 = Label(FrMaR6, width=11,text="Link 5")
Titulos_l5.place(relx=14/24-0.005,rely=8/23)
Titulos_l6 = Label(FrMaR6, width=11,text="Link 6")
Titulos_l6.place(relx=5/15,rely=12/23-0.01)
Titulos_lT = Label(FrMaR6, width=11,text="Total")
Titulos_lT.place(relx=5/15,rely=17/23-0.01)

#Frame Cinemática Inversa Antropomórfico (R6)
FrIKR6=LabelFrame(p4,text='IK', labelanchor='n')
FrIKR6.place(rely=0.63, relwidth=1, relheight=0.37)
FrIKR6.place_forget()

#####Pestaña 5: Jacobianos#####
frmJACO=LabelFrame(p3, labelanchor='n')
frmJACO.place(relwidth=1, relheight=1)

Fnc.fila_vacia(0,2,frmJACO,10)
Fnc.matrices_J(2,4,frmJACO,2,1)   #Matriz Jacobiano Scara
Fnc.columna_vacia(9,1,frmJACO,10)
Fnc.matrices_J(3,3,frmJACO,2,10)  #Matriz Jacobiano Antropomórfico (R3)
Fnc.fila_vacia(9,1,frmJACO,10)
Fnc.matrices_J(1,6,frmJACO,10,6)  #Matriz Jacobiano Antropomórfico (R6)

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
nb.add(p5,text='Planeación de trayectorias')

root.mainloop()