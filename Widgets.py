from tkinter import ttk
import tkinter.font as Fuentes
import tkinter as tk
import Ecuaciones as Ec
import numpy as np


class Pestañas(ttk.Frame):
    def __init__(self, Pestana, texto:str): 
        super().__init__(Pestana) 
        Pestana.add(self, text=texto)
        
class Frame(tk.LabelFrame):
    def __init__(self, frame_padre, texto:str, Fuente, ancho, alto, posx, posy, referencia):
        super().__init__(frame_padre, text=texto, font=Fuente, labelanchor='n')        
        self.place(relx=posx, rely=posy, relwidth=ancho, relheight=alto,anchor=referencia)

class Fuentes(Fuentes.Font):
    def __init__(self, familia:str, tamaño):
        super().__init__(family=familia, size=tamaño)  

class Labels(tk.Label):
    def __init__(self, frame_padre, variable:str, texto:str, T_Borde:int, Estilo, Tamano, Fuente, Fondo:str): 
        super().__init__(frame_padre, textvariable=variable, text=texto, borderwidth=T_Borde, relief=Estilo, font=Fuente, width=Tamano, bg=Fondo, pady=0, padx=0) 
    def Ubicacion(self, Posx, Posy, referencia):
        self.place(relx=Posx, rely=Posy, anchor=referencia)

class Imagenes(tk.PhotoImage):
    def __init__(self, archivo:str): 
        super().__init__(file=archivo)
        
class Editables(tk.Entry):
    def __init__(self, frame_padre, Fuente, posx, posy):
        self.entry_text = tk.StringVar() 
        super().__init__(frame_padre, width = 7, font = Fuente, textvariable = self.entry_text, justify=tk.RIGHT)
        self.insert(tk.END,"0")
        self.place(relx=posx, rely=posy)
        self.entry_text.trace("w", lambda *args: self.limitador(self.entry_text))  
        
    def limitador(self, entry_text):#Limita La cantidad de caracteres
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:6])
           
class Boton(tk.Button):
    def __init__(self, frame, ancho, alto, texto:str, color:str):   
        super().__init__(frame, width=ancho, height=alto, text=texto, bg=color, bd=5, font=("Lucida Grande",10))  
    def Ubicacion(self, posx, posy, referencia):
        self.place(relx=posx, rely=posy, anchor=referencia)

class Slider(tk.Scale):
    def __init__(self, frame, inicio, final, paso, largo, ancho, texto:str, Fuente):   
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
            font=Fuente            
            #command = servo1,
            )     
    def Ubicacion(self, posx, posy):
        self.place(relx=posx, rely=posy)
            
class Variables_Matrices: #Crea la cantidad de variables que seran utilizadas para llenar las matrices
    def __init__(self, cantidad, filas, columnas, identificador:str):
        for n in range(1, cantidad+1):
            for i in range(1, filas+1):
                for j in range(1, columnas+1):
                    globals()[identificador+str(n)+"_" + str(i) + str(j)]=tk.StringVar()
                
class Matrices(tk.Label):
    def __init__(self, frame, identificador:str, matriz, filas, columnas, titulo:str, posx, posy, Fuente): 
        Contenedor=tk.LabelFrame(frame, text=titulo, font=Fuente, labelanchor='n')        
        Contenedor.place(relx=posx, rely=posy, anchor=tk.N)       
        for r in range(1, filas+1):
            for c in range(1, columnas+1):                
                cell = tk.Label(Contenedor, width=13,  textvariable=globals()[identificador + str(matriz) + "_" + str(r) + str(c)], bg='white', borderwidth=1, relief="solid")
                cell.grid(row=r, column=c, ipady=5)

class Check(tk.Checkbutton):
    def __init__(self, frame, Posx, Posy): 
        #checkbox_value = tk.BooleanVar()  variable=checkbox_value
        super().__init__(frame, text="-", relief="solid")
        self.place(relx=Posx, rely=Posy)

class Barra(ttk.Progressbar):
    def __init__(self,frame, Largo, Ancho, Posx, Posy, referencia): 
        super().__init__(frame, length=Largo, maximum=100)
        #(FrIKS, length=150, style='green.Horizontal.TProgressbar', maximum=100)
        # s = ttk.Style()
        # s.theme_use('alt')
        # s.configure("red.Horizontal.TProgressbar", background='red')
        # s.configure("green.Horizontal.TProgressbar", background='green')       
        self['value'] = 10
        self.place(relx=Posx, rely=Posy, anchor=referencia, relheight=Ancho)

class Desplegable(ttk.Combobox):
    def __init__(self, frame, Opciones:np.array, Posx, Posy): 
        self.frame=frame     
        self.Frame_DK=tk.LabelFrame(self.frame, text="Cinematica Directa", font=("Lucida Grande", 12),labelanchor='n')   
        self.Frame_IK=tk.LabelFrame(self.frame, text="Cinematica Inversa", font=("Lucida Grande", 12),labelanchor='n')
        super(Desplegable,self).__init__(frame, state="readonly", values=Opciones)
        self.place(relx=Posx, rely=Posy)    
                   
    def Cambio(self,event):#Función Para Elección Pestaña 4        
        if self.get() == "Cinematica Directa":
            self.Frame_DK.place(relx=0, rely=1/36, relwidth=1, relheight=35/36)
            self.Frame_IK.place_forget()
        else:
            self.Frame_IK.place(relx=0, rely=1/36, relwidth=1, relheight=35/36)
            self.Frame_DK.place_forget()

class Radio(tk.Radiobutton):
    def __init__(self, frame, Texto, Fuente, Valor, Variable, Tamano):
        super().__init__(frame, text=Texto, font=Fuente, value=Valor, variable=Variable, width=Tamano)
    def Ubicacion(self, Posx, Posy):
        self.place(relx=Posx, rely=Posy)

# def llenado (matri,M,K):  #Llenado Matrices
#     for n in range(M,K):
#         for i in range(0,4):
#             for j in range(0,4):                
#                 globals()["mat"+ str(n) +"_" + str(i) + str(j)].set(matri[1][n-M][i][j])             
#                 globals()["mat"+ str(K) +"_"+ str(i) + str(j)].set(matri[0][i][j]) 