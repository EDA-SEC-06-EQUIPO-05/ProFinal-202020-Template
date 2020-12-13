"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import maxpq as max
from DISClib.ADT import minpq as min
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import arraylist as ar
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import datetime
import time
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion

def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar toda la información
    Se crean indices por los siguientes criterios:
    Retorna el analizador inicializado.
    """
    analyzer = {'taxisCompañias': None,
                'viajesCompañias': None,
                'Companies_services': None,
                'Companies_taxi': None,
                'grafoAreas': None
                }

    analyzer["taxisCompañias"]= m.newMap(500,109345121,
                                   maptype='CHAINING',
                                   loadfactor=0.4,
                                   comparefunction=compareIds)

    analyzer["viajesCompañias"]= m.newMap(500,109345121,
                                   maptype='CHAINING',
                                   loadfactor=0.4,
                                   comparefunction=compareIds)

    analyzer['Companies_services'] = {}

    analyzer['Companies_taxi'] = {}

    analyzer['grafoAreas']= gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
                                              comparefunction= compareIds)

    return analyzer


def addData(analyzer, info, dict, dict2):
    analyzer['Companies_services'] = dict
    analyzer['Companies_taxi'] = dict2

def addRoutes(analyzer, registro):

    tInicialComp= registro["trip_start_timestamp"]
    duracion= registro["trip_seconds"]
    areaSalida= registro["pickup_community_area"]
    areaLlegada= registro["dropoff_community_area"]
    tInicialComp= tInicialComp.replace("T"," ")
    tInicialComp= tInicialComp.split()
    tInicial= tInicialComp[1]
    if gr.containsVertex(analyzer['grafoAreas'], areaSalida)== False:
        gr.insertVertex(analyzer['grafoAreas'], areaSalida)
    if gr.containsVertex(analyzer['grafoAreas'], areaLlegada)== False:
        gr.insertVertex(analyzer['grafoAreas'], areaLlegada)
    if areaSalida!= areaLlegada:
        lstInfo= lt.newList("ARRAY_LIST", compareElements)
        lt.addLast(lstInfo, tInicial)
        lt.addLast(lstInfo, duracion)
        gr.addEdge(analyzer['grafoAreas'], areaSalida, areaLlegada, lstInfo)


# ==============================
# Funciones de consulta
# ==============================

def parteA(analyzer, toptaxis, topservicios):
    mxt = max.newMaxPQ(compareQuantity)
    mxs = max.newMaxPQ(compareQuantity)
    cantidad_taxis = 0
    for k,v in analyzer['Companies_taxi'].items():
        y = max.insert(mxt, v)
        cantidad_taxis += v
        #Para sacar la cantidad de taxis se recorre una vez el diccionario O(n), siendo n la cantidad de compañias
    for k,v in analyzer['Companies_services'].items():
        x = max.insert(mxs, v)
    cantidad_compañias = max.size(mxt) 
    #Cantidad de compañias O(1), función Size de maxpq
    if 0<toptaxis<=cantidad_compañias and 0<topservicios<=cantidad_compañias:
        a = 0
        top_taxis = []
        top_final_taxis = []
        while a<toptaxis:
            mayor_t = max.delMax(mxt)
            top_taxis.append(mayor_t)
            a += 1
        i = 0
        top = []
        top_final_servicios = []
        while i<topservicios:
            mayor = max.delMax(mxs)
            top.append(mayor)
            i += 1
        b = 0
        while b<len(top_taxis):
            for k,v in analyzer['Companies_taxi'].items():
                if v == top_taxis[b] and k not in top_final_taxis:
                    mt = k
                    top_final_taxis.append(mt) 
            b += 1
        j = 0
        while j<len(top):
            for k,v in analyzer['Companies_services'].items():
                if v == top[j] and k not in top_final_servicios:
                    ms = k
                    top_final_servicios.append(ms) 
            j += 1
        top_taxis_str = '\n'
        n = 0
        while n<len(top_final_taxis):
            top_taxis_str += str(top_final_taxis[n])
            top_taxis_str += '\n'
            n += 1
        top_servicios_str = '\n'
        n2 = 0
        while n2<len(top_final_servicios):
            top_servicios_str += str(top_final_servicios[n2])
            top_servicios_str += '\n'
            n2 += 1

        #Complejidad de los tops O(x log C), se sacan los máximos correspondientes de una maxpq
        #x representa los valores de M y N, es decir, los tops que da el usuario
        fin = '\nEl total de taxis individuales es ' + str(cantidad_taxis)+'\nEl total de compañias es ' + str(cantidad_compañias) + '\nEl top ' + str(toptaxis) +' de compañias ordenadas por la cantidad de taxis afiliados es: ' + str(top_taxis_str) + '\nEl top ' + str(topservicios) + ' de compañías que más servicios prestaron es: ' + str(top_servicios_str)
    else:
        fin = 'Por favor seleccione valores para los tops que se encuentren entre 1 y ' + str(cantidad_compañias)
    return fin

def parteC(analyzer, zonaSalida, zonaLlegada, horaInicial, horaFinal):

    
# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
    """
    Compara dos ids
    """
    if (id1 == id2):
        return 0
    else:
        return 1

def compareQuantity(num1, num2):

    if (num1 == num2):
        return 0
    elif (num1 > num2):
        return 1
    else:
        return -1

def compareElements(el1, el2):

    if (el1 == el2):
        return 0
    else:
        return 1

  
def prueba(hola,M):
    mx = max.newMaxPQ(compareQuantity)
    for k,v in hola.items():
        x = max.insert(mx, v)
    i = 0
    top = []
    top_final = []
    while i<M:
        mayor = max.delMax(mx)
        top.append(mayor)
        i += 1
    #print(top)
    j = 0
    while j<len(top):
        for k,v in hola.items():
            if v == top[j]:
                mt = k
                top_final.append(mt) 
        j += 1
    #print(mx)
    return top_final
#print(prueba({'Rick':13,'Tuly':3,'Leo':8,'Alejo':10,'Piedra':100}, 2))
def prueba2(hola):
    mx = min.newMinPQ(compareQuantity)
    for h in hola:
        x = min.insert(mx, h)
    mayor = min.min(mx)
    print(mx)
    return mayor
#print(prueba2([1,54,44,421,2,3,5]))
'''
    taxiId= info["taxi_id"]
    compañia= info["company"]
    lst_taxis= lt.newList("ARRAY_LIST", compareIds)
    if compañia == "":
        compañia= "Independent Owner"
    if m.contains(analyzer["taxisCompañias"], compañia) == False:
        m.put(analyzer["viajesCompañias"], compañia, 1)
        if lt.isPresent(lst_taxis, taxiId) == 0:
            m.put(analyzer["taxisCompañias"], compañia, 1)
            lt.addLast(lst_taxis, taxiId)
    elif m.contains(analyzer["taxisCompañias"], compañia) == True:
        keyvalue= m.get(analyzer["viajesCompañias"], compañia)
        valor= me.getValue(keyvalue)
        valor+= 1
        m.put(analyzer["viajesCompañias"], compañia, valor)
        if lt.isPresent(lst_taxis, taxiId) == 0:
            keyvalue= m.get(analyzer["taxisCompañias"], compañia)
            valor= me.getValue(keyvalue)
            valor+= 1
            m.put(analyzer["taxisCompañias"], compañia, valor)
'''

'''
    listaCompañias= m.keySet(analyzer["viajesCompañias"])
    cantidadCompañias= lt.size(listaCompañias)
    lstiterator= it.newIterator(listaCompañias)
    taxisTotales= 0
    descender= True
    cuenta= 0
    while it.hasNext(lstiterator):
        comp= it.next(lstiterator)
        anaTaxis= m.get(analyzer["taxisCompañias"], comp)
        numTaxis= me.getValue(anaTaxis)
        anaViajes= m.get(analyzer["viajesCompañias"], comp)
        numViajes= me.getValue(anaViajes)
        taxisTotales+= numTaxis
        while (descender == True) and (cuenta < toptaxis):
            p= 0 #Funcion aun por desarrollar
'''