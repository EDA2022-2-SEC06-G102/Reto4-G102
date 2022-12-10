from Clases.Station import Station
from Clases.BusRoute import BusRoute
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bfs as bfs
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import cycles as cycles
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr

from DISClib.DataStructures import mapentry as me
from DISClib.ADT import stack
from DISClib.Algorithms.Sorting import mergesort as merge

import traceback


#----------------------------------------------------------------------
#funciones de comparacion en mapas ordenados
def compareStringMap(str1, str2):
    try:        
        if (str1 == str2):
            return 0
        elif (str1 > str2):
            return 1
        else:
            return -1
    except:
        print(type(str1),str1,type(str2),str2)
        traceback.print_exc()

def compareStringMap2(str1, node):
    try:        
        if (str1 == node["key"]):
            return 0
        elif (str1 > node["key"]):
            return 1
        else:
            return -1
    except:
        print(type(str1),str1,type(node),node)
        traceback.print()
        
def compareIntMap(int1, intentry):
    if (int(int1) == int(intentry)):
        return 0
    elif (int(int1) > int(intentry)):
        return 1
    else:
        return -1



#----------------------------------------------------------------------
"""analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)"""
class Model:
    def __init__(self ):
        self.stations    = om.newMap(omaptype='RBT', comparefunction=compareStringMap)
        self.tr_stations = om.newMap(omaptype='RBT', comparefunction=compareStringMap)
        self.bus_routes  = om.newMap(omaptype='RBT', comparefunction=compareStringMap)
        self.graph       = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=14000,comparefunction=compareStringMap2)
        self.search      = None

    def addStation(self, station):
        if station.transbordo == "S":
            om.put(self.tr_stations, station.code, station)
        pair =  om.get(self.stations, station.code)
        if pair is None:
            om.put(self.stations, station.code, station)
        else:
            encontrada = pair["value"]
            if encontrada.latitud == station.latitud and encontrada.longitud == station.longitud:
                #print("Estacion mismo codigo latitud diferente ")
                station.code = station.code+"A"
                om.put(self.stations, station.code, station)
        
        return station                 

    

    def getStationsList(self):
        return om.valueSet(self.stations)

    def getStationsSize(self):
        return om.size(self.stations)

    def getTransbordoStationsSize(self):
        llaves = om.keySet(self.stations)
        count =0 
        for k in lt.iterator(llaves):
            station = om.get(self.stations,k)["value"]
            if station.transbordo == "S":
                count += 1
        return count

    def getTransbordoStationsSize2(self):
        llaves = om.keySet(self.tr_stations)
        return lt.size(llaves)

    def getStationByCode(self, code:str) ->Station:
        pair = om.get(self.stations, code)
        return me.getValue(pair)

    #Busca una estacion conociendo el vertice
    def getStationByVertex(self, vertex:str) ->Station:        
        if vertex.startswith("T-"):
            return self.getStationByCode(vertex[2:])
        code = vertex.split("-")[0]    
        return self.getStationByCode(code)

    def addBusRoute(self, bus_route):
        pair =  om.get(self.bus_routes, bus_route.id)
        if pair is None:
            om.put(self.bus_routes, bus_route.id, bus_route)

    def getBusRoutesList(self):
        return om.valueSet(self.bus_routes)

    def getBusRoutesSize(self):
        return om.size(self.bus_routes)

    def getBusByCode(self, code:str) ->BusRoute:
        pair = om.get(self.bus_routes, code)
        return me.getValue(pair)

    def addGraphVertex(self,vertex):
        #print("AGR VTX",vertex)
        if not gr.containsVertex(self.graph,vertex):
            gr.insertVertex(self.graph,vertex)

        
    def addGraphEdge(self,code_origen, code_dest, peso):
        edge = gr.getEdge(self.graph, code_origen, code_dest)
        if edge is not None:
            #print("ARCO REPETIDO",code_origen,code_dest)
            return 
        gr.addEdge(self.graph, code_origen, code_dest, peso)
        ##lista = gr.edges(self.graph)
        #print(lt.size(lista))
        #for e in lt.iterator(lista):
        #    print(" ( " +e["vertexA"]+" --"+str(round(e["weight"],2)) +" --> "+e["vertexB"]+" )",end=" ,")
        #print("\n" ," ------ ")    

    def getGraphVertexList(self):
        return gr.vertices(self.graph)


    def getGraphEdgesList(self):
        return gr.edges(self.graph)
    

    def cycles(self,initialStation):
        search = cycles.DirectedCycle(self.graph)
        cycles.dfs(self.graph,search,initialStation)
        if cycles.hasCycle(search):
            ciclo = cycles.cycle(search)
            for e in lt.iterator(ciclo):            
                print(e)

    def bfs(self,initialStation):
        cola = None
        print("P1")
        self.search = bfs.BreadhtFisrtSearch(self.graph, initialStation)
        print("P2")
        arcos = self.getGraphEdgesList()
        print("P3")
        vertices_llegada = lt.newList('ARRAY_LIST')
        print("P4")
        for arco in lt.iterator(arcos):
            if arco["vertexB"] == initialStation:
                lt.addLast(vertices_llegada,arco["vertexA"])
        print("P5")
        largo = 0 
        for vertice in lt.iterator(vertices_llegada):
            if bfs.hasPathTo(self.search, vertice):
                colatemp,peso = self.graphPathTo(vertice, "bfs")
                l = lt.size(colatemp)
                if l > largo:
                    for item in lt.iterator(colatemp):
                        if item.startswith("T-") :
                            cola = colatemp
                            largo = l
        print("P6")
        return cola

    def graphHasPathTo(self,initialStation, finalStation, algorithm:str):

        if algorithm == "djk":
            self.search  = djk.Dijkstra(self.graph, initialStation)
            haycamino =  djk.hasPathTo(self.search, finalStation)
            return haycamino
        if algorithm == "bfs":
            self.search = bfs.BreadhtFisrtSearch(self.graph, initialStation)
            haycamino = bfs.hasPathTo(self.search, finalStation)
            return haycamino
        

    def graphPathTo(self,finalStation, algorithm:str):
        peso = 0
        if algorithm == "djk":
            pila = djk.pathTo(self.search, finalStation)
            cola = lt.newList('ARRAY_LIST')
            if pila is not None:
                while (not stack.isEmpty(pila)):
                    stop = stack.pop(pila)
                    peso += stop["weight"]
                    lt.addLast(cola, stop)
            return cola, peso
        if algorithm == "bfs":
                cola = lt.newList('ARRAY_LIST')
                pila = bfs.pathTo(self.search, finalStation)
                #return pila,0
                if pila is not None:
                    for value in lt.iterator(pila):
                        #print(value)
                        lt.addFirst(cola,value)
                    return cola,0


    def comparedict(a1, a2):    
        if (a1["value"] == a2["value"]):
            return 0
        elif (a1["value"]  > a2["value"]):
            return 1
        else:
            return -1

    def MapaKosaraju(self):
        self.mapa_kosaraju  = om.newMap(omaptype='RBT', comparefunction=compareStringMap)
        self.search =scc.KosarajuSCC(self.graph) 
        idscc = self.search['idscc']['table']['elements']
        
        
        for element in idscc:            
            if element["value"] is not None:
                ##print(element)
                llave = int(element["value"])
                pair =  om.get(self.mapa_kosaraju, llave)
                if pair is not None:
                    dict = me.getValue(pair)
                    dict["cont"] += 1
                    lt.addLast(dict["vertices"], element["key"])
                    om.put(self.mapa_kosaraju, llave, dict)
                else:                    
                    vertices = lt.newList('ARRAY_LIST')
                    lt.addLast(vertices, element["key"])
                    dict = {"vertices":vertices, "num":llave, "cont":1}
                    om.put(self.mapa_kosaraju, llave, dict)

        
    def GraphScc(self):              
        num_conected =  scc.connectedComponents(self.search)
        lista_valores = om.valueSet(self.mapa_kosaraju)
        merge.sort(lista_valores, compareList)
        for element in lt.iterator(lista_valores):
            vertices = element["vertices"]
            merge.sort(vertices, compareList2)
            element["vertices"] = vertices
        return lista_valores, num_conected
    
    def estacionMasCercana(self, lon2, lat2):
        best_peso = 1000000000
        mejor_Station = None
        list = om.valueSet(self.stations)
        for station in lt.iterator(list):
            peso = station.distanceTo(lon2, lat2)
            if peso < best_peso:
                best_peso = peso
                mejor_Station = station
        print("mejor_station:", mejor_Station, " distance: ",best_peso) 
        return  mejor_Station

    def estacionesDelVecindario(self, vecindario):
            vecindarios_list = lt.newList('ARRAY_LIST')
            list = om.valueSet(self.stations)
            for station in lt.iterator(list):
                if station.neighborhood_name == vecindario:
                    lt.addLast(vecindarios_list, station)
 
            return vecindarios_list

    def verticesDelVecindario(self, stations_list):
        list_vertices = lt.newList('ARRAY_LIST')
        vetices = gr.vertices(self.graph)
        for station in lt.iterator(stations_list):
            if station.transbordo == "S":
                vertice = 'T-'+ station.code
                if gr.containsVertex(self.graph, vertice):
                    lt.addLast(list_vertices, vertice)

            for vertice in lt.iterator(vetices):
                if vertice.startswith(station.code+"-"):                
                    lt.addLast(list_vertices, vertice)                    
        return list_vertices


    def buscarVertice(self,station):
        if station.transbordo == "S":
            vertice = 'T-'+ station.code
            print("tenia transbordo ",vertice)
            print(gr.containsVertex(self.graph, vertice))
            if gr.containsVertex(self.graph, vertice):
                print("encontre vertice ",vertice)
                return vertice
        else:
            listVertex =gr.vertices(self.graph)
            for vertex in lt.iterator(listVertex):              
                new_vertex = new_vertice(vertex)
                print("Buscado ",new_vertex," vs ",station.code)
                if new_vertex == station.code:
                    print("encontro",vertex)
                    return vertex

def new_vertice(vertex):
    #print(vertex,"eeeeeeeeeee")
    lista_vertex =vertex.split('-')
    new_vertex = lista_vertex[0]
    #print(new_vertex,"eeeee")
    return new_vertex

def new_idbus(idbus):
    list =idbus.split('BUS-')
    new_idbus = list[1]
    return new_idbus

def compareList(a1, a2):    
    return a2["cont"] < a1["cont"] 
def compareList2(a1, a2):    
    return a2 < a1