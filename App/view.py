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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""
# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


Smallfile = 'taxi-trips-wrvz-psew-subset-small.csv'
Mediumfile = 'taxi-trips-wrvz-psew-subset-medium.csv'
Largefile = 'taxi-trips-wrvz-psew-subset-large.csv'

# ___________________________________________________
#  Variables
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("_"*40)
    print("\nBienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información sobre el servicio de taxis")
    print("3- Parte A")
    print("4- Parte B")
    print('5- Parte C')
    print("0- Salir")
    print("_"*40)


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('\nSeleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        eleccion = input('Seleccione un tamaño de archivo para cargar:\n'+"_"*40+' \nSmall: 1\nMedium: 2\nLarge: 3\n')
        print("\nCargando información de crimenes ....")
        if eleccion == 1:
            controller.loadData(cont, Smallfile)
        elif eleccion == 2:
            controller.loadData(cont, Mediumfile)
        elif eleccion == 3:
            controller.loadData(cont, Largefile)
        else:
            print('Por favor seleccione una opción válida')
    elif int(inputs[0]) == 3:
        print("\nParte A: ")
        print("\nBuscando accidentes según severidad en una fecha: ")
        initialDate = input("Fecha (YYYY-MM-DD): ")
        numoffenses = controller.getAccidentsByRangeSeverity(cont, initialDate)
        print(numoffenses)

    elif int(inputs[0]) == 4:
        print("\nParte B: ")
        print("\nBuscando accidentes anteriores de la fecha: ")
        initialDate = "2016-01-01"
        finalDate = input("Fecha a buscar (YYYY-MM-DD): ")
        total = controller.getAccidentsByRange(cont, initialDate, finalDate)
        print(total)

    elif int(inputs[0]) == 5:
        print("\nParte C: ")
        print("\nBuscando accidentes en un rango de fechas: ")
        initialDate = input("Rango Inicial (YYYY-MM-DD): ")
        finalDate = input("Rango Final (YYYY-MM-DD): ")
        total = controller.getAccidentsByRange(cont, initialDate, finalDate)
        print(total)
    else:
        sys.exit(0)
sys.exit(0)