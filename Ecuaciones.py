import numpy as np
import math as mt
from sympy import *

################### Cinemática Directa #################

def Parametros(n, q1, q2, q3, q4, q5, q6): #Definicion Parametros Robots
    Matrices=[]
    if n == 1:
        #Scara
        z=[0, q2, q3]
        d=[q1, 0, 0]
        x=[0, 0, 0] 
        a=[47.3, 149.1, 148.8]
        Eslabones=3     
    elif n == 2:
        #Antropomórfico R3
        z=[q1, q2, q3]
        d=[95.91, 0, 0]
        x=[mt.pi/2, 0, 0] 
        a=[0, 66.76, 130.45]         
        Eslabones=3
    else: 
        #Antropomórfico R6
        z=[q1, q2, q3, q4, q5, q6]
        d=[115, 30, -20, 245, -57, 235]
        x=[-mt.pi/2, 0, mt.pi/2, mt.pi/2, -mt.pi/2, 0] 
        a=[0, 280, 0, 0, 0, 0]    
        Eslabones=6
    for i in range (0, Eslabones):
        Matrices.append(Matrices_Homo((z[i]*mt.pi/180), d[i], x[i], a[i]))
    Final=Calculo_Directa(Matrices, Eslabones)
    return Final, Matrices

def Matrices_Homo(angz, dz, angx, ax): #Matriz Homogenea DH
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
    Homo=np.array([[r11, r12, r13, r14], [r21, r22, r23, r24], [r31, r32, r33, r34], [r41, r42, r43, r44]], float)
    return Homo

def Calculo_Directa(matrices_DH, n): #Calculo de matriz Cinemática Directa
    MatrizFinal=np.eye(4)
    for j in range (0, n):
        MatrizFinal=np.dot(MatrizFinal, matrices_DH[j]) 
        MatrizFinal=np.round(MatrizFinal, decimals=5)    
    return MatrizFinal

################### Cinemática Inversa #################

def Calculo_Inversa(n, P_X, P_Y, P_Z): #Calculo Cinemática Inversa
    if n==1:
        a_1=float(47.3)
        a_2=float(149.1)
        a_3=float(148.8)
        Ca=P_X-a_1    #Cateto Adyacente del triangulo formado en X-Y'
        Co=P_Y        #Cateto Opuesto del triangulo formado en X-Y'
        q_1=P_Z       #Variable De Juntura d1
        Rob='S'
    elif n==2:
        d_1=float(95.91)
        a_2=float(66.76)
        a_3=float(130.45)
        r=np.sqrt(float(P_X)**2+float(P_Y)**2) #Hipotenusa del triangulo generado desde origen al punto W en el plano XY
        Ca=r                                   #Cateto adyacente
        Co=float(P_Z)-d_1                      #Cateto opuesto, considerando la distancia d1 entre juntura 1-2
        q_1=mt.atan2(P_Y,P_X)*180/mt.pi        #Variable De Juntura T1
        Rob='A'
    
    h=np.sqrt(float(Ca)**2+float(Co)**2)
    alpha=mt.atan2(Co,Ca)
    beta=mt.acos((a_2**(2)+h**(2)-a_3**(2))/(2*a_2*h))

    #Codo arriba
    q_3ar=-mt.acos((h**(2)-a_2**(2)-a_3**(2))/(2*a_2*a_3))  #Variable De Juntura T3
    q_2ar=(alpha+beta)                                      #Variable De Juntura T2
    #Codo abajo
    q_3ab=mt.acos((h**(2)-a_2**(2)-a_3**(2))/(2*a_2*a_3))   #Variable De Juntura T3 
    q_2ab=(alpha-beta)                                      #Variable De Juntura T2
    
    Banderas=Limites_Junturas([q_1, q_2ar, q_3ar,  q_2ab, q_3ab], Rob)
    Qs_IK=np.array([q_1, q_2ab*180/mt.pi, q_3ab*180/mt.pi,  q_2ar*180/mt.pi, q_3ar*180/mt.pi, Banderas[0], Banderas[1]], float)
    return Qs_IK

def Limites_Junturas(Qs, Robot): #Establecer Si Los Limites Mecanicos De Junturas Son Superados
    if Robot == 'S':
        lim_1=221
        lim_2=mt.pi/2
        lim_3=mt.pi/2
    elif Robot == 'A':
        Qs[1]=Qs[1]-mt.pi/2
        Qs[3]=Qs[3]-mt.pi/2       
        lim_1=180
        lim_2=mt.pi/2
        lim_3=mt.pi/2

    if ((Qs[0] > lim_1) or (Qs[0] < -lim_1)) or ((Qs[1] > lim_2) or (Qs[1] < -lim_2)) or ((Qs[2] > lim_3) or (Qs[2] < -lim_3)):
        IndU=True
    else:
        IndU=False

    if ((Qs[0] > lim_1) or (Qs[0] < -lim_1)) or ((Qs[3] > lim_2) or (Qs[3] < -lim_2)) or ((Qs[4] > lim_3) or (Qs[4] < -lim_3)):
        IndD=True    
    else:
        IndD=False
    return IndU, IndD

def Ecua_Lim_S (X, ID): #Ecuaciones Para Limites Mecánicos Scara
    if (ID == 1):
            yext1=mt.sqrt((float(297.9))**2-(float(X)-float(47.3))**2)              #Cuando X>Xmedio     
            return yext1
    elif (ID == 2):    
            yint=mt.sqrt((float(210.65))**2-(float(X)-float(47.3))**2)              #Cuando Centro<=X<Xmedio
            return yint
    elif (ID == 3):
            yext2=mt.sqrt((float(148.8))**2-(float(X)-float(47.3))**2)+float(149.1) #Cuando Xmin<X<Centro
            return yext2

def Limites_Y_S(PosX): #Define Los Limites Del Slider "Py_S" Del Robot Scara
    ValX=float(PosX)
    centro=float(47.3)
    Xmin=float(-101.5)
    Xmax=float(345.2)
    Xmedio=float(257.95)    
    if ValX >= Xmax:
        yinf=0
        ysup=0
        neg=0
    elif ValX > Xmedio:
        ysup=Ecua_Lim_S(ValX, 1)
        yinf=-Ecua_Lim_S(ValX, 1)  
        neg=0
    elif (ValX >= centro and ValX < Xmedio):
        ysup=Ecua_Lim_S(ValX, 1)
        yinf=Ecua_Lim_S(ValX, 2)
        neg=1
    elif (ValX < centro and ValX > Xmin):
        ysup=Ecua_Lim_S(ValX, 3)
        yinf=Ecua_Lim_S(ValX, 2)
        neg=1
    else: 
        ysup=float(149.1)
        yinf=float(149.1)
        neg=1
    return yinf, ysup, neg    

def Ecua_Lim_A (X, Y, ID): #Ecuaciones Para Limites Mecánicos Antropomórfico
    Zmin=-float(34.64)
    if (ID == 1):
        zext=mt.floor(mt.sqrt(float(197.21)**2-float(X)**2-float(Y)**2)+float(95.91))
        zext2=mt.ceil(-mt.sqrt(float(197.21)**2-float(X)**2-float(Y)**2)+float(95.91))                
        if zext2 < Zmin:
            zext2 = Zmin                            
        return zext, zext2                          
    elif (ID == 2):    #Cuando X<Xborde ó X>-Xborde
        zint=mt.floor(mt.sqrt(float(146.63)**2-float(X)**2-float(Y)**2)+float(95.91))                   
        zint2=mt.ceil(-mt.sqrt(float(146.63)**2-float(X)**2-float(Y)**2)+float(95.91))                
        if zint2 < Zmin:
            zint2=Zmin                            
        return zint, zint2        

def Limites_Y_A(PosX): #Define Los Limites Del Slider "Py_A" Del Robot Antropomórfico
    ValX=float(PosX)
    ysup=mt.floor(mt.sqrt((197.21)**2-(ValX**2)))
    yinf=mt.ceil(-mt.sqrt((197.21)**2-(ValX**2)))    
    return ysup, yinf  

def Limites_Z_A(PosX, PosY): #Define Los Limites Del Slider "Pz_A" Del Robot Antropomórfico
    ValX=float(PosX)       
    ValY=float(PosY) 
    Lim_Interior=float(146.63)
    Ubi=mt.sqrt((PosX)**2+(PosY)**2)
    if (Ubi > Lim_Interior):
        zlim=Ecua_Lim_A(ValX, ValY, 1)
        zsup=zlim[0] 
        zinf=zlim[1]                                                                                                                                                                                                                        
        inf=0
    elif (Ubi < Lim_Interior):
        zlimext=Ecua_Lim_A(ValX, ValY, 1)  
        zlimint=Ecua_Lim_A(ValX, ValY, 2)
        zsup=[zlimext[0],zlimint[0]]
        zinf=[zlimint[1],zlimext[1]]
        inf=1
    else: 
        print ("No es posible el punto")
    return zsup, zinf, inf

################### Calculo Jacobianos #################

def Vec(Tipo, Col_Des, Fila_Des, Referencia): #Funcion Para Extraer Columna Deseada (Col_Des)
    if Tipo == 'C':
        Colum = []
        for i in range (0, 3):
            Colum.append(Referencia[i][Col_Des])
        return Colum
    elif Tipo == 'M':
        Matriz = []
        for i in range (0, Fila_Des):
            for j in range (0, Col_Des):
                Matriz.append(Referencia[i][j])
        return Matriz

def R_list(Pi, Pf): #Funcion Para Restar Listas
    resta=list(map(lambda x,y: x-y ,Pi,Pf))
    return resta    

def Jacobianos(n, q1, q2, q3): #Calculo Para Jacobianos Scara y Antropomórfico R3
    ##### Proceso Para Jacobiano Geometrico #####
    z0=[0, 0, 1]
    p0=[0, 0, 0]
    Cine_DK=Parametros(n, q1, q2, q3, None, None, None)
    Tm_1=np.dot(Cine_DK[1][0], Cine_DK[1][1])
    p1=Vec('C', 3, None, Cine_DK[1][0])    
    p2=Vec('C', 3, None, Tm_1)
    pe=Vec('C', 3, None, Cine_DK[0])    
    z1=Vec('C', 2, None, Cine_DK[1][0])
    z2=Vec('C', 2, None, Tm_1)

    ##### Proceso Para Jacobiano Analitico #####
    t1=symbols('t1')
    t2=symbols('t2')
    t3=symbols('t3')

    if n == 1:   
        r11=cos(t2+t3)
        r12=-sin(t2+t3)
        r13=0
        r23=0
        r33=1        
    elif n == 2:
        r12=-sin(t2+t3)*cos(t1)
        r11=cos(t2+t3)*cos(t1)
        r13=sin(t1)
        r23=-cos(t1)
        r33=0

    gamma=atan2(-r23,r33)        
    alpha=atan2(-r12, r11)
    beta=atan2(r13,sqrt(r12**2+r11**2))

    X = Matrix([gamma, alpha, beta])
    Y = Matrix([t1, t2, t3])

    Jaco_A_O=str(X.jacobian(Y))

    to_grad=mt.pi/180 
    
    if n == 1:
        t1=q1
    elif n == 2:
        t1=q1*to_grad        
    t2=q2*to_grad
    t3=q3*to_grad
    
    Jaco_A_O=eval(Jaco_A_O)

    if n == 1:   
        jaco_Geo=[[z0, np.cross(z1, R_list(pe, p1)), np.cross(z2, R_list(pe, p2))], [[0, 0, 0], z1, z2]]
        jaco_Ana=[[z0, np.cross(z1, R_list(pe, p1)), np.cross(z2, R_list(pe, p2))], matrix2numpy(Transpose(Jaco_A_O))]
    elif n == 2:
        jaco_Geo=[[np.cross(z0, R_list(pe, p0)), np.cross(z1, R_list(pe, p1)), np.cross(z2, R_list(pe, p2))], [z0, z1, z2]]
        jaco_Ana=[[np.cross(z0, R_list(pe, p0)), np.cross(z1, R_list(pe, p1)), np.cross(z2, R_list(pe, p2))], matrix2numpy(Transpose(Jaco_A_O))]
    return jaco_Geo, jaco_Ana

################### Planeación De Trayectorias ###################

def Perf_Cuadra(tf, n, Qi, Qf): #Encontrar Las Posiciones y Velocidades De Juntura Utilizando El Perfil Cuadratrico
    #Se recalcula un valor para "t" dependiendo la cantidad de puntos deseados (resolución)
    t = np.arange(0, tf+((tf)/(n-1)), (tf)/(n-1), dtype=float) 
    Err=0
    for i in range(0, 3): #Ciclo de 3 para crear los vectores de las 3 junturas     
        #Calculo de las constantes "a". (1 Vez para cada juntura)   
        Cons_a=Constantes_Cuadra(float(tf), float(Qf[i]), float(Qi[i]))  
        if i==0:
            Pos_q1= Cons_a[3]*t**(3) + Cons_a[2]*t**(2) + Cons_a[1]*t + Cons_a[0]  #Vector de Posición Juntura 1 (d1=Desplazamiento Base)                                   
            Vel_q1 = 3*Cons_a[3]*t**(2) + 2*Cons_a[2]*t + Cons_a[1]              #Vector de Velocidad Juntura 1 (d1=Desplazamiento Base)    
        if i==1:
            Pos_q2 = Cons_a[3]*t**(3) + Cons_a[2]*t**(2) + Cons_a[1]*t + Cons_a[0] #Vector de Posición Juntura 2 (t2=Angulo Brazo)
            Vel_q2= 3*Cons_a[3]*t**(2) + 2*Cons_a[2]*t + Cons_a[1]               #Vector de Velocidad Juntura 2 (t2=Angulo Brazo)
        else:
            Pos_q3 = Cons_a[3]*t**(3) + Cons_a[2]*t**(2) + Cons_a[1]*t + Cons_a[0] #Vector de Posición Juntura 3 (t3=Angulo AnteBrazo)
            Vel_q3 = 3*Cons_a[3]*t**(2) + 2*Cons_a[2]*t + Cons_a[1]              #Vector de Velocidad Juntura 3 (t3=Angulo AnteBrazo) 
    
    return Err, Pos_q1, Pos_q2, Pos_q3, Vel_q1, Vel_q2, Vel_q3

def Perf_Trape(tf, n, Qi, Qf, vect, tipe): #Encontrar Las Posiciones y Velocidades De Juntura Utilizando El Perfil Trapezoidal    
    t = np.arange(0, tf+((tf)/(n-1)), (tf)/(n-1), dtype=float) 
    Pos_q1=np.empty(n)
    Pos_q2=np.empty(n)
    Pos_q3=np.empty(n)
    Vel_q1=np.empty(n)
    Vel_q2=np.empty(n)
    Vel_q3=np.empty(n)
    for j in range (0, len(t)):
        for i in range (0, 3):
            Variab=Constantes_Trape(float(Qi[i]), float(Qf[i]), tf, float(vect[i]), tipe)
            tc=Variab[0]
            Ac=Variab[1] 
            Err=Variab[2]
            if Err == 1:
                return Err,Variab[3],i
            elif Err == 2:
                return Err, Variab[3],i
            else:
                Err=0
                if i == 0:
                    if t[j] <= tc:                            #Segmento velocidad LINEAL trapecio inicio
                        Pos_q1[j]=Qi[i]+(Ac*t[j]**2)/2
                        Vel_q1[j]=Ac*t[j]
                    elif t[j] <= tf-tc:                       #Segmento velocidad CONSTANTE trapecio medio
                        Pos_q1[j]=Qi[i]+Ac*tc*(t[j]-tc/2)
                        Vel_q1[j]=Ac*tc
                    else:                                   #Segmento velocidad LINEAL trapecio final
                        Pos_q1[j]=Qf[i]-(Ac*(tf-t[j])**(2))/2  
                        Vel_q1[j]=Ac*(tf-t[j])
                if i == 1:
                    if t[j] <= tc:                            #Segmento velocidad LINEAL trapecio inicio
                        Pos_q2[j]=Qi[i]+(Ac*t[j]**2)/2
                        Vel_q2[j]=Ac*t[j]
                    elif t[j] <= tf-tc:                       #Segmento velocidad CONSTANTE trapecio medio
                        Pos_q2[j]=Qi[i]+Ac*tc*(t[j]-tc/2)
                        Vel_q2[j]=Ac*tc
                    else:                                   #Segmento velocidad LINEAL trapecio final
                        Pos_q2[j]=Qf[i]-(Ac*(tf-t[j])**(2))/2  
                        Vel_q2[j]=Ac*(tf-t[j])
                if i == 2:
                    if t[j] <= tc:                            #Segmento velocidad LINEAL trapecio inicio
                        Pos_q3[j]=Qi[i]+(Ac*t[j]**2)/2
                        Vel_q3[j]=Ac*t[j]
                    elif t[j] <= tf-tc:                       #Segmento velocidad CONSTANTE trapecio medio
                        Pos_q3[j]=Qi[i]+Ac*tc*(t[j]-tc/2)
                        Vel_q3[j]=Ac*tc
                    else:                                   #Segmento velocidad LINEAL trapecio final
                        Pos_q3[j]=Qf[i]-(Ac*(tf-t[j])**(2))/2  
                        Vel_q3[j]=Ac*(tf-t[j])   
    return Err, Pos_q1, Pos_q2, Pos_q3, Vel_q1, Vel_q2, Vel_q3

def Constantes_Trape(Qi, Qf, tf, Vect, tipe): #Encontrar las constantes "tc y Ac" para el Perfil Trapezoidal
    if tipe == 1: #Si Es Perfil Trapezoidal Tipo I
        Vc=Vect
        cond=abs(Qf-Qi)/tf #cond from_ hasta cond*2 to (vel)
        cond_velocidad=cond
        #print (cond)
        if (2*cond >= Vc) & (Vc > cond):
            Vc=Signo(Qf-Qi)*Vc
            tc=(Qi-Qf+(Vc*tf))/Vc
            Ac=Vc/tc
            Error=0            
        else:
            tc=0
            Ac=0
            Error=1            
        Variables=[tc, Ac, Error, cond]        
    else: #Si Es Perfil Trapezoidal Tipo II
        Ac=Vect
        cond=4*abs(Qf-Qi)/tf**(2) #cond from_ hasta cond*4 to (acele) 
        cond_aceleracion=cond
        #print (cond) #vj1 vj2 vj3#
        if Ac > cond:
            Ac=Signo(Qf-Qi)*Ac
            tc=(tf/2)-(0.5*(np.sqrt(((tf**(2)*Ac)-(4*(Qf-Qi)))/Ac)))
            Error=0 
        else:
            tc=0
            Ac=0
            Error=2
        Variables=[tc, Ac, Error, cond]
    return Variables

def Constantes_Cuadra(tf, Qf, Qi): #Encontrar las constantes "a" de la funcion cuadratica
    #Parte de reposo y termina en reposo: ti=0
    Vi=0
    Vf=0
    
    a=np.array([0, 0, 0, 0],float)
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

    aux3 = solve([aux1, aux2], a2, a3) #Se solucionan en terminos de a2 y a3

    for data in aux3.values():#Ciclo para extraer los valores de a2 y a3 del "Diccionario aux3"
        a[cont]=float(data)
        cont+=1

    Const_as=np.array([a[0], a[1], a[2], a[3]], float)
    return Const_as

################### Funciones Adicionales ###################
def Signo(x): #Determina El signo del numero
    if x>=0:
        sgn=1            
    else:
        sgn=-1
    return sgn