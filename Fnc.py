import math as mt
import numpy as np

def IK_Scara_P3R(P_X, P_Y, P_Z, phi):

    #Distacias en x
    a_1=float(47.3);
    a_2=float(149.1);
    a_3=float(148.8);
    a_4=float(30);

    EFx=mt.cos(phi*mt.pi/180)*a_4;
    EFy=mt.sin(phi*mt.pi/180)*a_4; #Distancia en "y" entre punto W y Join4
    Ca=P_X-EFx-a_1;    #Cateto Adyacente del triangulo formado en X-Y'
    Co=P_Y-EFy;        #Cateto Opuesto del triangulo formado en X-Y'
    c=np.sqrt(float(Ca)**2+float(Co)**2) 
    alpha=mt.atan2(Co,Ca);
    beta=mt.acos((a_2**(2)+c**(2)-a_3**(2))/(2*a_2*c));
    #Codo abajo
    theta_3ab=mt.acos((c**(2)-a_2**(2)-a_3**(2))/(2*a_2*a_3))
    theta_2ab=(alpha-beta)
    theta_4ab=(phi-(theta_2ab*180/mt.pi)-(theta_3ab*180/mt.pi))
    #Codo ariba
    theta_3ar=-mt.acos((c**(2)-a_2**(2)-a_3**(2))/(2*a_2*a_3))
    theta_2ar=(alpha+beta)
    theta_4ar=(phi-(theta_2ar*180/mt.pi)-(theta_3ar*180/mt.pi))

    d_1=P_Z

    '''se envia a m1(4,d_1,theta_2,theta_3, theta_4)'''
    IK_FINAL=np.array([d_1, theta_2ab*180/mt.pi, theta_3ab*180/mt.pi, theta_4ab,  theta_2ar*180/mt.pi,theta_3ar*180/mt.pi, theta_4ar],float)
    return IK_FINAL
#print(IK_Scara_P3R(17,26,120,34))

def IK_Antropo_3R(P_X, P_Y, P_Z):

    #Distacias en x
    a_1=float(14.5);
    a_2=float(67.5);
    a_3=float(88.28);
    d_1=float(62.87);

    r=np.sqrt(float(P_X)**2+float(P_Y)**2);#Hipotenusa del triangulo generado desde origen al punto W en el plano XY
    Ca=r-a_1;#Cateto adyacente, considerando la distancia a1 entre juntura 1-2
    Co=P_Z-d_1;#Cateto opuesto, considerando la distancia d1 entre juntura 1-2
    h=np.sqrt(float(Ca)**2+float(Co)**2)

    cost3=(h**2-a_2**2-a_3**2)/(2*a_2*a_3) #Despejando del Teorema del coseno
    sent3=np.sqrt(1-cost3**2); #Propiedad trigonometrica sen^2+cos^2=1
    theta_3=mt.atan2(sent3,cost3) #Calcularlo por medio de tangente (para todos posibles valores)

    alpha=mt.atan2(Co,Ca);

    Ca2=a_2+a_3*mt.cos(theta_3);#Cateto adyacente
    Co2=a_3*mt.sin(theta_3);#Cateto opuesto
    beta=mt.atan2(Co2,Ca2);
    theta_2=alpha-beta

    theta_1=mt.atan2(P_Y,P_X)

    '''se envia a m1(4,d_1,theta_2,theta_3, theta_4)'''
    IK_FINAL=np.array([theta_1*180/mt.pi, theta_2*180/mt.pi , theta_3*180/mt.pi,theta_1*180/mt.pi, theta_2*180/mt.pi , theta_3*180/mt.pi],float)
    #IK_FINAL=np.array([d_1, theta_2ab*180/mt.pi, theta_3ab*180/mt.pi, theta_4ab,  theta_2ar*180/mt.pi,theta_3ar*180/mt.pi, theta_4ar],float)
    return IK_FINAL
#print(IK_Antropo_3R(36,50,20))