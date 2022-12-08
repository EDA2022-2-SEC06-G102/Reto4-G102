import model as model
class Station:
    def __init__(self, code, latitud:float, longitud:float, district_name:str, neighborhood_name:str, transbordo):
        self.code = code
        self.latitud = latitud
        self.longitud = longitud
        self.district_name = district_name
        self.neighborhood_name = neighborhood_name
        self.transbordo = transbordo 

    def distanceTo(self, lon2, lat2):
        return model.haversine(self.longitud, self.latitud, lon2, lat2)
        
    def __str__(self):
        return  self.code +" "+ self.district_name+" "+self.transbordo

        