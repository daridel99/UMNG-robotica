import math as mt
from turtle import pos
import Funciones as Fn
import numpy as np
from sympy import  *

def Perf_Cuadra(tf,n,Qi,Qf): #Encontrar Las Posiciones y Velocidades De Juntura Utilizando El Perfil Cuadratrico
    #Se recalcula un valor para "t" dependiendo la cantidad de puntos deseados (resolución)
    t = np.arange(0, tf+((tf)/(n-1)), (tf)/(n-1), dtype=float) 
    Err=0
    for i in range(0,3): #Ciclo de 3 para crear los vectores de las 3 junturas     
        #Calculo de las constantes "a". (1 Vez para cada juntura)   
        Cons_a=Constantes_Cuadra(float(tf),float(Qf[i]),float(Qi[i]))  
        if i==0:
            Pos_q1= Cons_a[3]*t**(3) + Cons_a[2]*t**(2) + Cons_a[1]*t + Cons_a[0]  #Vector de Posición Juntura 1 (d1=Desplazamiento Base)                                   
            Vel_q1 = 3*Cons_a[3]*t**(2) + 2*Cons_a[2]*t + Cons_a[1]              #Vector de Velocidad Juntura 1 (d1=Desplazamiento Base)    
        if i==1:
            Pos_q2 = Cons_a[3]*t**(3) + Cons_a[2]*t**(2) + Cons_a[1]*t + Cons_a[0] #Vector de Posición Juntura 2 (t2=Angulo Brazo)
            Vel_q2= 3*Cons_a[3]*t**(2) + 2*Cons_a[2]*t + Cons_a[1]               #Vector de Velocidad Juntura 2 (t2=Angulo Brazo)
        else:
            Pos_q3 = Cons_a[3]*t**(3) + Cons_a[2]*t**(2) + Cons_a[1]*t + Cons_a[0] #Vector de Posición Juntura 3 (t3=Angulo AnteBrazo)
            Vel_q3 = 3*Cons_a[3]*t**(2) + 2*Cons_a[2]*t + Cons_a[1]              #Vector de Velocidad Juntura 3 (t3=Angulo AnteBrazo) 
    
    return Err,Pos_q1,Pos_q2,Pos_q3,Vel_q1,Vel_q2,Vel_q3

def Perf_Trape(tf,n,Qi,Qf,vect,tipe): #Encontrar Las Posiciones y Velocidades De Juntura Utilizando El Perfil Trapezoidal    
    t = np.arange(0, tf+((tf)/(n-1)), (tf)/(n-1), dtype=float) 
    Pos_q1=np.empty(n)
    Pos_q2=np.empty(n)
    Pos_q3=np.empty(n)
    Vel_q1=np.empty(n)
    Vel_q2=np.empty(n)
    Vel_q3=np.empty(n)
    for j in range (0,len(t)):
        for i in range (0,3):
            Variab=Constantes_Trape(float(Qi[i]),float(Qf[i]),tf,float(vect[i]),tipe)
            tc=Variab[0]
            Ac=Variab[1] 
            Err=Variab[2]
            if Err==1:
                return Err
            elif Err==2:
                return Err
            else:
                Err=0
                if i==0:
                    if t[j]<=tc:                            #Segmento velocidad LINEAL trapecio inicio
                        Pos_q1[j]=Qi[i]+(Ac*t[j]**2)/2
                        Vel_q1[j]=Ac*t[j]
                    elif t[j]<=tf-tc:                       #Segmento velocidad CONSTANTE trapecio medio
                        Pos_q1[j]=Qi[i]+Ac*tc*(t[j]-tc/2)
                        Vel_q1[j]=Ac*tc
                    else:                                   #Segmento velocidad LINEAL trapecio final
                        Pos_q1[j]=Qf[i]-(Ac*(tf-t[j])**(2))/2  
                        Vel_q1[j]=Ac*(tf-t[j])
                if i==1:
                    if t[j]<=tc:                            #Segmento velocidad LINEAL trapecio inicio
                        Pos_q2[j]=Qi[i]+(Ac*t[j]**2)/2
                        Vel_q2[j]=Ac*t[j]
                    elif t[j]<=tf-tc:                       #Segmento velocidad CONSTANTE trapecio medio
                        Pos_q2[j]=Qi[i]+Ac*tc*(t[j]-tc/2)
                        Vel_q2[j]=Ac*tc
                    else:                                   #Segmento velocidad LINEAL trapecio final
                        Pos_q2[j]=Qf[i]-(Ac*(tf-t[j])**(2))/2  
                        Vel_q2[j]=Ac*(tf-t[j])
                if i==2:
                    if t[j]<=tc:                            #Segmento velocidad LINEAL trapecio inicio
                        Pos_q3[j]=Qi[i]+(Ac*t[j]**2)/2
                        Vel_q3[j]=Ac*t[j]
                    elif t[j]<=tf-tc:                       #Segmento velocidad CONSTANTE trapecio medio
                        Pos_q3[j]=Qi[i]+Ac*tc*(t[j]-tc/2)
                        Vel_q3[j]=Ac*tc
                    else:                                   #Segmento velocidad LINEAL trapecio final
                        Pos_q3[j]=Qf[i]-(Ac*(tf-t[j])**(2))/2  
                        Vel_q3[j]=Ac*(tf-t[j])   
    return Err,Pos_q1,Pos_q2,Pos_q3,Vel_q1,Vel_q2,Vel_q3

def Constantes_Trape(Qi,Qf,tf,Vect,tipe): #Encontrar las constantes "tc y Ac" para el Perfil Trapezoidal
    if tipe==1: #Si Es Perfil Trapezoidal Tipo I
        Vc=Vect
        cond=abs(Qf-Qi)/tf
        print (cond)
        if (2*cond>=Vc) & (Vc>cond):
            Vc=Fn.Signo(Qf-Qi)*Vc
            tc=(Qi-Qf+(Vc*tf))/Vc
            Ac=Vc/tc
            Error=0            
        else:
            tc=0
            Ac=0
            Error=1            
        Variables=[tc,Ac,Error]        
    else: #Si Es Perfil Trapezoidal Tipo II
        Ac=Vect
        cond=4*abs(Qf-Qi)/tf**(2)
        #print (cond)
        if Ac>cond:
            Ac=Fn.Signo(Qf-Qi)*Ac
            tc=(tf/2)-(0.5*(np.sqrt(((tf**(2)*Ac)-(4*(Qf-Qi)))/Ac)))
            Error=0 
        else:
            tc=0
            Ac=0
            Error=2
        Variables=[tc,Ac,Error]
    return Variables

def Constantes_Cuadra(tf,Qf,Qi): #Encontrar las constantes "a" de la funcion cuadratica
    #Parte de reposo y termina en reposo: ti=0
    Vi=0
    Vf=0
    
    a=np.array([0,0,0,0],float)
    a3=symbols('a3')  
    a2=symbols('a2')

    '''Con las siguientes 3 ecuaciones
    Q =      a3*t^3 + a2*t^2 + a1*t + a0   (Posición de Juntura)
    Q.= V =  3*a3*t^2 + 2*a2*t + a1        (Velocidad de Juntura)
    Q..= α = 6*a3*t + a2                   (Aceleración de Juntura)
    Calcular los valores de las "a"
    '''
    #Para t=ti: Se pueden calcular a0 y a1 de la ecuación "Q" y "Q."
    a0 = Qi
    a1 = Vi
    a[0]=a0
    a[1]=a1
    cont=2

    #Para t=tf: Se pueden calcular a2 y a3 de la ecuación "Q" y "Q."
    t = tf

    #Se utilizan variables auxiliares para realizar calculos simbolicos
    aux1 = a3*t**3 + a2*t**2 + a[1]*t + a[0] - Qf 
    aux2 = 3*a3*t**2 + 2*a2*t + a[1] - Vf   

    aux3 = solve([aux1,aux2],a2,a3) #Se solucionan en terminos de a2 y a3

    for data in aux3.values():#Ciclo para extraer los valores de a2 y a3 del "Diccionario aux3"
        a[cont]=float(data)
        cont+=1

    Const_as=np.array([a[0],a[1],a[2],a[3]],float)
    return Const_as

def IK_Scara_P3R(P_X, P_Y, P_Z): #Cinematica Inversa Scara (PR3)
    #Distacias en x
    a_1=float(47.3)
    a_2=float(149.1)
    a_3=float(148.8)

    Ca=P_X-a_1    #Cateto Adyacente del triangulo formado en X-Y'
    Co=P_Y       #Cateto Opuesto del triangulo formado en X-Y'
    c=np.sqrt(float(Ca)**2+float(Co)**2) 
    alpha=mt.atan2(Co,Ca)
    beta=mt.acos((a_2**(2)+c**(2)-a_3**(2))/(2*a_2*c))
    #Codo abajo
    theta_3ab=mt.acos((c**(2)-a_2**(2)-a_3**(2))/(2*a_2*a_3))   #Variable De Juntura T3
    theta_2ab=(alpha-beta)                                      #Variable De Juntura T2
    #Codo ariba
    theta_3ar=-mt.acos((c**(2)-a_2**(2)-a_3**(2))/(2*a_2*a_3))  #Variable De Juntura T3
    theta_2ar=(alpha+beta)                                      #Variable De Juntura T2
    d_1=P_Z                                                     #Variable De Juntura d1

    if (((theta_3ab)>mt.pi/2) or ((theta_2ab)>mt.pi/2)) or (((theta_3ab)<-mt.pi/2) or ((theta_2ab)<-mt.pi/2)):
        indab=1    
    else:
        indab=0

    if (((theta_3ar)>mt.pi/2) or ((theta_2ar)>mt.pi/2)) or (((theta_3ar)<-mt.pi/2) or ((theta_2ar)<-mt.pi/2)):
        indar=1    
    else:
        indar=0

    IK_FINAL=np.array([d_1, theta_2ab*180/mt.pi, theta_3ab*180/mt.pi,  theta_2ar*180/mt.pi, theta_3ar*180/mt.pi, indar,indab],float)
    return IK_FINAL

def IK_Antropo_3R(P_X, P_Y, P_Z): #Cinematica Inversa Antropomórfico (R3)
    #Distacias en x
    a_1=float(14.5)
    a_2=float(67.5)
    a_3=float(88.28)
    d_1=float(62.87)

    r=np.sqrt(float(P_X)**2+float(P_Y)**2)#Hipotenusa del triangulo generado desde origen al punto W en el plano XY
    Ca=r-a_1#Cateto adyacente, considerando la distancia a1 entre juntura 1-2
    Co=float(P_Z)-d_1#Cateto opuesto, considerando la distancia d1 entre juntura 1-2
    alpha=mt.atan2(Co,Ca)#Calculo Alfa (Para Teorema Del Coseno)
    h=np.sqrt(float(Ca)**2+float(Co)**2)

    theta_1=mt.atan2(P_Y,P_X)     #Variable De Juntura T1

    #Codo Abajo
    #Despejando del Teorema del coseno
    theta_3ab=mt.acos((h**2-a_2**2-a_3**2)/(2*a_2*a_3)) #Variable De Juntura T3
    Ca2=a_2+a_3*mt.cos(theta_3ab)                       #Cateto adyacente
    Co2=a_3*mt.sin(theta_3ab)                           #Cateto opuesto
    beta_ab=mt.atan2(Co2,Ca2)                           #Calculo Beta
    theta_2ab=alpha-beta_ab                             #Variable De Juntura T2
    
    #Codo ariba
    #Despejando del Teorema del coseno
    theta_3ar=-mt.acos((h**2-a_2**2-a_3**2)/(2*a_2*a_3))  #Variable De Juntura T3 
    Ca2=a_2+a_3*mt.cos(theta_3ab)                         #Cateto adyacente
    Co2=a_3*mt.sin(theta_3ab)                             #Cateto opuesto
    beta_ar=mt.atan2(Co2,Ca2)                             #Calculo Beta     
    theta_2ar=(alpha+beta_ar)                             #Variable De Juntura T2

    if (((theta_3ab)>mt.pi) or ((theta_2ab)>mt.pi) or ((theta_1)>mt.pi)) or (((theta_3ab)<-mt.pi) or ((theta_2ab)<-mt.pi) or ((theta_1)<-mt.pi)):
        indab=1    
    else:
        indab=0

    if (((theta_3ar)>mt.pi/2) or ((theta_2ar)>mt.pi/2) or ((theta_1)>mt.pi)) or (((theta_3ar)<-mt.pi) or ((theta_2ar)<-mt.pi) or ((theta_1)<-mt.pi)):
        indar=1    
    else:
        indar=0
    
    IK_FINAL=np.array([theta_1*180/mt.pi, theta_2ab*180/mt.pi , theta_3ab*180/mt.pi, theta_2ar*180/mt.pi , theta_3ar*180/mt.pi,indar,indab],float)    
    return IK_FINAL

def limites (X,ID): #Ecuaciones Para Limites Mecánicos Scara
    if (ID==1):
            yext1=mt.sqrt((float(327.9))**2-(float(X)-float(47.3))**2) 
            return yext1
    elif (ID==2):    
            yint1=mt.sqrt((float(190.5945))**2-(float(X)-float(47.3))**2)    #Cuando X<Xmedio
            return yint1
    elif (ID==3):
            yext2=mt.sqrt((float(178.8))**2-(float(X)-float(47.3))**2)+float(149.1)  #Cuando X<centro
            return yext2
    elif (ID==4):
            yint2=-mt.sqrt((float(30))**2-(float(X)+float(101.5))**2)+float(149.1)  #Cuando X<Xmin
            return yint2

def varX_scara(PosX): #Funcion Para Redefinir Los Valores De Los Sliders (Cinematica Inversa)
    ValX=float(PosX)
    centro=float(47.3)
    Xmin=float(-101.5)
    Xmax=float(345.2)
    Xmedio=float(190.5945)    
    if ValX>=Xmax:
        yinf=0
        ysup=0
        neg=0
    elif ValX>Xmedio:
        ysup=limites(ValX,1)
        yinf=-limites(ValX,1)  
        neg=0
    elif (ValX>=centro and ValX<Xmedio):
        ysup=limites(ValX,1)
        yinf=limites(ValX,2)
        neg=1
    elif (ValX<centro and ValX>Xmin):
        ysup=limites(ValX,3)
        yinf=limites(ValX,2)
        neg=1
    elif (ValX<=Xmin):
        ysup=limites(ValX,3)
        yinf=limites(ValX,4)
        neg=1
    else: 
        print ("No es posible el punto")
    return ysup,yinf,neg    

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

def M1(n,d1,t2,t3): #Definicion Parametros Scara (PR3)
    matrices=[]
    z=[0, t2, t3]
    d=[d1,0,0]
    x=[0,0,0] 
    a=[47.3,149.1,148.8]     
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

def M2(n,j1,j2,j3): #Definicion Parametros Antropomórfico (R6)
    matrices=[]
    z=[j1, j2, j3]
    d=[62.87,0,0]
    x=[mt.pi/2,0,0] 
    a=[14.5,67.5,88.28]         
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

def M3(n,j1,j2,j3,j4,j5,j6): #Definicion Parametros Antropomórfico (R6)
    matrices=[]
    z=[j1, j2, j3, j4, j5, j6]
    d=[115, 30, -20, 245, -57, 235]
    x=[-mt.pi/2, 0, mt.pi/2, mt.pi/2, -mt.pi/2, 0] 
    a=[0, 280, 0, 0, 0, 0]         
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

def Vec(c_ob,matriz_ob): #Funcion Para Extraer Columna Deseada (c_ob)
    P = []
    i_f=0
    while i_f < 3:
        P.append(matriz_ob[i_f][c_ob])
        i_f+= 1
    return P

def R_list(Pi,Pf): #Funcion Para Restar Listas
    resta=list(map(lambda x,y: x-y ,Pi,Pf))
    return resta
    
def JG_S(n,d1,t2,t3,t4): #Jacobiano Para Scara (PR3)
    Z0=[0,0,1]
    P0=[0,0,0]
    DK=M1(n,d1,t2,t3,t4)
    Tm_1=np.dot(DK[1][0],DK[1][1])
    Tm_2=np.dot(Tm_1,DK[1][2])
    P1=Vec(3,DK[1][0])
    P2=Vec(3,Tm_1)
    P3=Vec(3,Tm_2)
    Pe=Vec(3,DK[0])
    Z1=Vec(2,DK[1][0])
    Z2=Vec(2,Tm_1)
    Z3=Vec(2,Tm_2)    
    JG=[[Z0,np.cross(Z1,R_list(Pe,P1)),np.cross(Z2,R_list(Pe,P2)),np.cross(Z3,R_list(Pe,P3))],[[0,0,0],Z1,Z2,Z3]]
    return JG

def JG_A(n,j1,j2,j3): #Jacobiano Para Antropomórfico (R3)
    Z0=[0,0,1]
    P0=[0,0,0]
    DK=M2(n,j1,j2,j3)
    Tm_1=np.dot(DK[1][0],DK[1][1])
    P1=Vec(3,DK[1][0])
    P2=Vec(3,Tm_1)
    Pe=Vec(3,DK[0])
    Z1=Vec(2,DK[1][0])
    Z2=Vec(2,Tm_1)    
    JG=[[np.cross(Z0,R_list(Pe,P0)),np.cross(Z1,R_list(Pe,P1)),np.cross(Z2,R_list(Pe,P2))],[Z0,Z1,Z2]] 
    return JG

def JG_R(): #Jacobiano Para Antropomórfico (R6)
    JR=[[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1]]
    return JR
