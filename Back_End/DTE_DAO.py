from DTE import DTE
import json 
from datetime import datetime

class DTE_DAO:
    def __init__(self):
        self.dte_array = []


    #Función para crear nuevos DTE(Documento Tributario Electrónico)
    def new_dte(self,id_reference,emmiter_nit,reciever_nit,date,value,tax,total):
        for dte in self.dte_array:
            if dte.id_reference == id_reference:
                print('El Número de referencia ya existe, intente de nuevo')
                return False
        new = DTE(id_reference,emmiter_nit,reciever_nit,date,value,tax,total)
        self.dte_array.append(new)
        print("Se creo un nuevo DTE")
        return True