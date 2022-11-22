###### Librerias ######
import tkinter as tk
<<<<<<< Updated upstream
import Ecuaciones as Ec
=======
>>>>>>> Stashed changes
import numpy as np
import time as tm
import functools as tools
import Ecuaciones as Ec
###### Modulos De Librerias ######
import tkinter.font as Fuentes
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
###### SubModulos De Librerias ######
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as Canvas

class Pestañas(ttk.Frame): #Clase Para Crear Pestañas
    def __init__(self, Pestana, texto:str): 
        super().__init__(Pestana) 
        Pestana.add(self, text=texto)
        
class Frame(tk.LabelFrame): #Clase Para Crear Frames
    def __init__(self, frame_padre, texto:str, Fuente, ancho, alto, posx, posy, referencia):
        super().__init__(frame_padre, text=texto, font=Fuente, labelanchor='n')        
        self.place(relx=posx, rely=posy, relwidth=ancho, relheight=alto, anchor=referencia)

class Fuentes(Fuentes.Font): #Clase Para Crear Fuentes
    def __init__(self, familia:str, tamaño):
        super().__init__(family=familia, size=tamaño)  

class Labels(tk.Label): #Clase Para Crear Labels
    def __init__(self, frame_padre, variable:str, texto:str, T_Borde:int, Estilo, Tamano, Fuente, Fondo:str): 
        super().__init__(frame_padre, textvariable=variable, text=texto, borderwidth=T_Borde, relief=Estilo, font=Fuente, width=Tamano, bg=Fondo, pady=0, padx=0) 
    def Ubicacion(self, Posx, Posy, referencia):
        self.place(relx=Posx, rely=Posy, anchor=referencia)

class Imagenes(tk.PhotoImage): #Clase Para Insertar Imagenes
    def __init__(self, archivo:str): 
        super().__init__(file=archivo)
        
class Editables(tk.Entry): #Clase Para Crear Edit Text
    def __init__(self, frame_padre, Fuente, posx, posy):
        self.entry_text = tk.StringVar() 
        super().__init__(frame_padre, width=7, font=Fuente, textvariable=self.entry_text, justify=tk.RIGHT)
        self.insert(tk.END,"0")
        self.place(relx=posx, rely=posy)
        self.entry_text.trace("w", lambda *args: self.limitador(self.entry_text))  
        
    def limitador(self, entry_text):#Limita La cantidad de caracteres ("6" en este caso)
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:6])
  
class Boton(tk.Button): #Clase Para Crear Botones    
    def __init__(self, Frame:tk, Ancho:float, Alto:float, Texto:str, Color:str, Comando, Identificador):        
        super().__init__(Frame, width=Ancho, height=Alto, text=Texto, bg=Color, bd=5, font=("Lucida Grande",10), command=tools.partial(Comando, Identificador))  
    def Ubicacion(self, posx, posy, referencia):
        self.place(relx=posx, rely=posy, anchor=referencia)
    
class Slider(tk.Scale): #Clase Para Crear Sliders
    def __init__(self, frame, inicio, final, paso, largo, ancho, texto:str, Fuente, Comando, Ident):   
        super().__init__(
            frame,
            from_=inicio,
            to=final,
            resolution=paso,
            orient = tk.HORIZONTAL,
            length=largo,
            width = ancho,
            cursor='dot',
            label = texto,            
            troughcolor='NavajoWhite2',
            font=Fuente,
            command=tools.partial(Comando, Ident)
            ) 

    def Ubicacion(self, posx, posy):
        self.place(relx=posx, rely=posy)    
            
class Variables_Matrices: #Crea la cantidad de variables que seran utilizadas para llenar las matrices
    def __init__(self, cantidad, filas, columnas, identificador:str):
        for n in range(1, cantidad+1):
            for i in range(1, filas+1):
                for j in range(1, columnas+1):
                    globals()[identificador+str(n)+"_" + str(i) + str(j)]=tk.StringVar()
                
class Matrices(): #Clase Para Crear Matrices
    def __init__(self, frame, identificador:str, matriz, filas, columnas, titulo:str, posx, posy, Fuente): 
        Contenedor=tk.LabelFrame(frame, text=titulo, font=Fuente, labelanchor='n')        
        Contenedor.place(relx=posx, rely=posy, anchor=tk.N)       
        for r in range(1, filas+1):
            for c in range(1, columnas+1):                
                cell = tk.Label(Contenedor, width=13,  textvariable=globals()[identificador + str(matriz) + "_" + str(r) + str(c)], bg='white', borderwidth=1, relief="solid")
                cell.grid(row=r, column=c, ipady=5)

class Check(tk.Checkbutton): #Clase Para Crear Check Boxes
    def __init__(self, frame, Texto, Posx, Posy, Comando, Ident, Var): 
        super().__init__(frame, text=Texto, command=tools.partial(Comando, Ident), variable=Var, relief='solid')
        self.place(relx=Posx, rely=Posy)

class Barra(ttk.Progressbar): #Clase Para Crear Barra De Progreso
    def __init__(self, frame, Largo, Ancho, Posx, Posy, referencia):         
        super().__init__(frame, length=Largo, maximum=100)                  
        self.place(relx=Posx, rely=Posy, anchor=referencia, relheight=Ancho) 
    def Carga(Barra):
        while Barra['value'] < 100:
            Barra['value'] += 10
            tm.sleep(0.02)
        Barra['value'] = 0

class Desplegable(ttk.Combobox): #Clase Para Crear Menu Desplegable
    def __init__(self, frame, Opciones:np.array): 
        self.frame=frame     
        self.Frame_DK=tk.LabelFrame(self.frame, text="Cinemática Directa", font=("Lucida Grande", 12), labelanchor='n')   
        self.Frame_IK=tk.LabelFrame(self.frame, text="Cinemática Inversa", font=("Lucida Grande", 12), labelanchor='n')
        super(Desplegable, self).__init__(frame, state="readonly", values=Opciones)

    def Ubicacion(self, Posx, Posy):
        self.place(relx=Posx, rely=Posy)  
                   
    def Cambio(self, event):#Función Para Elección (Antropomórfico R6)        
        if self.get() == "Cinemática Directa":
            self.Frame_DK.place(relx=0, rely=1/36, relwidth=1, relheight=35/36)
            self.Frame_IK.place_forget()
        else:
            self.Frame_IK.place(relx=0, rely=1/36, relwidth=1, relheight=35/36)
            self.Frame_DK.place_forget()    
   
class Radio(tk.Radiobutton): #Clase Para Crear Radio Button
    def __init__(self, frame, Texto, Fuente, Valor, Variable, Tamano, Comando):
        super().__init__(frame, text=Texto, font=Fuente, value=Valor, variable=Variable, width=Tamano, command=Comando)                
    def Ubicacion(self, Posx, Posy):
        self.place(relx=Posx, rely=Posy)

class Grafica(): #Clase Para Crear Graficas
    def __init__(self, Frame, Titulo, T_Ejey, Posx, Posy):
        fig, self.ax=plt.subplots(facecolor='#85888A') 
        fig.subplots_adjust(bottom=0.17, left=0.2)       
        self.ax.set_ylabel(T_Ejey)
        self.ax.set_xlabel(r'Time$[s]$')
        fig.align_labels()
        plt.title(Titulo, color='k', size=12, family="Arial")        
        canvas=Canvas(fig, master=Frame)
        canvas.get_tk_widget().place(relx=Posx, rely=Posy, relwidth=1/3, relheight=0.5)     
        # relwidth=1/3+0.02, relheight=1/3+0.05
    def Linea(self, Resolucion, Ampl_Min, Ampl_Max, Tiempo, Vec_Datos):
        self.ax.set_xlim(0, Tiempo)
        self.ax.set_ylim(Ampl_Min, Ampl_Max+(Signo(Ampl_Max)*0.5))   
        self.line,=self.ax.plot([], [], color='k', linestyle='solid', linewidth=2)
        paso=Tiempo/Resolucion
        self.line.set_data(np.arange(0, Tiempo, paso, dtype=float), Vec_Datos)
    
def Ocultar(Objetos): #Función Para Ocultar Objetos
    for i in range (0, len(Objetos)):
        Objetos[i].place_forget()

def Aparecer(Objetos:tk, Posx, Posy): #Función Para Aparecer Objetos
    for i in range (0, len(Objetos)):
        Objetos[i].place(relx=Posx[i], rely=Posy[i])

def Llenado (matri, M, K): #Función Para Llenado Matrices Cinemática Directa
    for n in range(M, K):
        for i in range(1, 5):
            for j in range(1, 5):                
                globals()["DK" + str(n) +"_" + str(i) + str(j)].set(matri[1][n-M][i-1][j-1])           
                globals()["DK" + str(K) +"_"+ str(i) + str(j)].set(matri[0][i-1][j-1]) 

def Llenado_Jaco (matri, M, K): #Función Para Llenado Matrices Jacobianos
    for n in range(M, K+1):        
            for j in range(1, 4):
                for i in range(0, 2):
                    h=i*3  
                    for k in range(1, 4):                                    
                        globals()["Jaco" + str(n) +"_" + str(k+h) + str(j)].set("{:.5f}".format(matri[n-M][i][j-1][k-1])) 

def Signo(x): #Determina El signo del numero
    if x>=0:
        sgn=1            
    else:
        sgn=-1
    return sgn

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

# def Manipulador(manipu,cod,Pxi,Pyi,Pzi,Pxf,Pyf,Pzf): #Determina el Manipulador a Utilizar
#     if manipu==1:
#         Inversai=Cal.IK_Scara_P3R(Pxi,Pyi,Pzi) #Cinematica Inversa para Punto Inicial        
#         Inversaf=Cal.IK_Scara_P3R(Pxf,Pyf,Pzf) #Cinematica Inversa para Punto Final
#         Junturas=Solucion(cod,Inversai,Inversaf)        
#     else:
#         Inversai=Cal.IK_Antropo_3R(Pxi,Pyi,Pzi) #Cinematica Inversa para Punto Inicial
#         Inversaf=Cal.IK_Antropo_3R(Pxf,Pyf,Pzf) #Cinematica Inversa para Punto Final
#         Junturas=Solucion(cod,Inversai,Inversaf)
#     return Junturas

# def Solucion(sol,Ini,Fin): #Determina la Solución a utilizar (Codo Arriba o Codo Abajo)
#     if sol==1: #Codo Abajo
#         Qi=[Ini[0],Ini[1],Ini[2]] #Toma los valores de las junturas iniciales para Codo Abajo 
#         Qf=[Fin[0],Fin[1],Fin[2]] #Toma los valores de las junturas finales para Codo Abajo 
#     else: #Codo Arriba
#         Qi=[Ini[0],Ini[3],Ini[4]] #Toma los valores de las junturas iniciales para Codo Arriba
#         Qf=[Fin[0],Fin[3],Fin[4]] #Toma los valores de las junturas finales para Codo Arriba
#     return Qi,Qf