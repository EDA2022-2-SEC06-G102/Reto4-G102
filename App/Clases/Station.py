import model as model
from DISClib.ADT import orderedmap as om

def compareStrCodeMap(str1, str2):

    if (str1 == str2):
        return 0
    elif (str1 > str2):
        return 1
    else:
        return -1


class Station:
    def __init__(self, code, latitud:float, longitud:float, district_name:str, neighborhood_name:str, transbordo):
        self.code = code
        self.latitud = latitud
        self.longitud = longitud
        self.district_name = district_name
        self.neighborhood_name = neighborhood_name
        self.transbordo = transbordo 
        self.adyacentes = om.newMap(omaptype='RBT', comparefunction=compareStrCodeMap)

    def distanceTo(self, lon2, lat2):
        return model.haversine(self.longitud, self.latitud, lon2, lat2)

    def addAyacente(self,code:str):
        om.put(self.adyacentes,code,code)

    def getAyacentes(self,code:str):
        return om.keys(self.adyacentes)
        
    def __str__(self):
        return  "Estacion: "+self.code +" "+ str(self.district_name)+" ("+str(self.neighborhood_name)+" ) "+self.transbordo

        