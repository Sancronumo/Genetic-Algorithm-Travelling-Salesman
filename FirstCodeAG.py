# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 19:57:09 2021

@author: yisus
"""
#librerías
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

#inicialización
cantidadCromosomas=10


#se importan las coordenadas de las ciudades el primer índice es la ciudad
#el segundo las coordenadas
coorCiudades=np.loadtxt('ciudades.txt')

cantidadCiudades=len(coorCiudades)
#cantidadCiudades=4

probmut=1/cantidadCiudades
#probmut=1
'''
Funciones
'''


def CrearCromosomas(cantidadCromosomas, cantidadCiudades):
    '''
    Crea una lista de Cromosomas 

    Parameters
    ----------
    cantidadCromosomas : int
        Cantidad de cromosomas a crear
    cantidadCiudades : int
        Cantidad de ciudades, la longitud del cromosoma depende de 
        este parámetro

    Returns
    -------
    listaCromosomas : Array
        Matriz con los cromosomas creados

    '''
    listaCromosomas=[]
    for icromos in range(0, cantidadCromosomas):
        cromosoma=[]
        for igen in range(0, cantidadCiudades):
            nextGen=np.random.randint(0, cantidadCiudades)
            while nextGen in cromosoma:
                nextGen=np.random.randint(0, cantidadCiudades)
            cromosoma.append(nextGen)
        '''    
        Esto no es del todo necesario, es para que no se repitan los cromosomas
        '''
        while cromosoma in listaCromosomas:
            cromosoma=[]
            for igen in range(0, cantidadCiudades):
                nextGen=np.random.randint(0, cantidadCiudades)
                while nextGen in cromosoma:
                    nextGen=np.random.randint(0, cantidadCiudades)
                cromosoma.append(nextGen)
                
        listaCromosomas.append(cromosoma)
    return listaCromosomas

def ObtenerValAjuste(cromosoma,coorCiudades):
    '''
    Obtiene el valor de ajuste de un cromosoma obteniendo
    la longitud del camino y sacando su inversa

    Parameters
    ----------
    cromosoma : cromosoma que se desea obtener valor de ajuste vector con index de ciudades
    coorCiudades : matriz con coordendas de ciudades

    Returns
    -------
    TYPE
       doble inversa de la longitud del camino seguido

    '''
    ValAjuste=0
    for i in range(len(cromosoma)):
        if cromosoma[i]==cromosoma[-1]:
            ciuIni=cromosoma[i]
            ciuFin=cromosoma[0]
            ValAjuste+=((coorCiudades[ciuFin][0]-coorCiudades[ciuIni][0])**2+(coorCiudades[ciuFin][1]-coorCiudades[ciuIni][1])**2)**(1/2)
        else:
            ciuIni=cromosoma[i]
            ciuFin=cromosoma[i+1]
            ValAjuste+=((coorCiudades[ciuFin][0]-coorCiudades[ciuIni][0])**2+(coorCiudades[ciuFin][1]-coorCiudades[ciuIni][1])**2)**(1/2)
    return 1/ValAjuste
def CalcularAjustes(listaCromosomas,coorCiudades):
    '''
    Una generalización de la función ObtenerValAjuste que aplica esta función a 
    una lista de cromosomas

    Parameters
    ----------
    listaCromosomas : Array
        Matriz con los cromosomas
    coorCiudades : Array
        Matriz con las coordenadas de las ciudades

    Returns
    -------
    listaAjustes : Array
        Vector con los valores de ajustes

    '''
    listaAjustes=[]
    for indexCrom in range(len(listaCromosomas)):
        listaAjustes.append(ObtenerValAjuste(listaCromosomas[indexCrom],coorCiudades))
    return listaAjustes
    

def MutarCromosomas(listaCromosomas, excepcion=-1):
    '''
    Aplica una mutación a los cromosomas con una probabilidad probmut definido
    arriba como variable global

    Parameters
    ----------
    listaCromosomas : Array
        Matriz con los vectores de los cromosomas en cada columna
    excepcion: int
        cromosoma que no se quiere alterar porque es el mejor

    Returns
    -------
    listaCromosomas : Array
        Matriz original de cromosomas pero modificados

    '''
    for indexcrom in range(len(listaCromosomas)):
        if np.random.random()<probmut and indexcrom!=excepcion:
            gen1=np.random.randint(0,len(listaCromosomas[indexcrom]))
            gen2=np.random.randint(0,len(listaCromosomas[indexcrom]))
            while gen2==gen1:
                gen2=np.random.randint(0,len(listaCromosomas[indexcrom]))
            gentrans=listaCromosomas[indexcrom][gen2]
            listaCromosomas[indexcrom][gen2]=listaCromosomas[indexcrom][gen1]
            listaCromosomas[indexcrom][gen1]=gentrans
    return listaCromosomas
 
'''
Código Principal
'''
#Variables
cantidadIteraciones=10000
           
listaCromosomas=CrearCromosomas(cantidadCromosomas, cantidadCiudades)
Iteraciones=[]
valoresMinimos=[]
valoresPromedioAjuste=[]
valoresMaximosAjuste=[]
#Código
for i in range(cantidadIteraciones):
    listaAjustes=CalcularAjustes(listaCromosomas, coorCiudades)
    Maximo=listaAjustes.index(max(listaAjustes))
    Iteraciones.append(i)
    valoresMinimos.append(1/listaAjustes[Maximo])
    valoresMaximosAjuste.append(listaAjustes[Maximo])
    valoresPromedioAjuste.append(np.sum(listaAjustes)/len(listaAjustes))
    listaCromosomas=MutarCromosomas(listaCromosomas,Maximo)
caminoMinimo=listaCromosomas[Maximo]
caminoMinCoor=[]
for i in caminoMinimo:
    caminoMinCoor.append(coorCiudades[i])

#Gráfico
fig, ax =plt.subplots()
ax.plot(Iteraciones,valoresMinimos) 
ax.set_xlabel('Iteraciones')
ax.set_ylabel('Longitud Mínima')
ax.set_title('Graf 1. Longitud Mínima vs Cantidad de Iteraciones')

#Gráfico de ciudades
for i in range(1,len(caminoMinCoor)):
    a=caminoMinCoor[:i]
    fig, ax = plt.subplots()
    path=Path(a)
    patch=patches.PathPatch(path,facecolor='none', lw=2)
    ax.add_patch(patch)
    ax.set_xlim(0,20)
    ax.set_ylim(0,20)
    plt.savefig('Imagenes/i{}.jpg'.format(i))
#Guardar archivo
np.savetxt('Camino más Corto.txt',caminoMinCoor,fmt='%2f')
print('La longitud del camino más corto encontrado es {}'.format(1/listaAjustes[Maximo]))   

#gráfico final
fig, ax =plt.subplots()
ax.plot(Iteraciones,valoresMaximosAjuste) 
ax.plot(Iteraciones,valoresPromedioAjuste) 
ax.set_xlabel('Iteraciones')
ax.set_ylabel('Valor de Ajuste')
ax.set_title('Graf 3. Valor de Ajuste Máximo y Valor Promedio  vs Cantidad de Iteraciones')