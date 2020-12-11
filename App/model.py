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
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
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
                'viajesCompañias': None
                }

    analyzer["taxisCompañias"]= m.newMap(500,109345121,
                                   maptype='CHAINING',
                                   loadfactor=0.4,
                                   comparefunction=compareIds)

    analyzer["viajesCompañias"]= m.newMap(500,109345121,
                                   maptype='CHAINING',
                                   loadfactor=0.4,
                                   comparefunction=compareIds)

    return analyzer


def addData(analyzer, info):

    taxiId= info["taxi_id"]
    compañia= info["company"]
    lst_taxis= lt.newList("ARRAY_LIST", compareIds)
    if compañia == "":
        compañia= "Independent Owner"
    if m.contains(analyzer["taxisCompañias"], compañia) == False:
        m.put(analyzer["viajesCompañias"], compañia, 1)
        if lt.isPresent(lst_taxis, taxiId) == 0:
            m.put(analyzer["taxisCompañias"], compañia, 1)
            lt.addLast(taxiId)
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

# ==============================
# Funciones de consulta
# ==============================

def parteA(analyzer, toptaxis, topservicios):

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

 '''  
def prueba(hola):
    mx = max.newMaxPQ(compareQuantity)
    for h in hola:
        x = max.insert(mx, h)
    mayor = max.delMax(mx)
    mayor2 = max.delMax(mx)
    mayor3 = max.delMax(mx)
    mayor4 = max.delMax(mx)
    print(mx)
    return mayor, mayor2, mayor3, mayor4
print(prueba({'Rick':13,'Tuly':30,'Leo':8,'Alejo':10}))
def prueba2(hola):
    mx = min.newMinPQ(compareQuantity)
    for h in hola:
        x = min.insert(mx, h)
    mayor = min.min(mx)
    print(mx)
    return mayor
print(prueba2([1,54,44,421,2,3,5]))
'''