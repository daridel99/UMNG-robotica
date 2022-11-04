from cProfile import label
from tkinter import *
import tkinter as tk
import Calculos as Cal
import numpy as np

def fila_vacia(donde,cuantas,frame,tamaño): #Crear Filas Vacias
    for n in range (0,cuantas):
        fila = Label(frame,width=tamaño)
        fila.grid(column=0, row=donde+n)

def columna_vacia(donde,cuantas,frame,tamano): #Crear Columnas Vacias
    for n in range (0,cuantas):
        blanco = Label(frame, width=tamano)
        blanco.grid(column=donde+n, row=0)

def creacion(): #Creacion De Variables En Masa
    globals()["txt_edit_yS_var"] = StringVar()

    for n in range(1,16):
        for i in range(0,4):
            for j in range(0,4):
                globals()["arr"+str(n)+"_" + str(i) + str(j)]=StringVar()

    for n in range(2,5):
         for i in range(0,6):
            for j in range(0,int(12/n)):
                globals()["jaco" + str(n-1) + "_" + str(i) + str(j)]=StringVar()

def matrices(m,f,k,frame): #Creación Matrices Cinemática Directa
    for r in range(0, 4):
        for c in range(0, 4):
            cell = tk.Label(frame, width=11,  textvariable=globals()["arr" + str(m) + "_" + str(r) + str(c)], bg='white')
            cell.grid(row=r+f, column=c+k,ipady=3)

def matrices_J(m,grados,frame,f,k): #Creación Matrices Jacobianos
    for r in range(0, 6):
        for c in range(0, grados):
            cell = Entry(frame, width=12,  textvariable=globals()["jaco" + str(m) +"_" + str(r) + str(c)], state= DISABLED)
            cell.grid(row=r+f, column=c+k, ipady=4)

def llenado (matri,M,K):  #Llenado Matrices
    for n in range(M,K):
        for i in range(0,4):
            for j in range(0,4):                
                globals()["arr"+ str(n) +"_" + str(i) + str(j)].set(matri[1][n-M][i][j])             
                globals()["arr"+ str(K) +"_"+ str(i) + str(j)].set(matri[0][i][j]) 

def llenado_JACO (JA,JS,JR): #Llenado Matrices JACO
    for n in range (3,5):
        s=n-1
        if (s==1):
            J=JR
        elif (s==2):
            J=JS
        elif (s==3):
            J=JA
        for i in range(0,2):
            i=i*3
            for j in range(0,int(12/n)):           
                for k in range(0,3):                
                    globals()["jaco" + str(n-1) +"_" + str(i+k) + str(j)].set(J[i-2][j][k]) 

def Perfil(tipo,mani,codo,tf,xi,yi,zi,xf,yf,zf,resol,var): #Determinar el tipo de Perfil A Utilizar
    if tipo==1:   #Perfil Cuadratico
        Qs=Manipulador(mani,codo,xi,yi,zi,xf,yf,zf)
        perfiles=Cal.Perf_Cuadra(tf,resol,Qs[0],Qs[1])
    elif tipo==2: #Perfil Trapezoidal Tipo I
        Qs=Manipulador(mani,codo,xi,yi,zi,xf,yf,zf)
        perfiles=Cal.Perf_Trape(tf,resol,Qs[0],Qs[1],var,1)
    else:         #Perfil Trapezoidal Tipo II
        Qs=Manipulador(mani,codo,xi,yi,zi,xf,yf,zf)
        perfiles=Cal.Perf_Trape(tf,resol,Qs[0],Qs[1],var,2)
    return perfiles       

def Manipulador(manipu,cod,Pxi,Pyi,Pzi,Pxf,Pyf,Pzf): #Determina el Manipulador a Utilizar
    if manipu==1:
        Inversai=Cal.IK_Scara_P3R(Pxi,Pyi,Pzi) #Cinematica Inversa para Punto Inicial
        Inversaf=Cal.IK_Scara_P3R(Pxf,Pyf,Pzf) #Cinematica Inversa para Punto Final
        Junturas=Solucion(cod,Inversai,Inversaf)
    else:
        Inversai=Cal.IK_Antropo_3R(Pxi,Pyi,Pzi) #Cinematica Inversa para Punto Inicial
        Inversaf=Cal.IK_Antropo_3R(Pxf,Pyf,Pzf) #Cinematica Inversa para Punto Final
        Junturas=Solucion(cod,Inversai,Inversaf)
    return Junturas

def Solucion(sol,Ini,Fin): #Determina la Solución a utilizar (Codo Arriba o Codo Abajo)
    if sol==1: #Codo Abajo
        Qi=[Ini[0],Ini[1],Ini[2]] #Toma los valores de las junturas iniciales para Codo Abajo 
        Qf=[Fin[0],Fin[1],Fin[2]] #Toma los valores de las junturas finales para Codo Abajo 
    else: #Codo Arriba
        Qi=[Ini[0],Ini[3],Ini[4]] #Toma los valores de las junturas iniciales para Codo Arriba
        Qf=[Fin[0],Fin[3],Fin[4]] #Toma los valores de las junturas finales para Codo Arriba
    return Qi,Qf

def Signo(x): #Determina El signo del numero
    sgn=np.array([0,0,0],float)
    for a in range(0,len(x)):
        if x(a)>=0:
            sgn[a]=1            
        else:
            sgn[a]=-1
    return sgn

def prueba():
    exec(open("sera.py").read())

#prueba()