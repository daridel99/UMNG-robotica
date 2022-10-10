from cProfile import label
from tkinter import *
import tkinter as tk

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

    for n in range(1,17):
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