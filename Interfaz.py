###### Librerias ######
import tkinter as tk
import Widgets as Wd
import Ecuaciones as Ec
import time as tm
import threading as hilos
###### Modulos De Librerias ######
import tkinter.ttk as ttk
import tkinter.messagebox as MsB
import serial
import serial.tools.list_ports

board =serial.Serial(port='COM1', baudrate=9600)
tm.sleep(1)

def Show_Sliders(event): #Función Para Mostrar Sliders
    Alter_Sliders('T', Pl_x.get())
    Wd.Aparecer([Pl_x,Pl_y,Pl_z,P_xi,P_yi,P_zi,P_x,P_y,P_z,P_inicial,P_final],
    [1/16+0.025, 1/16+0.025, 1/16+0.025, 0, 0, 0, 1/16+0.01, 1/16+0.01, 1/16+0.01, 0, 2/16],
    [1/6, 3/6-0.07, 0.693, 2/6-0.02, 3/6+0.075, 0.836, 2/6-0.02, 3/6+0.075, 0.836, 1/6-0.02, 0])

def Show_Codo(Iden, Valor): #Función Para Mostrar Codos
    Wd.Aparecer([T_Codo,Despl_Codo],[4/16+0.02, 4/16+0.01],[3/7+0.02, 4/6])    

def Show_Perfiles(event): #Función Para Mostrar Perfiles
    Wd.Aparecer([Cuadratico,TrapezoidalI,TrapezoidalII],[6/16+0.04, 9/16+0.04, 12/16+0.04],[0, 0, 0])  

def Show_Datos(): #Función Para Mostrar Los Sliders De Datos De Entrada
    if Tipo.get()==1:
        Wd.Ocultar([Vj_1, Vj_2, Vj_3, Aj_1, Aj_2, Aj_3, TAc_1, TAc_2, TAc_3, TVc_1, TVc_2, TVc_3])

    if Tipo.get()==2:
        Wd.Aparecer([Vj_1, Vj_2, Vj_3, TVc_1, TVc_2, TVc_3],
        [9/16+0.04, 9/16+0.04, 9/16+0.04, 9/16+0.02, 9/16+0.02, 9/16+0.02],
        [1/8+0.01, 3/8+0.04, 5/8+0.08, 1/7+0.12, 3/7+0.12, 5/7+0.12])  
        Wd.Ocultar([Aj_1, Aj_2, Aj_3, TAc_1, TAc_2, TAc_3])
        #Calculos.Perf_Trape(T_f.get(),N_p.get(),0,0,0,1)
    
    if Tipo.get()==3:
        Wd.Aparecer([Aj_1, Aj_2, Aj_3, TAc_1, TAc_2, TAc_3],
        [12/16+0.04, 12/16+0.04, 12/16+0.04, 12/16+0.02, 12/16+0.02, 12/16+0.02],
        [1/8+0.01, 3/8+0.04, 5/8+0.08, 1/7+0.12, 3/7+0.12, 5/7+0.12])  
        Wd.Ocultar([Vj_1, Vj_2, Vj_3, TVc_1, TVc_2, TVc_3])
        #Calculos.Perf_Trape(T_f.get(),N_p.get(),0,0,0,2)

    Wd.Aparecer([T_f, N_p, TT_f, TN_p, Calcular_PT],
    [6/16+0.04, 6/16+0.04, 6/16+0.02, 6/16+0.02, 6/16+0.04],
    [1/8+0.01, 3/8+0.04, 1/7+0.012, 3/7+0.012, 6/8])
    
bands=0
bandr=0
def Datos_Temp(xtemp, ytemp, ztemp, RW): #Función Para Guardar Los Valores Para Nuevo Punto Inicial
    global bands
    global bandr
   
    if RW==0:
        selection = Despl_Mani.get()
        if selection == "Scara (PRR)":
            temp_xs=xtemp 
            temp_ys=ytemp
            temp_zs=ztemp 
            bands=1
        else:
            temp_xr=xtemp 
            temp_yr=ytemp
            temp_zr=ztemp
            bandr=1
    else:
        selection = Despl_Mani.get()               
        if selection == "Scara (PRR)":
            if bands==1:
                P_xi.config(text=temp_xs)
                P_yi.config(text=temp_ys)
                P_zi.config(text=temp_zs)                
            else:
                P_xi.config(text=345.2) 
                P_yi.config(text=0)
                P_zi.config(text=0)
        else:   
            if bandr==1:
                P_xi.config(text=temp_xr)
                P_yi.config(text=temp_yr)
                P_zi.config(text=temp_zr)                
            else:   
                P_xi.config(text=170.28) 
                P_yi.config(text=0)
                P_zi.config(text=62.87)    

def Alter_Sliders(Ident, Valor): #Función Para Alternos Los Sliders (Scara-Antropomórfico)
    Datos_Temp(0,0,0,1) 
    if Despl_Mani.get() == "Scara (PRR)":
        Pl_x['from_']=-131.5
        Pl_x['to']=375.5
        Pl_z['from_']=0
        Pl_z['to']=221
        if Ident == 'A1':        
            Red_Slider(['S', 'T', Pl_y, Check_S_PL, 1/4-0.025, 1/3+0.22], Valor)           
    else:
        Pl_x['from_']=-197
        Pl_x['to']=197  
        if Ident == 'A1':
            Red_Slider(['A1', 'T', Pl_y, Check_A_PL, 1/4-0.025, 2/3+0.15], Valor) 
        elif Ident == 'A2':
            Red_Slider(['A2', 'T', Pl_z, Check_A_PL, 1/4-0.025, 2/3+0.15], Valor) 

def Mensajes(Cual): #Función Para Seleccionar Mensaje Emergente A Mostrar
    if Cual=="DK":
        MsB.showinfo(
            "Instrucciones Cinemática Directa",
        """
            Sliders: Desplazar los slider para mover las 
            articulaciones del brazo robótico en tiempo real 
            para obtener las matrices individuales y total de 
            la cinemática directa. \n
            
            Cuadro de Texto: Digitar el valor que se encuentre
            en el rango de funcionamiento del robot para mover 
            las articulaciones del brazo robótico. 
            Luego presionar el botón de envió y obtener las
            matrices individuales y total de la cinemática directa 
            en tiempo real.
        """)
    elif Cual=="IK":        
        MsB.showinfo(
            "Instrucciones Cinemática Inversa",
        """
            Deslizar cada slider para establecer la posición 
            del efector final, dar click en el botón "Calcular"
            y finalizar seleccionando la configuración del codo 
            a utilizar para mover el manipulador. \n
            
            Se debe tener en cuenta que las opciones de los codos
            únicamente están disponibles sí los valores calculados 
            de las articulaciones no superan los límites mecánicos
        """)

def Color(Bandera, Boton, Identi): #Función Para Alternan Color De Boton
    #print-->board.write
    if Bandera:
        Boton["bg"]="red4"
        print(Identi + '1')
    else:
        Boton["bg"]="lime green"
        board.write(Identi + '0')

def Gripper(Identi): #Función Para Abrir o Cerrar Grippers
        global Estado_S        
        global Estado_A
        global Estado_R
        if Identi=='E':            
            Estado_S=not Estado_S
            Color(Estado_S,Gp_S,'E')
        elif Identi=='A':
            Estado_A=not Estado_A
            Color(Estado_A,Gp_A,'A')
        else:
            Estado_R=not Estado_R
            Color(Estado_R,Gp_R,'R')

def Red_Slider(Vec, Valor): #Función Para Redefinir Los Limites de Los Sliders De Cinematica Inversa
    Ident=Vec[0]        
    if (Ident == 'S') or (Ident == 'A2') or (Ident =='A1'): 
        Pes=Vec[1]
        Slider=Vec[2]
        Check=Vec[3]
        PosX=Vec[4]
        PosY=Vec[5]
    if Ident =='S':                                   #Redefinir Slider "Py_S" De Scara
        if Pes == 'I':
            Variable=Check_S_Valor
        elif Pes == 'T':
            Variable=Check_ST_Valor
            Check_A_PL.place_forget()
        LimitY_S=Ec.Limites_Y_S(Valor)
        Slider['from_']=str(LimitY_S[0])
        Slider['to']=str(LimitY_S[1]) 
        if LimitY_S[2] == 1 :
            Check.place(relx=PosX, rely=PosY)
        else:
            Check.place_forget()
        if Variable.get():                       #Evalua El Checkbox "-", Para Valores Negativos                 
            Slider['from_']=str(float(-1)*LimitY_S[1])
            Slider['to']=str(float(-1)*LimitY_S[0]) 
    if Ident =='A1':                                  #Redefinir Slider "Py_A" De Antropomórfico 
        LimitY_A=Ec.Limites_Y_A(Valor)                           
        Slider['from_']=str(LimitY_A[1])
        Slider['to']=str(LimitY_A[0])                      
    if Ident =='A2':                                  #Redefinir Slider "Pz_A" De Antropomórfico   
        if Pes == 'I':
            LimitZ=Ec.Limites_Z_A(Px_A.get(), Py_A.get())
            Variable=Check_A_Valor
        elif Pes == 'T':
            LimitZ=Ec.Limites_Z_A(Pl_x.get(), Pl_y.get())
            Variable=Check_AT_Valor 
            Check_S_PL.place_forget() 
        if LimitZ[2] == 1 :
            Check.place(relx=PosX, rely=PosY)  
            if Variable.get():                   #Evalua El Checkbox "inf", Para Valores Del Limite Inferior                   
                Slider['from_']=str(LimitZ[1][1])
                Slider['to']=str(LimitZ[1][0]) 
            else:
                Slider['from_']=str(LimitZ[0][1])
                Slider['to']=str(LimitZ[0][0])  
        else:
            Check.place_forget()
            Slider['from_']=str(LimitZ[1])
            Slider['to']=str(LimitZ[0])  
                                                
def Cambio(Ident): #Función Para Detectar El Cambio De Los CheckBox
    if Ident == 'S':
        Red_Slider(['S', 'I', Py_S, Check_S, 3/16, 1/2+0.01], Px_S.get())
    elif Ident == 'A2':
        Red_Slider(['A2', 'I', Pz_A, Check_A, 3/16, 2/3+0.18], None)
    elif Ident == 'ST':
        Red_Slider(['S', 'T', Pl_y, Check_S_PL, 1/4-0.025, 1/3+0.22], Pl_x.get())
    elif Ident == 'AT':
        Red_Slider(['A2', 'T', Pl_z, Check_A_PL, 1/4-0.025, 2/3+0.15], None)        

def Cine_Directa(Vector, Valor): #Función Para Enviar y Calcular Cinemática Directa Con Los Sliders
    Identi=Vector[0]
    if (bool(Identi.find('E')))==False:        
        Matriz=Ec.Parametros(1, Qs1_S.get(), Qs2_S.get(), Qs3_S.get(), None, None, None)
        Wd.Llenado(Matriz, 1, 4)
    elif (bool(Identi.find('A')))==False:
        Matriz=Ec.Parametros(2, Qs1_A.get(), Qs2_A.get(), Qs3_A.get(), None, None, None)
        Wd.Llenado(Matriz, 5, 8)
    else:
        Matriz=Ec.Parametros(3, Qs1_R.get(), Qs2_R.get(), Qs3_R.get(), Qs4_R.get(), Qs5_R.get(), Qs6_R.get())  
        Wd.Llenado(Matriz, 9, 15)    
    hilos.Thread(target=Wd.Barra.Carga, args=(Vector[1],)).start()
    #print-->board.write
    board.write(Identi.encode()+b','+ Valor.encode()+b'\n')

def Cajas_DK(Vector): #Función Para Boton "Enviar". Se Calcula y Envia La Cinemática Directa Con Los Cuadros de Texto
    Identi=Vector[0]
    Valor=Vector[1]  
    Enviar(Vector)
    if (bool(Identi[0].find('E')))==False:
        Matriz=Ec.Parametros(1, float(Valor[0].get()), float(Valor[1].get()), float(Valor[2].get()), None, None, None)  
        Wd.Llenado(Matriz, 1, 4)   
    elif (bool(Identi[0].find('A')))==False:
        Matriz=Ec.Parametros(2, float(Valor[0].get()), float(Valor[1].get()), float(Valor[2].get()), None, None, None)  
        Wd.Llenado(Matriz, 5, 8)   
    else:
        Matriz=Ec.Parametros(3, float(Valor[0].get()), float(Valor[1].get()), float(Valor[2].get()), float(Valor[3].get()), float(Valor[4].get()), float(Valor[5].get()))  
        Wd.Llenado(Matriz, 9, 15)          

def Cine_Inversa(Vector): #Función Para Calcular Cinematica Inversa Del Scara
    Identi=Vector[0]
    Codos=Vector[1]
    if Identi=='S':
        Vec_IK=Ec.Calculo_Inversa(1, float(Px_S.get()), float(Py_S.get()), float(Pz_S.get())) 
        Codos[0].Ubicacion(1/2,1/2,tk.N)
        Codos[1].Ubicacion(2/3, 1/2, tk.N)
        #Inserta Valores de Variables de Juntura en La Interfaz (Codo Abajo y Codo Arriba)
        q1_S.set(str(int(Vec_IK[0]/10)))
        q2_S_D.set(str(int(Vec_IK[1])))
        q3_S_D.set(str(int(Vec_IK[2])))
        q2_S_U.set(str(int(Vec_IK[3])))
        q3_S_U.set(str(int(Vec_IK[4])))        
    elif Identi=='A':
        Vec_IK=Ec.Calculo_Inversa(2, float(Px_A.get()), float(Py_A.get()), float(Pz_A.get())) 
        Codos[0].Ubicacion(1/2, 1/2, tk.N)
        Codos[1].Ubicacion(2/3, 1/2, tk.N)
        if Vec_IK[0]<(-1):
            Vec_IK[0]=360+Vec_IK[0]
        #Inserta Valores de Variables de Juntura en La Interfaz (Codo Abajo y Codo Arriba)
        q1_A.set(str(int(Vec_IK[0])))
        q2_A_D.set(str(int(Vec_IK[1])))
        q3_A_D.set(str(int(Vec_IK[2])))
        q2_A_U.set(str(int(Vec_IK[3])))
        q3_A_U.set(str(int(Vec_IK[4])))
        
    #Desabilitación de Botones de Envio Cinematica Inversa
    if Vec_IK[5] or Vec_IK[6]: #indar indab
        if  Vec_IK[6] == 1:#indab
            Codos[0].place_forget()
        if  Vec_IK[5] == 1:#indar
            Codos[1].place_forget()
        MsB.showwarning("Advertencia Selección Codo","""
        Una o ambas soluciones supera los limites mecanicos.
                                Varie el valor del punto
                     """)

def Enviar(Vector): #Función Donde Se Envia Los Datos
    Identi=Vector[0]
    Valor=Vector[1]    
    for i in range (0,len(Identi)):
        #print-->board.write
        #hilos.Thread(target=Wd.Barra.Carga, args=(Vector[2],)).start()
        board.write(Identi[i].encode()+Valor[i].get().encode())  
        tm.sleep(4)

def Jacobians(Barra): #Función Para Mostrar Los Jacobianos
    j_S=Ec.Jacobianos(1, Qs1_S.get(), Qs2_S.get(), Qs3_S.get())    
    j_A=Ec.Jacobianos(2, Qs1_A.get(), Qs2_A.get(), Qs3_A.get())    
    Matriz=[j_S[0], j_S[1], j_A[0], j_A[1]]
    hilos.Thread(target=Wd.Barra.Carga, args=(Barra,)).start()
    Wd.Llenado_Jaco(Matriz, 1, 4)
    
#Objetos Principales
Ventana = tk.Tk()
Ventana.title('Controles de Manipuladores Roboticos')
# width=Ventana.winfo_screenwidth()  
# height= Ventana.winfo_screenheight() 
# Ventana.geometry("%dx%d" % (width, height))
Panel_Pestañas = ttk.Notebook(Ventana)
Panel_Pestañas.pack(fill='both',expand='yes')

#Variables 
Nombres= tk.StringVar() #Variable String Para Nombres
Nombres.set("""
Dario Delgado - 1802992 \n 
Brayan Ulloa - 1802861 \n 
Fernando Llanes - 1802878 \n
Karla Baron - 1803648 \n 
Sebastian Niño - 1803558
""")
Reposo= tk.StringVar() #Variable String Para Mensaje Reposo
Reposo.set("Parte de reposo \r termina en reposo: \r Ti=0; Vi=0; Vf=0")
Wd.Variables_Matrices(15, 4, 4, "DK") #Variables Matrices DK
Wd.Variables_Matrices(4, 6, 3, "Jaco") #Variables Matrices Jacobianos Scara-Antropomórfico
Wd.Variables_Matrices(2, 6, 6, "JacoR") #Variables Matrices Jacobianos R
Estado_S=False
Estado_A=False
Estado_R=False
Check_S_Valor=tk.BooleanVar()
Check_A_Valor=tk.BooleanVar()
Check_ST_Valor=tk.BooleanVar()
Check_AT_Valor=tk.BooleanVar()

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
Fi=Wd.Frame(Pestaña_Info, 'GUI Para Controlar Manipuladores Robóticos', Fuente_12, 1, 1, 0, 0, None) #Frame
Wd.Labels(Fi, Nombres, None, None, None, None, Fuente_25, None).Ubicacion(1/2, 1/2, tk.CENTER)#Label-Nombres
#Com=Wd.Boton(Fi, 20, 5, 'COM Close', None).Ubicacion(1/2, 7/8, tk.CENTER)

#Imagenes
Logo= Wd.Imagenes('./Imagenes/LOGOUMNG.png').zoom(2)                        #Logo UMNG
tk.Label(Fi, image=Logo).place(relx=1/4, rely=1/2, anchor=tk.CENTER)
Icono= Wd.Imagenes('./Imagenes/icon.png').zoom(2)                           #Icono Robot
tk.Label(Fi, image=Icono).place(relx=3/4, rely=1/2, anchor=tk.CENTER)

##################################Pestaña 2########################################
Fr_DK_S=Wd.Frame(Pestaña_Scara, 'Cinemática Directa', Fuente_12, 1, 5/8, 0, 0, None)   #Frame Cinematica Directa
Fr_IK_S=Wd.Frame(Pestaña_Scara, 'Cinemática Inversa', Fuente_12, 1, 3/8, 0, 5/8, None) #Frame Cinematica Inversa

######Cinematica Directa######

#Barra De Progreso
Ba_S=Wd.Barra(Fr_IK_S, 300, 1/6, 0.98, 0.25, tk.E)

#Sliders
Qs1_S=Wd.Slider(Fr_DK_S, 1, 19, 1, 250, 34, 'Desplazamiento Base', Fuente_Slider, Cine_Directa, ['Eb',Ba_S])
Qs1_S.Ubicacion(0,0)
Qs2_S=Wd.Slider(Fr_DK_S, 0, 180, 10, 250, 34, 'Rotación Antebrazo', Fuente_Slider, Cine_Directa, ['Ebr',Ba_S])
Qs2_S.Ubicacion(0, 1/3)
Qs3_S=Wd.Slider(Fr_DK_S, 0, 180, 10, 250, 34, 'Rotación Brazo', Fuente_Slider, Cine_Directa, ['Eab',Ba_S])
Qs3_S.Ubicacion(0, 2/3)
Qt1_S=Wd.Editables(Fr_DK_S, Fuente_Num, 3/16, 0.11)
Qt2_S=Wd.Editables(Fr_DK_S, Fuente_Num, 3/16, 1/3+0.11)
Qt3_S=Wd.Editables(Fr_DK_S, Fuente_Num, 3/16, 2/3+0.11)
Qt_S=[Qt1_S, Qt2_S, Qt3_S]
#Seteo Inicial
Qs3_S.set(90)
board.write(b'Eb,1\r\n')
board.write(b'Ebr,5\r\n')




#Matrices
Wd.Matrices(Fr_DK_S, "DK", 1, 4, 4, "Link 1", 1/2, 0, Fuente_12)
Wd.Matrices(Fr_DK_S, "DK", 2, 4, 4, "Link 2", 5/6, 0, Fuente_12)
Wd.Matrices(Fr_DK_S, "DK", 3, 4, 4, "Link 3", 1/2, 1/2, Fuente_12)
Wd.Matrices(Fr_DK_S, "DK", 4, 4, 4, "Total", 5/6, 1/2, Fuente_12)

#Botones
Wd.Boton(Fr_DK_S, None, None, "Instrucciones", "LightYellow2", Mensajes, 'DK').Ubicacion(1, 1, tk.SE)
Gp_S=Wd.Boton(Fr_DK_S, 15, 3, "Griper", "lime green", Gripper, 'E')
Gp_S.Ubicacion(4/6, 0.9, tk.CENTER)
Wd.Boton(Fr_DK_S, 12, 2, "Enviar", "ivory3", Cajas_DK, [['Eb,','Ebr,','Eab,'], Qt_S, Ba_S]).Ubicacion(1/4+0.02, 0.9, tk.W)

######Cinematica Inversa######
#Sliders

Py_S=Wd.Slider(Fr_IK_S, -90, 90, 0.5, 250, 20, 'Py', Fuente_Slider, Red_Slider, ['N','N'])
Py_S.Ubicacion(0, 1/3)
Pz_S=Wd.Slider(Fr_IK_S, 0, 190, 10, 250, 20, 'Pz', Fuente_Slider, Red_Slider, ['N','N'])
Pz_S.Ubicacion(0, 2/3)
Check_S=Wd.Check(Fr_IK_S, '-', 3/16, 1/3+0.18, Cambio, 'S', Check_S_Valor)
Px_S=Wd.Slider(Fr_IK_S, -101.5, 345, 0.5, 250, 20, 'Px', Fuente_Slider, Red_Slider, ['S', 'I', Py_S, Check_S, 3/16, 1/2+0.01])
Px_S.Ubicacion(0, 0)

#Codo Abajo
Co_D_S=Wd.Frame(Fr_IK_S, "Codo Abajo", Fuente_12, 1/10, 1/2, 1/2, 0, tk.N)
q1_S=tk.StringVar()
q2_S_D=tk.StringVar()
q3_S_D=tk.StringVar()
qs_S_D=[q1_S, q2_S_D, q3_S_D]
Wd.Labels(Co_D_S, None, "d₁", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 0, tk.NW)      
Wd.Labels(Co_D_S, q1_S, None, None, None, None, Fuente_15, "white").Ubicacion(1, 0, tk.NE)     
Wd.Labels(Co_D_S, None, "θ₂", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 1/3, tk.NW)  
Wd.Labels(Co_D_S, q2_S_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 1/3, tk.NE)   
Wd.Labels(Co_D_S, None, "θ₃", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 2/3, tk.NW)  
Wd.Labels(Co_D_S, q3_S_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 2/3, tk.NE) 

#Codo Arriba
Co_U_S=Wd.Frame(Fr_IK_S, "Codo Arriba", Fuente_12, 1/10, 1/2, 2/3, 0, tk.N)
q2_S_U=tk.StringVar()
q3_S_U=tk.StringVar()
qs_S_U=[q1_S, q2_S_U, q3_S_U]
Wd.Labels(Co_U_S, None, "d₁", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 0, tk.NW)      
Wd.Labels(Co_U_S, q1_S, None, None, None, None, Fuente_15, "white").Ubicacion(1, 0, tk.NE)     
Wd.Labels(Co_U_S, None, "θ₂", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 1/3, tk.NW)  
Wd.Labels(Co_U_S, q2_S_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 1/3, tk.NE)   
Wd.Labels(Co_U_S, None, "θ₃", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 2/3, tk.NW)  
Wd.Labels(Co_U_S, q3_S_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 2/3, tk.NE)  

#Botones
Wd.Boton(Fr_IK_S, None, None, "Instrucciones", "LightYellow2", Mensajes, 'IK').Ubicacion(1, 1, tk.SE)
CodoD_S=Wd.Boton(Fr_IK_S, 12, 2, "Codo Abajo", "ivory3", Enviar, [['Eb,','Ebr,','Eab,'], qs_S_D, Ba_S])
CodoU_S=Wd.Boton(Fr_IK_S, 12, 2, "Codo Arriba", "ivory3", Enviar, [['Eb,','Ebr,','Eab,'], qs_S_U, Ba_S])
Wd.Boton(Fr_IK_S, 12, 8, "Calcular", "dim gray", Cine_Inversa, ['S', [CodoD_S, CodoU_S]]).Ubicacion(1/4+0.02, 1/2, tk.W)

##################################Pestaña 3########################################
Fr_DK_A=Wd.Frame(Pestaña_Antro3R, 'Cinemática Directa', Fuente_12, 1, 5/8, 0, 0, None)   #Frame Cinematica Directa
Fr_IK_A=Wd.Frame(Pestaña_Antro3R, 'Cinemática Inversa', Fuente_12, 1, 3/8, 0, 5/8, None) #Frame Cinematica Inversa

######Cinematica Directa######

#Barra De Progreso
Ba_A=Wd.Barra(Fr_IK_A, 300, 1/6, 0.98, 0.25, tk.E)

#Sliders
Qs1_A=Wd.Slider(Fr_DK_A, 0, 360, 10, 250, 34, 'Rotación Base', Fuente_Slider, Cine_Directa, ['Ab',Ba_A])
Qs1_A.Ubicacion(0, 0)
Qs2_A=Wd.Slider(Fr_DK_A, 0, 180, 10, 250, 34, 'Rotación Brazo', Fuente_Slider, Cine_Directa, ['Aab',Ba_A])
Qs2_A.Ubicacion(0, 2/3)
Qs3_A=Wd.Slider(Fr_DK_A, 0, 180, 10, 250, 34, 'Rotación Antebrazo', Fuente_Slider, Cine_Directa, ['Abr',Ba_A])
Qs3_A.Ubicacion(0, 1/3)
Qt1_A=Wd.Editables(Fr_DK_A,Fuente_Num, 3/16, 0.11)
Qt2_A=Wd.Editables(Fr_DK_A,Fuente_Num, 3/16, 1/3+0.11)
Qt3_A=Wd.Editables(Fr_DK_A,Fuente_Num, 3/16, 2/3+0.11)
Qt_A=[Qt1_A, Qt2_A, Qt3_A]

#Matrices
Wd.Matrices(Fr_DK_A, "DK", 5, 4, 4, "Link 1", 1/2, 0, Fuente_12)
Wd.Matrices(Fr_DK_A, "DK", 6, 4, 4, "Link 2", 5/6, 0, Fuente_12)
Wd.Matrices(Fr_DK_A, "DK", 7, 4, 4, "Link 3", 1/2, 1/2, Fuente_12)
Wd.Matrices(Fr_DK_A, "DK", 8, 4, 4, "Total", 5/6, 1/2, Fuente_12)

#Botones
Wd.Boton(Fr_DK_A, None, None, "Instrucciones", "LightYellow2", Mensajes, 'DK').Ubicacion(1, 1, tk.SE)
Gp_A=Wd.Boton(Fr_DK_A, 15, 3, "Griper", "lime green", Gripper, 'A')
Gp_A.Ubicacion(4/6, 0.9, tk.CENTER)
Wd.Boton(Fr_DK_A, 12, 2, "Enviar", "ivory3", Cajas_DK, [['Ab,','Abr,','Aab,'], Qt_A, Ba_A]).Ubicacion(1/4+0.02, 0.9, tk.W)

######Cinematica Inversa######

#Sliders
Pz_A=Wd.Slider(Fr_IK_A, None, None, 0.5, 250, 20, 'Pz', Fuente_Slider, Red_Slider, ['N','N'])
Pz_A.Ubicacion(0, 2/3)
Check_A=Wd.Check(Fr_IK_A, 'Inf', 3/16, 2/3+0.18, Cambio, 'A2', Check_A_Valor)
Py_A=Wd.Slider(Fr_IK_A, None, None, 0.5, 250, 20, 'Py', Fuente_Slider, Red_Slider, ['A2', 'I', Pz_A, Check_A, 3/16, 2/3+0.18])
Py_A.Ubicacion(0, 1/3)
Px_A=Wd.Slider(Fr_IK_A, -197, 197, 0.5, 250, 20, 'Px', Fuente_Slider, Red_Slider, ['A1', 'I', Py_A, None, None, None])
Px_A.Ubicacion(0, 0)

#Codo Abajo
Co_D_A=Wd.Frame(Fr_IK_A, "Codo Abajo", Fuente_12, 1/10, 1/2, 1/2, 0, tk.N)
q1_A=tk.StringVar()
q2_A_D=tk.StringVar()
q3_A_D=tk.StringVar()
qs_A_D=[q1_A, q2_A_D, q3_A_D]
Wd.Labels(Co_D_A, None, "θ₁", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 0, tk.NW)      
Wd.Labels(Co_D_A, q1_A, None, None, None, None, Fuente_15, "white").Ubicacion(1, 0, tk.NE)     
Wd.Labels(Co_D_A, None, "θ₂", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 1/3, tk.NW)  
Wd.Labels(Co_D_A, q2_A_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 1/3, tk.NE)   
Wd.Labels(Co_D_A, None, "θ₃", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 2/3, tk.NW)  
Wd.Labels(Co_D_A, q3_A_D, None, None, None, None, Fuente_15, "white").Ubicacion(1, 2/3, tk.NE) 

#Codo Arriba
Co_U_A=Wd.Frame(Fr_IK_A, "Codo Arriba", Fuente_12, 1/10, 1/2, 2/3, 0, tk.N)
q2_A_U=tk.StringVar()
q3_A_U=tk.StringVar()
qs_A_U=[q1_A, q2_A_U, q3_A_U]
Wd.Labels(Co_U_A, None, "θ₁", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 0, tk.NW)      
Wd.Labels(Co_U_A, q1_A, None, None, None, None, Fuente_15, "white").Ubicacion(1, 0, tk.NE)     
Wd.Labels(Co_U_A, None, "θ₂", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 1/3, tk.NW)  
Wd.Labels(Co_U_A, q2_A_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 1/3, tk.NE)   
Wd.Labels(Co_U_A, None, "θ₃", None, None, None, Fuente_15, "sandy brown").Ubicacion(0, 2/3, tk.NW)  
Wd.Labels(Co_U_A, q3_A_U, None, None, None, None, Fuente_15, "white").Ubicacion(1, 2/3, tk.NE)  

#Botones
Wd.Boton(Fr_IK_A, None, None, "Instrucciones", "LightYellow2", Mensajes, 'IK').Ubicacion(1, 1, tk.SE)
CodoD_A=Wd.Boton(Fr_IK_A, 12, 2, "Codo Abajo", "ivory3", Enviar, [['Ab,','Abr,','Aab,'], qs_A_D, Ba_A])
CodoU_A=Wd.Boton(Fr_IK_A, 12, 2, "Codo Arriba", "ivory3", Enviar, [['Ab,','Abr,','Aab,'], qs_A_U, Ba_A])
Wd.Boton(Fr_IK_A, 12, 8, "Calcular", "dim gray", Cine_Inversa, ['A', [CodoD_A, CodoU_A]]).Ubicacion(1/4+0.02, 1/2, tk.W)

##################################Pestaña 4########################################

#Desplegable
Despl_R=Wd.Desplegable(Pestaña_Antro6R, ["Cinemática Directa", "Cinemática Inversa"])
Despl_R.Ubicacion(0, 0)
Despl_R.bind("<<ComboboxSelected>>",Despl_R.Cambio)
Fr_DK_R=Despl_R.Frame_DK
Fr_IK_R=Despl_R.Frame_IK
#####Cinematica Directa######

#Barra De Progreso
Ba_R=Wd.Barra(Fr_DK_R, 200, 1/15, 0.98, 3/4, tk.NE)

#Sliders
Qs1_R=Wd.Slider(Fr_DK_R,0, 360, 0.5, 250, 34, 'Rotación Primera Base', Fuente_Slider, Cine_Directa, ['Rb1',Ba_R])
Qs1_R.Ubicacion(0, 0)
Qs2_R=Wd.Slider(Fr_DK_R,0, 360, 0.5, 250, 34, 'Rotación Primer Brazo', Fuente_Slider, Cine_Directa, ['Rbr1',Ba_R])
Qs2_R.Ubicacion(0, 1/6)
Qs3_R=Wd.Slider(Fr_DK_R,0, 360, 0.5, 250, 34, 'Rotación Segundo Brazo', Fuente_Slider, Cine_Directa, ['Rbr2',Ba_R])
Qs3_R.Ubicacion(0, 2/6)
Qs4_R=Wd.Slider(Fr_DK_R,0, 360, 0.5, 250, 34, 'Rotación Segunda Base', Fuente_Slider, Cine_Directa, ['Rb2',Ba_R])
Qs4_R.Ubicacion(0, 3/6)
Qs5_R=Wd.Slider(Fr_DK_R,0, 360, 0.5, 250, 34, 'Rotación Antebrazo', Fuente_Slider, Cine_Directa, ['Rab',Ba_R])
Qs5_R.Ubicacion(0, 4/6)
Qs6_R=Wd.Slider(Fr_DK_R,0, 360, 0.5, 250, 34, 'Rotación Muñeca', Fuente_Slider, Cine_Directa, ['Rm',Ba_R])
Qs6_R.Ubicacion(0, 5/6)
Qt1_R=Wd.Editables(Fr_DK_R, Fuente_Num, 3/16, 1/18+0.014)
Qt2_R=Wd.Editables(Fr_DK_R, Fuente_Num, 3/16, 4/18+0.014)
Qt3_R=Wd.Editables(Fr_DK_R, Fuente_Num, 3/16, 7/18+0.014)
Qt4_R=Wd.Editables(Fr_DK_R, Fuente_Num, 3/16, 10/18+0.014)
Qt5_R=Wd.Editables(Fr_DK_R, Fuente_Num, 3/16, 13/18+0.014)
Qt6_R=Wd.Editables(Fr_DK_R, Fuente_Num, 3/16, 16/18+0.014)
Qt_R=[Qt1_R, Qt2_R, Qt3_R, Qt4_R, Qt5_R, Qt6_R]

#Matrices
Wd.Matrices(Fr_DK_R, "DK", 9, 4, 4, "Link 1", 1/2, 0, Fuente_12)
Wd.Matrices(Fr_DK_R, "DK", 10, 4, 4, "Link 2", 5/6, 0, Fuente_12)
Wd.Matrices(Fr_DK_R, "DK", 11, 4, 4, "Link 3", 1/2, 1/4, Fuente_12)
Wd.Matrices(Fr_DK_R, "DK", 12, 4, 4, "Link 4", 5/6, 1/4, Fuente_12)
Wd.Matrices(Fr_DK_R, "DK", 13, 4, 4, "Link 5", 1/2, 2/4, Fuente_12)
Wd.Matrices(Fr_DK_R, "DK", 14, 4, 4, "Link 6", 5/6, 2/4, Fuente_12)
Wd.Matrices(Fr_DK_R, "DK", 15, 4, 4, "Total", 2/3, 3/4, Fuente_12)

#Botones
Wd.Boton(Fr_DK_R, None, None, "Instrucciones", "LightYellow2", Mensajes, 'DK').Ubicacion(1, 1, tk.SE)
Gp_R=Wd.Boton(Fr_DK_R, 15, 3, "Griper", "lime green", Gripper, 'R')
Gp_R.Ubicacion(7/16, 3/4+0.1, tk.N)
Wd.Boton(Fr_DK_R, 12, 2, "Enviar", "ivory3", Cajas_DK, [['Rb1,','Rbr1,','Rbr2,','Rb2,','Rab,','Rm,'], Qt_R, Ba_R]).Ubicacion(7/16, 3/4, tk.N)

######Cinematica Inversa######

#Sliders
# Wd.Slider(Fr_IK_R, -200, 200, 0.5, 250, 34, 'Px', Fuente_Slider, None, None).Ubicacion(0, 0)
# Wd.Slider(Fr_IK_R, -200, 200, 0.5, 250, 34, 'Py', Fuente_Slider, None, None).Ubicacion(0, 1/6)
# Wd.Slider(Fr_IK_R, -200, 200, 0.5, 250, 34, 'Pz', Fuente_Slider, None, None).Ubicacion(0, 2/6)
# Wd.Slider(Fr_IK_R, -200, 200, 0.5, 250, 34, 'Alfa', Fuente_Slider, None, None).Ubicacion(0, 3/6)
# Wd.Slider(Fr_IK_R, -200, 200, 0.5, 250, 34, 'Beta', Fuente_Slider, None, None).Ubicacion(0, 4/6)
# Wd.Slider(Fr_IK_R, -200, 200, 0.5, 250, 34, 'Gamma', Fuente_Slider, None, None).Ubicacion(0, 5/6)

#Botones
Wd.Boton(Fr_IK_R, None, None, "Instrucciones", "LightYellow2", Mensajes, 'IK').Ubicacion(1, 1, tk.SE)

##################################Pestaña 5########################################

Fr_T_J=Wd.Frame(Pestaña_Trayectorias_Jacobiano, 'Planificación de Trayectorias Por Jacobiano Inverso', Fuente_12, 1, 1, 0, 0, None)   #Frame Jacobiano

##################################Pestaña 6########################################

Fr_J=Wd.Frame(Pestaña_Jacobianos, 'Jacobianos', Fuente_12, 1, 1, 0, 0, None)   #Frame Jacobiano

#Barra De Progreso
Ba_J=Wd.Barra(Fr_J, 300, 1/15, 1/2, 1/3, tk.N)

#Matrices
Wd.Matrices(Fr_J, "Jaco", 1, 6, 3, "Jacobiano Scara Geométrico", 1/4, 0, Fuente_12)
Wd.Matrices(Fr_J, "Jaco", 2, 6, 3, "Jacobiano Scara Analítico", 3/4, 0, Fuente_12)
Wd.Matrices(Fr_J, "Jaco", 3, 6, 3, "Jacobiano Antropomórfico Geométrico", 1/4, 1/3, Fuente_12)
Wd.Matrices(Fr_J, "Jaco", 4, 6, 3, "Jacobiano Antropomórfico Analítico", 3/4, 1/3, Fuente_12)
Wd.Matrices(Fr_J, "JacoR", 1, 6, 6, "Jacobiano Antropomórfico 6R Geométrico", 1/4, 2/3, Fuente_12)
Wd.Matrices(Fr_J, "JacoR", 2, 6, 6, "Jacobiano Antropomórfico 6R Analítico", 3/4, 2/3, Fuente_12)

#Botones
#Wd.Boton(Fr_J, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)
Wd.Boton(Fr_J, 15, 3, "Mostrar", "dim gray", Jacobians, Ba_J).Ubicacion(1/2, 1/2, tk.N)

##################################Pestaña 7########################################

Fr_T=Wd.Frame(Pestaña_Trayectorias, 'Datos de Entrada', Fuente_12, 1, 1/4, 0, 0, None)   #Frame Datos Trayectorias

#Desplegables
Despl_Mani=Wd.Desplegable(Fr_T, ["Scara (PRR)", "Antropomórfico (RRR)"])
Despl_Mani.Ubicacion(0, 0)
Despl_Mani.bind("<<ComboboxSelected>>",Show_Sliders)
Despl_Codo=Wd.Desplegable(Fr_T, ["Codo Arriba", "Codo Abajo"])
Despl_Codo.bind("<<ComboboxSelected>>",Show_Perfiles)

#Label Información Importante (Parte de Reposo)
Wd.Labels(Fr_T, Reposo, None, 1, "solid", None, Fuente_15, None).Ubicacion(4/16, 0, None)

#Puntos Iniciales-Finales
#Labels
P_xi=Wd.Labels(Fr_T, None, "0", 1, "solid", 12, None, None)
P_yi=Wd.Labels(Fr_T, None, "0", 1, "solid", 12, None, None)
P_zi=Wd.Labels(Fr_T, None, "0", 1, "solid", 12, None, None)
P_x= Wd.Labels(Fr_T, None, "Px", None, None, None, None, None)
P_y= Wd.Labels(Fr_T, None, "Py", None, None, None, None, None)
P_z= Wd.Labels(Fr_T, None, "Pz", None, None, None, None, None)

#Buttons
Tipo=tk.IntVar()
Cuadratico=Wd.Radio(Fr_T, "Perfil Cuadrático", Fuente_12, 1, Tipo, 15, Show_Datos)
TrapezoidalI=Wd.Radio(Fr_T, "Perfil Trapezoidal I", Fuente_12, 2, Tipo, 15, Show_Datos)
TrapezoidalII=Wd.Radio(Fr_T, "Perfil Trapezoidal II", Fuente_12, 3, Tipo, 15, Show_Datos)
#Calcular_PT=Wd.Boton(Fr_T, 12, None, "Calcular", "dim gray")
#Wd.Boton(Fr_T, None, None, "Instrucciones", "LightYellow2").Ubicacion(1, 1, tk.SE)

#Barra De Progreso
Br_Pl=Wd.Barra(Fr_T, 150, 1/8, 5/16, 1, tk.S)

#Sliders
Check_S_PL=Wd.Check(Fr_T, '-', 1/4-0.025, 1/3+0.22, Cambio, 'ST', Check_ST_Valor)
Check_A_PL=Wd.Check(Fr_T, 'Inf', 1/4-0.025, 2/3+0.15, Cambio, 'AT', Check_AT_Valor)
Pl_x=Wd.Slider(Fr_T, None, None, 0.5, 180, 20, None, None, Alter_Sliders, 'A1')              
Pl_y=Wd.Slider(Fr_T, None, None, 0.5, 180, 20, None, None, Alter_Sliders, 'A2')
Pl_z=Wd.Slider(Fr_T, None, None, 0.5, 180, 20, None, None, Show_Codo, None)
# T_f=Wd.Slider(Fr_T, 15, 40, 1, 180, 20, None, None, None, None)
# N_p=Wd.Slider(Fr_T, 10, 1000, 10, 180, 20, None, None, None, None)
# Vj_1=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None, None, None)
# Vj_2=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None, None, None)
# Vj_3=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None, None, None)
# Aj_1=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None, None, None)
# Aj_2=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None, None, None)
# Aj_3=Wd.Slider(Fr_T, None, None, 0.2, 180, 20, None, None, None, None)

# #Wd.Aparecer(Despl_Codo, 4/16+0.01, 4/6)
# #Titulos
P_inicial=Wd.Labels(Fr_T, None, "Puntos Iniciales", None, None, 12, Fuente_Num2, None)
P_final=Wd.Labels(Fr_T, None, "Puntos Finales", None, None, 12, Fuente_Num2, None)
T_Codo=Wd.Labels(Fr_T, None, "Elección Codo", None, None, 12, Fuente_Num2, None)
TT_f=Wd.Labels(Fr_T, None, "Tf", None, None, None, Fuente_Num2, None)
TN_p=Wd.Labels(Fr_T, None, "Np", None, None, None, Fuente_Num2, None)
TVc_1=Wd.Labels(Fr_T, None, "Vc1", None, None, None, Fuente_Num2, None)
TVc_2=Wd.Labels(Fr_T, None, "Vc2", None, None, None, Fuente_Num2, None)
TVc_3=Wd.Labels(Fr_T, None, "Vc3", None, None, None, Fuente_Num2, None)
TAc_1=Wd.Labels(Fr_T, None, "Ac1", None, None, None, Fuente_Num2, None)
TAc_2=Wd.Labels(Fr_T, None, "Ac2", None, None, None, Fuente_Num2, None)
TAc_3=Wd.Labels(Fr_T, None, "Ac3", None, None, None, Fuente_Num2, None)

Fr_Graf=Wd.Frame(Pestaña_Trayectorias, 'Gráficas', Fuente_12, 1, 3/4, 0, 1/4, None)   #Frame Graficas
Wd.Grafica(Fr_Graf, r'Posición $q_1$', "q[°]", 0, 0)
Wd.Grafica(Fr_Graf, r'Posición $q_2$', "q[°]", 1/3, 0)
Wd.Grafica(Fr_Graf, r'Posición $q_3$', "q[°]", 2/3, 0)
Wd.Grafica(Fr_Graf, r'Velocidad $w_1$', r'w$[rad/s]$', 0, 1/2)
Wd.Grafica(Fr_Graf, r'Velocidad $w_2$', r'w$[rad/s]$', 1/3, 1/2)
Wd.Grafica(Fr_Graf, r'Velocidad $w_3$', r'w$[rad/s]$', 2/3, 1/2)

Ventana.attributes('-fullscreen',True)
Ventana.mainloop()