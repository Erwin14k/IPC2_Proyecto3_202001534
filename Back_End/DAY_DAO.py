import json 
from datetime import datetime
import re
from DAY import DAY
class DAY_DAO:
    def __init__(self):
        self.days = []
    
    #Función para registrar nuevos días
    def new_day(self,date):
        for day in self.days:
            if day.date == date:
                return False
        new = DAY(date)
        self.days.append(new)
        print("Se registró un nuevo día: ",date)
        return True
