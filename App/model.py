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
