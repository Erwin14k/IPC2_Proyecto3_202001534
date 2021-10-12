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
    
    def errors_counter_by_date(self,date):
        emmiters_errors=0
        recievers_errors=0
        tax_errors=0
        total_errors=0
        duplicate_errors=0
        list_summary=[]
        for error in self.errors:
            if error.type=="TOTAL" and error.date==date:
                total_errors+=1
            elif error.type=="NIT_EMISOR" and error.date==date:
                emmiters_errors+=1
            elif error.type=="NIT_RECEPTOR" and error.date==date:
                recievers_errors+=1
            elif error.type=="IVA" and error.date==date:
                tax_errors+=1
            elif error.type=="DUPLICADO" and error.date==date:
                duplicate_errors+=1
        list_summary=[*list_summary,emmiters_errors]
        list_summary=[*list_summary,recievers_errors]
        list_summary=[*list_summary,tax_errors]
        list_summary=[*list_summary,total_errors]
        list_summary=[*list_summary,duplicate_errors]
        return list_summary
    def print_all_errors(self):
        for error in self.errors:
            print(error.date,error.type)