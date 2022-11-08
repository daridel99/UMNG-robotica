import tkinter as tk
from tkinter import ttk
import Widgets as Wd


#Objetos Principales
Ventana = tk.Tk()
Ventana.title('Controles de Manipuladores Roboticos')
# width=Ventana.winfo_screenwidth()  
# height= Ventana.winfo_screenheight() 
# Ventana.geometry("%dx%d" % (width, height))
Panel_Pestañas = ttk.Notebook(Ventana)
Panel_Pestañas.pack(fill='both',expand='yes')

#Variables 
Nombres= tk.StringVar()
Nombres.set("""
Dario Delgado - 1802992 \n 
Brayan Ulloa - 1802861 \n 
Fernando Llanes - 1802878 \n
Karla Baron - 1803648 \n 
Sebastian Niño - 1803558
""")
Reposo= tk.StringVar()
Reposo.set("Parte de reposo \r termina en reposo: \r Ti=0; Vi=0; Vf=0")
Wd.Variables_Matrices(15, 4, 4, "DK")
Wd.Variables_Matrices(4, 6, 3, "Jaco")
Wd.Variables_Matrices(2, 6, 6, "JacoR6")

#Pestañas
Pestaña_Info=Wd.Pestañas(Panel_Pestañas, 'Portada')
Pestaña_Scara=Wd.Pestañas(Panel_Pestañas, 'Robot Scara (P2R)')
Pestaña_Antro3R=Wd.Pestañas(Panel_Pestañas, 'Robot Antropomórfico (3R)')
Pestaña_Antro6R=Wd.Pestañas(Panel_Pestañas, 'Robot Antropomórfico (6R)')
Pestaña_Trayectorias_Jacobiano=Wd.Pestañas(Panel_Pestañas, 'Trayectorias Por Jacobiano Inverso')
Pestaña_Jacobianos=Wd.Pestañas(Panel_Pestañas, 'Jacobiano')
Pestaña_Trayectorias=Wd.Pestañas(Panel_Pestañas, 'Planeación De Trayectorias')

#Fuentes
Fuente_12 = Wd.Fuentes("Lucida Grande", 12)
Fuente_15 = Wd.Fuentes("Lucida Grande", 15)
Fuente_25 = Wd.Fuentes("Lucida Grande", 25)
Fuente_Num = Wd.Fuentes("Palatino Linotype", 18)
Fuente_Num2 = Wd.Fuentes("Palatino Linotype", 12)
Fuente_Slider= Wd.Fuentes("Bookman Old Style", 12)

##################################Pestaña 1########################################
Fi=Wd.Frame(Pestaña_Info, 'Interfaz Grafica Para Controlar Manipuladores Roboticos', Fuente_12, 1, 1, 0, 0, None) #Frame
Portada = Wd.Labels(Fi, Nombres, None, None, None, None, Fuente_25, None).Ubicacion(1/2, 1/2, tk.CENTER)#Label-Nombres
Com=Wd.Boton(Fi, 20, 5, 'COM Close', None).Ubicacion(1/2, 7/8, tk.CENTER)

#Imagenes
Logo= Wd.Imagenes('./Imagenes/LOGOUMNG.png').zoom(2)                        #Logo UMNG
tk.Label(Fi, image=Logo).place(relx=1/4, rely=1/2, anchor=tk.CENTER)
Icono= Wd.Imagenes('./Imagenes/icon.png').zoom(2)                           #Icono Robot
tk.Label(Fi, image=Icono).place(relx=3/4, rely=1/2, anchor=tk.CENTER)

##################################Pestaña 2########################################
Fr_DK_S=Wd.Frame(Pestaña_Scara, 'Cinematica Directa', Fuente_12, 1, 5/8, 0, 0, None)   #Frame Cinematica Directa
Fr_IK_S=Wd.Frame(Pestaña_Scara, 'Cinematica Inversa', Fuente_12, 1, 3/8, 0, 5/8, None) #Frame Cinematica Inversa

######Cinematica Directa######

#Sliders
Wd.Slider(Fr_DK_S, 0, 221, 0.5, 250, 34, 'Desplazamiento Base', Fuente_Slider).Ubicacion(0, 0)
Wd.Slider(Fr_DK_S, -90, 90, 0.5, 250, 34, 'Rotación Brazo', Fuente_Slider).Ubicacion(0, 1/3)
Wd.Slider(Fr_DK_S, -90, 90, 0.5, 250, 34, 'Rotación Codo', Fuente_Slider).Ubicacion(0, 2/3)
Qt1_S=Wd.Editables(Fr_DK_S,Fuente_Num, 3/16, 0.11)
Qt2_S=Wd.Editables(Fr_DK_S,Fuente_Num, 3/16, 1/3+0.11)
Qt3_S=Wd.Editables(Fr_DK_S,Fuente_Num, 3/16, 2/3+0.11)

#Matrices
Wd.Matrices(Fr_DK_S, "DK", 1, 4, 4, "Link 1", 1/2, 0, Fuente_12)
Wd.Matrices(Fr_DK_S, "DK", 2, 4, 4, "Link 2", 5/6, 0, Fuente_12)
Wd.Matrices(Fr_DK_S, "DK", 3, 4, 4, "Link 3", 1/2, 1/2, Fuente_12)
Wd.Matrices(Fr_DK_S, "DK", 4, 4, 4, "Total", 5/6, 1/2, Fuente_12)

#Botones
Wd.Boton(Fr_DK_S, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)
Wd.Boton(Fr_DK_S, 15,3, "Griper", "lime green").Ubicacion(4/6, 0.9, tk.CENTER)
Wd.Boton(Fr_DK_S, 12,2, "Enviar", "ivory3").Ubicacion(1/4+0.02, 0.9, tk.W)

######Cinematica Inversa######
#Sliders
Px_S=Wd.Slider(Fr_IK_S, -101.5, 345, 0.5, 250, 20, 'Px', Fuente_Slider).Ubicacion(0, 0)
Py_S=Wd.Slider(Fr_IK_S, -90, 90, 0.5, 250, 20, 'Py', Fuente_Slider).Ubicacion(0, 1/3)
Wd.Check(Fr_IK_S, 3/16, 1/2+0.01)
Pz_S=Wd.Slider(Fr_IK_S, 0, 221, 0.5, 250, 20, 'Pz', Fuente_Slider).Ubicacion(0, 2/3)

#Codo Abajo
Co_D_S=Wd.Frame(Fr_IK_S, "Codo Abajo", Fuente_12, 1/10, 1/2, 1/2, 0, tk.N)
q1_S_D=tk.StringVar()
q2_S_D=tk.StringVar()
q3_S_D=tk.StringVar()
Wd.Labels(Co_D_S, None, "d₁", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 0, tk.NW)      
Wd.Labels(Co_D_S, q1_S_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 0, tk.NE)     
Wd.Labels(Co_D_S, None, "θ₂", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 1/3, tk.NW)  
Wd.Labels(Co_D_S, q2_S_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 1/3, tk.NE)   
Wd.Labels(Co_D_S, None, "θ₃", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 2/3, tk.NW)  
Wd.Labels(Co_D_S, q3_S_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 2/3, tk.NE) 

#Codo Arriba
Co_U_S=Wd.Frame(Fr_IK_S, "Codo Arriba", Fuente_12, 1/10, 1/2, 2/3, 0, tk.N)
q1_S_U=tk.StringVar()
q2_S_U=tk.StringVar()
q3_S_U=tk.StringVar()
Wd.Labels(Co_U_S, None, "d₁", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 0, tk.NW)      
Wd.Labels(Co_U_S, q1_S_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 0, tk.NE)     
Wd.Labels(Co_U_S, None, "θ₂", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 1/3, tk.NW)  
Wd.Labels(Co_U_S, q2_S_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 1/3, tk.NE)   
Wd.Labels(Co_U_S, None, "θ₃", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 2/3, tk.NW)  
Wd.Labels(Co_U_S, q3_S_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 2/3, tk.NE)  

#Botones
Wd.Boton(Fr_IK_S, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)
Wd.Boton(Fr_IK_S, 12,2, "Codo Abajo", "ivory3").Ubicacion(1/2,1/2,tk.N)
Wd.Boton(Fr_IK_S, 12,2, "Codo Arriba", "ivory3").Ubicacion(2/3, 1/2, tk.N)
Wd.Boton(Fr_IK_S, 12,8, "Calcular", "dim gray").Ubicacion(1/4+0.02, 1/2, tk.W)

#Barra De Progreso
Wd.Barra(Fr_IK_S, 300, 1/6, 0.98, 0.25, tk.E)

##################################Pestaña 3########################################
Fr_DK_R3=Wd.Frame(Pestaña_Antro3R, 'Cinematica Directa', Fuente_12, 1,5/8, 0, 0, None)   #Frame Cinematica Directa
Fr_IK_R3=Wd.Frame(Pestaña_Antro3R, 'Cinematica Inversa', Fuente_12, 1,3/8, 0, 5/8, None) #Frame Cinematica Inversa

######Cinematica Directa######

#Sliders
Wd.Slider(Fr_DK_R3, -90, 90, 0.5, 250, 34, 'Rotación Base', Fuente_Slider).Ubicacion(0, 0)
Wd.Slider(Fr_DK_R3, -90, 90, 0.5, 250, 34, 'Rotación Brazo', Fuente_Slider).Ubicacion(0, 1/3)
Wd.Slider(Fr_DK_R3, -90, 90, 0.5, 250, 34, 'Rotación Codo', Fuente_Slider).Ubicacion(0, 2/3)
Qt1_R3=Wd.Editables(Fr_DK_R3,Fuente_Num, 3/16, 0.11)
Qt2_R3=Wd.Editables(Fr_DK_R3,Fuente_Num, 3/16, 1/3+0.11)
Qt3_R3=Wd.Editables(Fr_DK_R3,Fuente_Num, 3/16, 2/3+0.11)

#Matrices
Wd.Matrices(Fr_DK_R3, "DK", 5, 4, 4, "Link 1", 1/2, 0, Fuente_12)
Wd.Matrices(Fr_DK_R3, "DK", 6, 4, 4, "Link 2", 5/6, 0, Fuente_12)
Wd.Matrices(Fr_DK_R3, "DK", 7, 4, 4, "Link 3", 1/2, 1/2, Fuente_12)
Wd.Matrices(Fr_DK_R3, "DK", 8, 4, 4, "Total", 5/6, 1/2, Fuente_12)

#Botones
Wd.Boton(Fr_DK_R3, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)
Wd.Boton(Fr_DK_R3, 15, 3, "Griper", "lime green").Ubicacion(4/6, 0.9, tk.CENTER)
Wd.Boton(Fr_DK_R3, 12, 2, "Enviar", "ivory3").Ubicacion(1/4+0.02, 0.9, tk.W)

######Cinematica Inversa######
#Sliders
Px_R3=Wd.Slider(Fr_IK_R3, -90, 90, 0.5, 250, 20, 'Px', Fuente_Slider).Ubicacion(0, 0)
Py_R3=Wd.Slider(Fr_IK_R3, -90, 90, 0.5, 250, 20, 'Py', Fuente_Slider).Ubicacion(0, 1/3)
Pz_R3=Wd.Slider(Fr_IK_R3, -90, 90, 0.5, 250, 20, 'Pz', Fuente_Slider).Ubicacion(0, 2/3)

#Codo Abajo
Co_D_R3=Wd.Frame(Fr_IK_R3, "Codo Abajo", Fuente_12, 1/10, 1/2, 1/2, 0, tk.N)
q1_R3_D=tk.StringVar()
q2_R3_D=tk.StringVar()
q3_R3_D=tk.StringVar()
Wd.Labels(Co_D_R3, None, "d₁", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 0, tk.NW)      
Wd.Labels(Co_D_R3, q1_R3_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 0, tk.NE)     
Wd.Labels(Co_D_R3, None, "θ₂", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 1/3, tk.NW)  
Wd.Labels(Co_D_R3, q2_R3_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 1/3, tk.NE)   
Wd.Labels(Co_D_R3, None, "θ₃", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 2/3, tk.NW)  
Wd.Labels(Co_D_R3, q3_R3_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 2/3, tk.NE) 

#Codo Arriba
Co_U_R3=Wd.Frame(Fr_IK_R3, "Codo Arriba", Fuente_12, 1/10, 1/2, 2/3, 0, tk.N)
q1_R3_U=tk.StringVar()
q2_R3_U=tk.StringVar()
q3_R3_U=tk.StringVar()
Wd.Labels(Co_U_R3, None, "d₁", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 0, tk.NW)      
Wd.Labels(Co_U_R3, q1_R3_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 0, tk.NE)     
Wd.Labels(Co_U_R3, None, "θ₂", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 1/3, tk.NW)  
Wd.Labels(Co_U_R3, q2_R3_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 1/3, tk.NE)   
Wd.Labels(Co_U_R3, None, "θ₃", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 2/3, tk.NW)  
Wd.Labels(Co_U_R3, q3_R3_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 2/3, tk.NE)  

#Botones
Wd.Boton(Fr_IK_R3, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)
Wd.Boton(Fr_IK_R3, 12, 2, "Codo Abajo", "ivory3").Ubicacion(1/2, 1/2, tk.N)
Wd.Boton(Fr_IK_R3, 12, 2, "Codo Arriba", "ivory3").Ubicacion(2/3, 1/2, tk.N)
Wd.Boton(Fr_IK_R3, 12, 8, "Calcular", "dim gray").Ubicacion(1/4+0.02, 1/2, tk.W)

#Barra De Progreso
Wd.Barra(Fr_IK_R3, 300, 1/6, 0.98, 0.25, tk.E)

##################################Pestaña 4########################################

#Desplegable
Despl_R6=Wd.Desplegable(Pestaña_Antro6R, ["Cinematica Directa", "Cinematica Inversa"],  0, 0)
Despl_R6.bind("<<ComboboxSelected>>",Despl_R6.Cambio)
Fr_DK_R6=Despl_R6.Frame_DK
Fr_IK_R6=Despl_R6.Frame_IK
#####Cinematica Directa######

#Sliders
Wd.Slider(Fr_DK_R6,0, 360, 0.5, 250, 34, 'Rotación Primera Base', Fuente_Slider).Ubicacion(0, 0)
Wd.Slider(Fr_DK_R6,0, 360, 0.5, 250, 34, 'Rotación Primer Brazo', Fuente_Slider).Ubicacion(0, 1/6)
Wd.Slider(Fr_DK_R6,0, 360, 0.5, 250, 34, 'Rotación Segundo Brazo', Fuente_Slider).Ubicacion(0, 2/6)
Wd.Slider(Fr_DK_R6,0, 360, 0.5, 250, 34, 'Rotación Segunda Base', Fuente_Slider).Ubicacion(0, 3/6)
Wd.Slider(Fr_DK_R6,0, 360, 0.5, 250, 34, 'Rotación Antebrazo', Fuente_Slider).Ubicacion(0, 4/6)
Wd.Slider(Fr_DK_R6,0, 360, 0.5, 250, 34, 'Rotación Muñeca', Fuente_Slider).Ubicacion(0, 5/6)
Qt1_R6=Wd.Editables(Fr_DK_R6, Fuente_Num, 3/16, 1/18+0.014)
Qt2_R6=Wd.Editables(Fr_DK_R6, Fuente_Num, 3/16, 4/18+0.014)
Qt3_R6=Wd.Editables(Fr_DK_R6, Fuente_Num, 3/16, 7/18+0.014)
Qt1_R6=Wd.Editables(Fr_DK_R6, Fuente_Num, 3/16, 10/18+0.014)
Qt2_R6=Wd.Editables(Fr_DK_R6, Fuente_Num, 3/16, 13/18+0.014)
Qt3_R6=Wd.Editables(Fr_DK_R6, Fuente_Num, 3/16, 16/18+0.014)

#Matrices
Wd.Matrices(Fr_DK_R6, "DK", 9, 4, 4, "Link 1", 1/2, 0, Fuente_12)
Wd.Matrices(Fr_DK_R6, "DK", 10, 4, 4, "Link 2", 5/6, 0, Fuente_12)
Wd.Matrices(Fr_DK_R6, "DK", 11, 4, 4, "Link 3", 1/2, 1/4, Fuente_12)
Wd.Matrices(Fr_DK_R6, "DK", 12, 4, 4, "Link 4", 5/6, 1/4, Fuente_12)
Wd.Matrices(Fr_DK_R6, "DK", 13, 4, 4, "Link 5", 1/2, 2/4, Fuente_12)
Wd.Matrices(Fr_DK_R6, "DK", 14, 4, 4, "Link 6", 5/6, 2/4, Fuente_12)
Wd.Matrices(Fr_DK_R6, "DK", 15, 4, 4, "Total", 2/3, 3/4, Fuente_12)

#Botones
Wd.Boton(Fr_DK_R6, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)
Wd.Boton(Fr_DK_R6, 15,3, "Griper", "lime green").Ubicacion(7/16, 3/4+0.1, tk.N)
Wd.Boton(Fr_DK_R6, 12,2, "Enviar", "ivory3").Ubicacion(7/16, 3/4, tk.N)

#Barra De Progreso
Wd.Barra(Fr_DK_R6, 200, 1/15, 0.98, 3/4, tk.NE)

######Cinematica Inversa######

#Sliders
Wd.Slider(Fr_IK_R6,-200, 200, 0.5, 250, 34, 'Px', Fuente_Slider).Ubicacion(0, 0)
Wd.Slider(Fr_IK_R6,-200, 200, 0.5, 250, 34, 'Py', Fuente_Slider).Ubicacion(0, 1/6)
Wd.Slider(Fr_IK_R6,-200, 200, 0.5, 250, 34, 'Pz', Fuente_Slider).Ubicacion(0, 2/6)
Wd.Slider(Fr_IK_R6,-200, 200, 0.5, 250, 34, 'Alfa', Fuente_Slider).Ubicacion(0, 3/6)
Wd.Slider(Fr_IK_R6,-200, 200, 0.5, 250, 34, 'Beta', Fuente_Slider).Ubicacion(0, 4/6)
Wd.Slider(Fr_IK_R6,-200, 200, 0.5, 250, 34, 'Gamma', Fuente_Slider).Ubicacion(0, 5/6)

#Botones
Wd.Boton(Fr_IK_R6, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)

##################################Pestaña 5########################################

Fr_T_J=Wd.Frame(Pestaña_Trayectorias_Jacobiano, 'Planificación de Trayectorias Por Jacobiano Inverso', Fuente_12, 1, 1, 0, 0, None)   #Frame Jacobiano

##################################Pestaña 6########################################

Fr_J=Wd.Frame(Pestaña_Jacobianos, 'Jacobianos', Fuente_12, 1, 1, 0, 0, None)   #Frame Jacobiano

#Matrices
Wd.Matrices(Fr_J, "Jaco", 1, 6, 3, "Jacobiano Scara Geométrico", 1/4, 0, Fuente_12)
Wd.Matrices(Fr_J, "Jaco", 2, 6, 3, "Jacobiano Scara Analítico", 3/4, 0, Fuente_12)
Wd.Matrices(Fr_J, "Jaco", 3, 6, 3, "Jacobiano Antropomórfico Geométrico", 1/4, 1/3, Fuente_12)
Wd.Matrices(Fr_J, "Jaco", 4, 6, 3, "Jacobiano Antropomórfico Analítico", 3/4, 1/3, Fuente_12)
Wd.Matrices(Fr_J, "JacoR6", 1, 6, 6, "Jacobiano Antropomórfico 6R Geométrico", 1/4, 2/3, Fuente_12)
Wd.Matrices(Fr_J, "JacoR6", 2, 6, 6, "Jacobiano Antropomórfico 6R Analítico", 3/4, 2/3, Fuente_12)

#Botones
Wd.Boton(Fr_J, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)
Wd.Boton(Fr_J, 15,3, "Mostrar", "dim gray").Ubicacion(1/2, 1/2, tk.N)

#Barra De Progreso
Wd.Barra(Fr_J, 300, 1/15, 1/2, 1/3, tk.N)

##################################Pestaña 7########################################

Fr_T=Wd.Frame(Pestaña_Trayectorias, 'Datos de Entrada', Fuente_12, 1, 1/4, 0, 0, None)   #Frame Jacobiano

#Desplegables
Despl_Mani=Wd.Desplegable(Fr_T, ["Scara (PRR)", "Antropomórfico (RRR)"],  0, 0)
Despl_Codo=Wd.Desplegable(Fr_T, ["Codo Arriba", "Codo Abajo"],  4/16+0.01, 4/6)

#Label Información Importante (Parte de Reposo)
Wd.Labels(Fr_T, Reposo, None, 1, "solid", None, Fuente_15, None).Ubicacion(4/16, 0, None)

#Puntos Iniciales-Finales
#Labels
P_xi=Wd.Labels(Fr_T, None, "0", 1, "solid", 12, None, None).Ubicacion(0, 2/6-0.02, None)
P_yi=Wd.Labels(Fr_T, None, "0", 1, "solid", 12, None, None).Ubicacion(0, 3/6+0.075, None)
P_zi=Wd.Labels(Fr_T, None, "0", 1, "solid", 12, None, None).Ubicacion(0, 0.836, None)
P_x= Wd.Labels(Fr_T, None, "Px", None, None, None, None, None).Ubicacion(1/16+0.01, 2/6-0.02, None)
P_y= Wd.Labels(Fr_T, None, "Py", None, None, None, None, None).Ubicacion(1/16+0.01, 3/6+0.075, None)
P_z= Wd.Labels(Fr_T, None, "Pz", None, None, None, None, None).Ubicacion(1/16+0.01, 0.836, None)

#Radio Buttons
Tipo=tk.IntVar()
Cuadratico=Wd.Radio(Fr_T, "Perfil Cuadratico", Fuente_12, 1, Tipo, 15).Ubicacion(6/16+0.04, 0)
TrapezoidalI=Wd.Radio(Fr_T, "Perfil Trapezoidal I", Fuente_12, 2, Tipo, 15).Ubicacion(9/16+0.04, 0)
TrapezoidalII=Wd.Radio(Fr_T, "Perfil Trapezoidal II", Fuente_12, 3, Tipo, 15).Ubicacion(12/16+0.04, 0)

#Sliders
Pl_x=Wd.Slider(Fr_T, None, None, 0.5, 180, 20, None, None).Ubicacion(1/16+0.025, 1/6)
Pl_y=Wd.Slider(Fr_T, None, None, 0.5, 180, 20, None, None).Ubicacion(1/16+0.025, 3/6-0.07)
Wd.Check(Fr_T, 4/16-0.027, 3/6+0.05)
Pl_z=Wd.Slider(Fr_T, None, None, 0.5, 180, 20, None, None).Ubicacion(1/16+0.025, 0.693)
T_f=Wd.Slider(Fr_T, 15, 40, 1, 180, 20, None, None).Ubicacion(6/16+0.04, 1/8+0.01)
N_p=Wd.Slider(Fr_T, 10, 1000, 10, 180, 20, None, None).Ubicacion(6/16+0.04, 3/8+0.04)
Vj_1=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None).Ubicacion(9/16+0.04, 1/8+0.01)
Vj_2=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None).Ubicacion(9/16+0.04, 3/8+0.04)
Vj_3=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None).Ubicacion(9/16+0.04, 5/8+0.08)
Aj_1=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None).Ubicacion(12/16+0.04, 1/8+0.01)
Aj_2=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None).Ubicacion(12/16+0.04, 3/8+0.04)
Aj_3=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None).Ubicacion(12/16+0.04, 5/8+0.08)

#Titulos
P_inicial=Wd.Labels(Fr_T, None, "Puntos Iniciales", None, None, 12, Fuente_Num2, None).Ubicacion(0, 1/6-0.02, None)
P_final=Wd.Labels(Fr_T, None, "Puntos Finales", None, None, 12, Fuente_Num2, None).Ubicacion(2/16 , 0, None)
T_Codo=Wd.Labels(Fr_T, None, "Elección Codo", None, None, 12, Fuente_Num2, None).Ubicacion(5/16 , 4/7, tk.CENTER)
TT_f=Wd.Labels(Fr_T, None, "Tf", None, None, None, Fuente_Num2, None).Ubicacion(6/16+0.02, 1/7+0.12, None)
TN_p=Wd.Labels(Fr_T, None, "Np", None, None, None, Fuente_Num2, None).Ubicacion(6/16+0.02, 3/7+0.12, None)
TVc_1=Wd.Labels(Fr_T, None, "Vc1", None, None, None, Fuente_Num2, None).Ubicacion(9/16+0.02, 1/7+0.12, None)
TVc_2=Wd.Labels(Fr_T, None, "Vc2", None, None, None, Fuente_Num2, None).Ubicacion(9/16+0.02, 3/7+0.12, None)
TVc_3=Wd.Labels(Fr_T, None, "Vc3", None, None, None, Fuente_Num2, None).Ubicacion(9/16+0.02, 5/7+0.12, None)
TAc_1=Wd.Labels(Fr_T, None, "Ac1", None, None, None, Fuente_Num2, None).Ubicacion(12/16+0.02, 1/7+0.12, None)
TAc_2=Wd.Labels(Fr_T, None, "Ac2", None, None, None, Fuente_Num2, None).Ubicacion(12/16+0.02, 3/7+0.12, None)
TAc_3=Wd.Labels(Fr_T, None, "Ac3", None, None, None, Fuente_Num2, None).Ubicacion(12/16+0.02, 5/7+0.12, None)

Ventana.attributes('-fullscreen',True)
Ventana.mainloop()
