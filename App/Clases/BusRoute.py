class BusRoute:
    def __init__(self, id):
        self.id = id
        self.newId = id.replace('BUS - ', '')
    # cuando se vaya a imprimir    
    def __str__(self):
        return  self.id