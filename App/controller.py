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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, taxisfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    taxisfile = cf.data_dir + taxisfile
    input_file = csv.DictReader(open(taxisfile, encoding="utf-8"),
                                delimiter=",")
    d = {}
    d2 = {}
    lista = []
    for registro in input_file:
        if registro['taxi_id'] not in lista:
            lista.append(registro['taxi_id'])
            if registro['company'] not in d2.keys():
                d2[registro['company']] = 1
            else:
                d2[registro['company']] += 1
                
        if registro['company'] not in d.keys():
            d[registro['company']] = 0
        else:
            d[registro['company']] += 1
        model.addData(analyzer, registro, d, d2)

        model.addRoutes(analyzer, registro)
    #print(d)
    #print(len(lista))
    #print(d2)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def parteA(analyzer, toptaxis, topservicios):
    a = model.parteA(analyzer, toptaxis, topservicios)
    return a

def parteC(analyzer, zonaSalida, zonaLlegada, horaInicial, horaFinal):
    c= model.parteC(analyzer, zonaSalida, zonaLlegada, horaInicial, horaFinal)
    return c