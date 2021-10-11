import json 
from datetime import datetime
import re
from ERROR import ERROR
class ERROR_DAO:
    def __init__(self):
        self.errors = []
        self.type_error_counter_by_date=0
    
    #Función para crear nuevos ERRORES
    def new_error(self,date,type):
        new = ERROR(date,type)
        self.errors.append(new)
        print("Se detectó un nuevo Error= ","Fecha:",date,"Tipo:",type)
        return True