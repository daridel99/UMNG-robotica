import math as mt
from tkinter import StringVar
import numpy as np

def IK_Scara_P3R(P_X, P_Y, P_Z, phi):

    #Distacias en x
    a_1=float(47.3)
    a_2=float(149.1)
    a_3=float(148.8)
    a_4=float(30)

    EFx=mt.cos(phi*mt.pi/180)*a_4
    EFy=mt.sin(phi*mt.pi/180)*a_4 #Distancia en "y" entre punto W y Join4
    Ca=P_X-EFx-a_1    #Cateto Adyacente del triangulo formado en X-Y'
    Co=P_Y-EFy        #Cateto Opuesto del triangulo formado en X-Y'
    c=np.sqrt(float(Ca)**2+float(Co)**2) 
    alpha=mt.atan2(Co,Ca)
    beta=mt.acos((a_2**(2)+c**(2)-a_3**(2))/(2*a_2*c))
    #Codo abajo
    theta_3ab=mt.acos((c**(2)-a_2**(2)-a_3**(2))/(2*a_2*a_3))
    #print(theta_3ab)
    theta_2ab=(alpha-beta)
    theta_4ab=(phi-(theta_2ab*180/mt.pi)-(theta_3ab*180/mt.pi))
    #Codo ariba
    theta_3ar=-mt.acos((c**(2)-a_2**(2)-a_3**(2))/(2*a_2*a_3))
    theta_2ar=(alpha+beta)
    theta_4ar=(phi-(theta_2ar*180/mt.pi)-(theta_3ar*180/mt.pi))

    if (((theta_3ab or theta_3ar)>mt.pi/2) or ((theta_2ar or theta_2ab)>mt.pi/2) or ((theta_4ar or theta_4ab)>90)) or (((theta_3ab or theta_3ar)<-mt.pi/2) or ((theta_2ar or theta_2ab)<-mt.pi/2) or ((theta_4ar or theta_4ab)<-90)):
        ind=1    
    else:
        ind=0

    #print ("Varie el valor de Phi")

    d_1=P_Z

    '''se envia a m1(4,d_1,theta_2,theta_3, theta_4)'''
    IK_FINAL=np.array([d_1, theta_2ab*180/mt.pi, theta_3ab*180/mt.pi, theta_4ab,  theta_2ar*180/mt.pi,theta_3ar*180/mt.pi, theta_4ar,ind],float)
    return IK_FINAL
#print(IK_Scara_P3R(17,26,120,34))

def IK_Antropo_3R(P_X, P_Y, P_Z):

    #Distacias en x
    a_1=float(14.5)
    a_2=float(67.5)
    a_3=float(88.28)
    d_1=float(62.87)

    r=np.sqrt(float(P_X)**2+float(P_Y)**2)#Hipotenusa del triangulo generado desde origen al punto W en el plano XY
    Ca=r-a_1#Cateto adyacente, considerando la distancia a1 entre juntura 1-2
    Co=P_Z-d_1#Cateto opuesto, considerando la distancia d1 entre juntura 1-2
    h=np.sqrt(float(Ca)**2+float(Co)**2)

    cost3=(h**2-a_2**2-a_3**2)/(2*a_2*a_3) #Despejando del Teorema del coseno
    sent3=np.sqrt(1-cost3**2)#Propiedad trigonometrica sen^2+cos^2=1
    theta_3=mt.atan2(sent3,cost3) #Calcularlo por medio de tangente (para todos posibles valores)

    alpha=mt.atan2(Co,Ca)

    Ca2=a_2+a_3*mt.cos(theta_3)#Cateto adyacente
    Co2=a_3*mt.sin(theta_3)#Cateto opuesto
    beta=mt.atan2(Co2,Ca2)
    theta_2=alpha-beta

    theta_1=mt.atan2(P_Y,P_X)

    '''se envia a m1(4,d_1,theta_2,theta_3, theta_4)'''
    IK_FINAL=np.array([theta_1*180/mt.pi, theta_2*180/mt.pi , theta_3*180/mt.pi,theta_1*180/mt.pi, theta_2*180/mt.pi , theta_3*180/mt.pi],float)
    #IK_FINAL=np.array([d_1, theta_2ab*180/mt.pi, theta_3ab*180/mt.pi, theta_4ab,  theta_2ar*180/mt.pi,theta_3ar*180/mt.pi, theta_4ar],float)
    return IK_FINAL
#print(IK_Antropo_3R(36,50,20))

def varX_scara(PosX):
    ValX=float(PosX)
    centro=float(47.3)
    Xmin=float(-101.5)
    Xmax=float(375.2)
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
     
def limites (X,ID):
    match ID:
        case 1:
            yext1=mt.sqrt((float(327.9))**2-(float(X)-float(47.3))**2) 
            return yext1
        case 2:     
            yint1=mt.sqrt((float(190.5945))**2-(float(X)-float(47.3))**2)    #Cuando X<Xmedio
            return yint1
        case 3:
            yext2=mt.sqrt((float(178.8))**2-(float(X)-float(47.3))**2)+float(149.1)  #Cuando X<centro
            return yext2
        case 4:
            yint2=-mt.sqrt((float(30))**2-(float(X)+float(101.5))**2)+float(149.1)  #Cuando X<Xmin
            return yint2


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

def M1(n,d1,t2,t3,t4): #Definicion Parametros Scara (P3R)
    matrices=[]
    z=[0, t2, t3,t4]
    d=[d1,0,0,0]
    x=[0,0,0,0] 
    a=[47.3,149.1,148.8,30]     
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

def M2(n,j1,j2,j3): #Definicion Parametros Antropomorfico (3R)
    matrices=[]
    z=[j1, j2, j3]
    d=[62.87,0,0]
    x=[mt.pi/2,0,0] 
    a=[14.5,67.5,88.28]         
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

def M3(n,j1,j2,j3,j4,j5,j6): #Definicion Parametros Antropomorfico (6R)
    matrices=[]
    z=[j1, j2, j3, j4, j5, j6]
    d=[115, 30, -20, 245, 57, 105]
    x=[-mt.pi/2, 0, -mt.pi/2, -mt.pi/2, mt.pi/2, 0] 
    a=[0, 280, 0, 0, 0, 0]         
    for i in range (0,n):
        matrices.append(matrices_T((z[i]*mt.pi/180),d[i],x[i],a[i]))
    final=calculo(matrices,n)
    return final,matrices

def Vec(c_ob,matriz_ob):
    P = []
    i_f=0
    while i_f < 3:
        P.append(matriz_ob[i_f][c_ob])
        i_f+= 1
    return P

def R_list(Pi,Pf):
    resta=list(map(lambda x,y: x-y ,Pi,Pf))
    return resta
    
def JG_S(n,d1,t2,t3,t4):
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

def JG_A(n,j1,j2,j3):
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
