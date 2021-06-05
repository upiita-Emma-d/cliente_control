import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
from scipy.interpolate import interp1d
import csv
import matplotlib.pyplot as plt

""" FILTRO"""
def filtro(T_Sucia):
    T_limpia = np.empty((1,), float)
    T1 = T_Sucia[1]
    T2 = T_Sucia[1]
    T3 = T_Sucia[1]
    T4 = T_Sucia[1]
    T5 = T_Sucia[1]
    T6 = T_Sucia[1]
    T7 = T_Sucia[1]
    T8 = T_Sucia[1]
    T9 = T_Sucia[1]
    T  = T_Sucia[1]
    for i in T_Sucia:
        T9 = T8
        T8 = T7
        T7 = T6
        T6 = T5
        T5 = T4
        T4 = T3
        T3 = T2
        T2 = T1
        if (i < T - 5):
            T1 = T1
        else:
            T1 = i
        T = (T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8 + T9 ) / 9
        T_limpia = np.append(T_limpia,T,axis=None)
    return T_limpia


with open('D:/repositorios/python-labview/dato_adquiridos.csv',newline= '') as File:
    reader = csv.reader(File)

    t = np.empty((1,0),float)
    u = np.empty((1,0),float)
    yp= np.empty((1,0),float)
    for i in reader:
        #print(i)
        t = np.append(t,float(i[0]) , axis=None)
        u = np.append(u,float(i[1]) , axis=None)
        yp = np.append(yp,float(i[2]) , axis=None)

yp = filtro(yp)

u0 = u[0]
yp0 = yp[0]

t = t.T - t[0]
u = u.T 
yp = yp.T

#Numero de pasos
ns = len(t)
delta_t = t[1] - t[0]

#Creamo una interpolacion lineal
uf = interp1d(t,u)

def objetive(x):
    #modelo simulado
    ym = sim_model(x)
    # calculando objetivo
    obj = 0.0
    for i in range(len(ym)):
        obj = obj + (ym[i]-yp[i]) ** 2
    return obj

def sim_model(x):
    #Valores de entrada
    k = x[0]
    tau = x[1]
    td = x[2]
    #alamacenamiento de datos
    ym = np.zeros(ns)
    #Condicion inicial
    ym[0] = yp0
    #lazo para cada paso o intervalo discetizado en el tiempo.
    for i in range(0,ns-1):
        ts = [t[i],t[i+1]]
        y1 = odeint(fopdt,ym[i],ts,args=(uf,k,tau,td))
        ym[i+1] = y1[-1]
    return ym

def fopdt(y,t,uf,Km,taum,td):
    try:
        if(t-td)<= 0:
            um = uf(0.0)
        else:
            um = uf(t-td)
    except:
        um = u0
    #calcular la derivada 
    dydt = -(y-yp0)/taum + Km /taum *(um-u0)
    return dydt    
 
 #valores iniciales
x0 = np.zeros(3)
x0[0] = .1 #k
x0[1] = 6   #tau
x0[2] = 0.0 #td

#valor del objetivo inicial
print('ISE:' + str(objetive(x0)))

solution = minimize(objetive,x0)
x = solution.x
# resultados finales
print('ISE final' + str(objetive(x)) )
print('k' + str(x[0]))
print('tau' + str(x[1]))
print('dt' + str(x[2]))

ym1 = sim_model(x0)
ym2 = sim_model(x)

#
plt.figure()
plt.subplot(2,1,1)
plt.plot(t,yp,'ko-', linewidth = 2 ,label = 'Datos de proceso')
plt.plot(t,ym1,'b-', linewidth = 2 ,label = 'Primer valor')
plt.plot(t,ym1,'r--', linewidth = 2 ,label = 'FOPFT optimizado')
plt.ylabel('Salida')
plt.legend(loc = 'best')
plt.show()
