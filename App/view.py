"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from Clases.Model import Model
import time
from tabulate import tabulate

control =  None
#catalog = None


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

#----------------------------------------------------------------------
#funciones para obtener la memoria
def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

def printLoadDataAnswer(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if isinstance(answer, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer:.3f}")
#----------------------------------------------------------------------
#controlador

def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control


def printList(lista):
    for element in lt.iterator(lista):
        print(element)


    




def getModel(control) ->Model:
    return control["model"]

#--------------------------------------------------------------------------------------------------------------------------------------------


def requerimiento_0():
    print("Cargando información de los archivos ....")
    file_size = input("\nSeleccione el tamaño de la muestra:\n5pct\n10pct\n20pct\n30pct\n50pct\n80pct\nlarge\nsmall\n Seleccione una opción para continuar: ")
    
    print("Desea observar el uso de memoria? (True/False)")
    mem = input("Respuesta: ")
    mem = castBoolean(mem)

    answer = controller.Tiempo_de_carga_loadData(file_size, control, memflag=mem)
    printLoadDataAnswer(answer)
    model = getModel(control) 
    print("Numero total de estaciones:        " , model.getStationsSize())
    print("Numero de estaciones de transbordo:" , model.getTransbordoStationsSize())
    print("Numero de estaciones de transbordo:" , model.getTransbordoStationsSize2())
    print("Numero total de rutas de bus:      " , model.getBusRoutesSize())
    ####print("-----------------------[rutas]-------------------")
    ###printList(model.getBusRoutesList())


    #print(lt.size(lista_stops))
    print("-----------------------[vertces del grafo]-------------------")
    printList(model.getGraphVertexList())
    print("numero vertices grafo:            ",lt.size(model.getGraphVertexList()))
    ###print("-----------------------[arcos del grafo]-------------------")
    ###printList(model.getGraphEdgesList())

    ###edges = model.getGraphEdgesList()    
    ###for e in lt.iterator(edges):
    ###    print(e["vertexA"]+","+str(round(e["weight"],2)) +", "+e["vertexB"])
    print("numero arcos grafo ",lt.size(model.getGraphEdgesList()))

def print_primeros_y_ultimos(lista, funcion_de_impresion, num, True_or_False):
    
    #Entra si es True
    if True_or_False:
        if lt.size(lista) > num*2:
            primeros = lt.subList(lista, 1, num)
            ultimos  = lt.subList(lista, lt.size(lista)-(num-1), num)
            for line in lt.iterator(ultimos):
                lt.addLast(primeros, line )  
                if funcion_de_impresion:               
                    funcion_de_impresion(primeros)
            return primeros
        else:
            if funcion_de_impresion:    
                funcion_de_impresion(lista)
            return lista

    #Entra si es False
    else: 
        if lt.size(lista) > num:
            total = lt.subList(lista, 1, num)
            funcion_de_impresion(total)
            return total
        else:
            funcion_de_impresion(lista)
            return lista


#----------------------------------------------------------------------
def printMenu():
    print("Bienvenido")
    print("0- Cargar información desde los Archivos")
    print("1- (REQ 1)Buscar un camino posible entre dos estaciones")
    print("2- (REQ 2)Buscar el camino con menos estaciones entre dos estaciones")
    print("3- (REQ 3 INDIVIDUAL)Reconocer los componentes conectados de la Red de rutas de bus")
    print("4- (REQ 4 INDIVIDUAL)Planear el camino con distancia mínima entre dos puntos geográficos")
    print("5- (REQ 5 INDIVIDUAL)Localizar las estaciones “alcanzables” desde un origen a un número máximo de conexiones dado")
    print("6- (REQ 6 INDIVIDUAL)Buscar el camino con distancia mínima entre una estación de origen y un vecindario de destino")
    print("7- (REQ 7 INDIVIDUAL)Encontrar un posible camino circular desde una estación de origen")
    print("8- (REQ 8 BONO)Graficar resultados para cada uno de los requerimientos")


def print_Requerimiento_3(lista):
    impresion_req3 = []
    headers = [ "numero de estaciones", "indices"]
    for element in lt.iterator(lista):
        vertices =print_primeros_y_ultimos( element["vertices"] , None, 3, True)
        new_vertice = ""
        for vertice in lt.iterator(vertices):
            new_vertice = new_vertice +", " + vertice
        impresion_req3.append([ element["cont"],new_vertice[1:] ])
        
    print(tabulate(impresion_req3, headers, tablefmt="grid"))


while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        control = newController()
        modelClass = control["model"]
        requerimiento_0()
    elif int(inputs[0]) == 1:
        origen = input("Identificador de la estación origen: ")
        destino = input("Identificador de la estación destino: ")
        cola, peso = controller.requerimiento_1(modelClass, origen, destino)
        print("La distancia del recorrido es de", peso)

    elif int(inputs[0]) == 2:
        origen = input("Identificador de la estación origen: ")
        destino = input("Identificador de la estación destino: ")
        pila = controller.requerimiento_2(modelClass, origen, destino)
    elif int(inputs[0]) == 3:
        lista_valores, num_conected = controller.requerimiento_3(modelClass)
        print_primeros_y_ultimos( lista_valores , print_Requerimiento_3, 5, False)
    elif int(inputs[0]) == 4:
        print('Localización geográfica del usuario')
        lonOrigen = float(input("Origen (longitud) del usuario': "))
        latOrigen = float(input("Origen (latitud) del usuario': "))
        lonDestino = float(input(" destino(longitud) del usuario': "))
        latDestino = float(input(" destino(latitud) del usuario': "))
        cola, peso = controller.requerimiento_4(modelClass, lonOrigen, latOrigen, lonDestino, latDestino)

    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:

        vertice_origen = str(input("Identificador de la estación origen (en formato Code-IdBus): "))
        vecindario_destino = str(input("El identificador del vecindario (Neighborhood) destino: "))
        controller.requerimiento_6(modelClass, vertice_origen, vecindario_destino)

    elif int(inputs[0]) == 7:
        pass
    elif int(inputs[0]) == 8:
        pass
        
    else:
        sys.exit(0)
sys.exit(0)
