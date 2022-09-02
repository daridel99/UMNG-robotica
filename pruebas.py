import math as mt
from operator import length_hint
from tkinter import HORIZONTAL, PhotoImage, StringVar, Widget
from ctypes import sizeof
import tkinter  as tk
from tkinter import *
from turtle import color
import numpy as np
from time import sleep
from tkinter import messagebox
from PIL import Image, ImageTk
import serial, serial.tools.list_ports
from tkinter import ttk

class Objetos:
    def __init__(self,ventana):
        self.vent=ventana
        self.vent.title('Controles de Manipuladores Roboticos')
        self.vent.geometry("1366x768")
                
        # self.run=True
        # self.receive=False

        #Frame Informacion (Contenedor)
        fi=LabelFrame(self.vent, text='Interfaz Grafica Para Controlar Manipuladores Roboticos', labelanchor='n')
        fi.place(relwidth=1, relheight=0.15)

        #Logo
        img= PhotoImage(file="LOGOUMNG.png")
        widget = Label(fi, image=img)
        widget.place(relwidth=1,relheight=0.5)

        img1= PhotoImage(file="icon.png")
        widget1 = Label(fi, image=img1)
        widget1.place(relwidth=1.5,relheight=1)

        # globals()["color_boton1"]=StringVar()
        # color_boton1='green'

        #Label Nombres
        var= StringVar()
        etiqueta = Label(fi, textvariable=var , relief=FLAT , pady=5)
        var.set("Dario Delgado - 1802992 \n Brayan Ulloa - 1802861 \n Santiago Tobar - 1803015 \n Fernando Llanes - 1802878 \n Karla Baron - 1803648 \n Sebastian Niño - 1803558")
        etiqueta.place(relwidth=1,relheight=1)

        #Frame Manipuladores (Contenedor)
        frm=LabelFrame(self.vent,relief="raised")
        frm.place(rely=0.15, relwidth=1, relheight=0.85)

        #Frame Manipulador1 Scara (Contenedor)
        frm1=LabelFrame(frm,text='Robot Scara', labelanchor='n')
        frm1.place(relwidth=1, relheight=0.55)

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
        frm2=LabelFrame(frm,text='Robot Antropomorfico (RRR)', labelanchor='n')
        frm2.place(rely=0.55, relwidth=1, relheight=0.45)

        #Brazo
        #Slider
        Aangulo1=Scale(frm2,
                from_=0,
                to=122,
                orient = HORIZONTAL,
                length=300,
                troughcolor='gray',
                width = 30,
                cursor='dot',
                label = 'Rotación Brazo',
                  )
        Aangulo1.place(rely=0,relwidth=1/5, relheight=1/3)
        #Text_Box
        txt_edit_ang4 = tk.Text(frm2,width=3)
        txt_edit_ang4.place(relx=1/5, rely=0.16, relheight=1/6-0.05)
        txt_edit_ang4.insert(tk.END, "0")
        
        #Antebrazo
        #Slider
        Aangulo2= Scale(frm2,
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Codo'  )
        Aangulo2.place(rely=(1/4+0.083), relwidth=1/5, relheight=1/3)
        #Text_Box
        txt_edit_ang5 = tk.Text(frm2, width = 3)
        txt_edit_ang5.place(relx=1/5, rely=2/6+0.16, relheight=1/6-0.05)
        txt_edit_ang5.insert(tk.END, "0")

        #Muñeca
        #Slider
        Aangulo3= Scale(frm2,              
              from_=0,
              to=180,
              orient = HORIZONTAL,
              length=300,
              troughcolor='gray',
              width = 30,
              cursor='dot',
              label = 'Rotación Muñeca')
        Aangulo3.place(rely=(3/4-0.083), relwidth=1/5, relheight=1/3)
        #Text_Box
        txt_edit_ang6 = tk.Text(frm2, width = 3, height=1.8)
        txt_edit_ang6.place(relx=1/5, rely=4/6+0.16, relheight=1/6-0.05)
        txt_edit_ang6.insert(tk.END, "0")
        

        def blanco(n):
            blanco = Label(frmdh1, width=6)
            blanco.grid(column=4+n, row=0)
            


        #Frame Matrices Manipulador 1 Scara (Contenedor)
        frmdh1=LabelFrame(frm1,relief="raised")
        frmdh1.place(relx=1/5+0.028, relwidth=1, relheight=1)


        Titulos = Label(frmdh1, width=10,text="Link 1")
        Titulos.grid(column=2, row=0)

        espacio = Label(frmdh1, width=10)
        espacio.grid(column=0, row=0)

        for r in range(2, 6):
            for c in range(2, 6):
                cell = Entry(frmdh1, width=12)
                cell.grid(row=r, column=c, ipady=4)

        blanco(0)

        for r in range(0, 4):
            for c in range(5, 9):
                cell = Entry(frmdh1, width=12)
                cell.grid(row=r, column=c, ipady=4)
        blanco(5)

        for r in range(0, 4):
            for c in range(11, 15):
                cell = Entry(frmdh1, width=12)
                cell.grid(row=r, column=c, ipady=4)
        
        blanco = Label(frmdh1, width=10)
        blanco.grid(column=1, row=6)

        Titulos = Label(frmdh1, width=10,text="Link 4")
        Titulos.grid(column=1, row=7)

        for r in range(8, 11):
            for c in range(0, 4):
                cell = Entry(frmdh1, width=12)
                cell.grid(row=r, column=c, ipady=4)
        


        # #Botones
        # ttk.Button(fr1,text='Volumen').place(relwidth=1/3, relheight=1/3)
        # ttk.Button(fr1,text='Temperatura').place(relx=1/3,relwidth=1/3, relheight=1/3)
        # ttk.Button(fr1,text='Distancia').place(relx=2/3, relwidth=1/3, relheight=1/3)
        # ttk.Button(fr1,text='Todos').place(rely=1/3,relwidth=0.5, relheight=1/3)
        # ttk.Button(fr1,text='Ninguno').place(relx=0.5, rely=1/3, relwidth=0.5, relheight=1/3)
        # self.conectar=ttk.Button(fr1,text='Conectar')
        # self.conectar.place(rely=2/3, relwidth=1/2, relheight=1/3)
        # self.desconectar=ttk.Button(fr1,text='Desconectar')
        # self.desconectar.place(rely=2/3, relx=1/2, relwidth=1/2, relheight=1/3)
        
        # #Frame De Leds (Contenedor)
        # fr2=LabelFrame(self.vent, text='Leds', labelanchor='n')
        # fr2.place(relx=0.6, rely=0.4, relwidth=0.2, relheight=0.3)

        # #Leds
        # self.check1=IntVar()
        # self.check2=IntVar()
        # self.check3=IntVar()
        
        # Checkbutton(fr2,text='Led Verde',selectcolor='green',variable=self.check1).place(relwidth=1, relheight=1/3)
        # Checkbutton(fr2,text='Led Amarillo',selectcolor='yellow',variable=self.check2).place(rely=1/3,relwidth=1, relheight=1/3)
        # Checkbutton(fr2,text='Led Rojo',selectcolor='red',variable=self.check3).place(rely=2/3,relwidth=1, relheight=1/3)

if __name__== '__main__':
    ventana=Tk()
    aplicacion=Objetos(ventana)
    ventana.mainloop()