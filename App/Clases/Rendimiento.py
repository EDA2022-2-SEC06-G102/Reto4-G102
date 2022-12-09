
import time
import tracemalloc

class Rendimiento:
    def __init__(self,memflag) -> None:
        # toma el tiempo al inicio del proceso
        self.start_time = getTime()
        self.memflag = memflag
   
        # inicializa el proceso para medir memoria
        if self.memflag is True:
            tracemalloc.start()
            start_memory = self.getMemory()

    def finalizar(self):            
    
        stop_time = self.getTime()
        # calculando la diferencia en tiempo
        delta_time = self.deltaTime(stop_time, self.start_time)

        # finaliza el proceso para medir memoria
        if self.memflag is True:
            stop_memory = self.getMemory()
            tracemalloc.stop()
            # calcula la diferencia de memoria
            delta_memory = self.deltaMemory(stop_memory, self.start_memory)
            # respuesta con los datos de tiempo y memoria
            print("Time: ",delta_time," Memoria: ",delta_memory)
        

        else:
            # respuesta sin medir memoria
            print("Time: ",delta_time)

    
    def getMemory(self):
        """
        toma una muestra de la memoria alocada en instante de tiempo
        """
        return tracemalloc.take_snapshot()

    def deltaTime(self,end, start):
        """
        devuelve la diferencia entre tiempos de procesamiento muestreados
        """
        elapsed = float(end - start)
        return elapsed        