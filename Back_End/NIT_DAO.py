from datetime import date
from NIT import NIT
import xml.etree.ElementTree as ET
class NIT_DAO:
    def __init__(self):
        self.nits_array = []

    #Función para registrar nuevos días
    def new_nit(self,code,date,recieved_nit,emmited_nit):
        for nit in self.nits_array:
            if nit.date == date and nit.code==code:
                nit.recieved_nit+=float(recieved_nit)
                nit.emmited_nit+=float(emmited_nit)
                return "-------"
        new = NIT(code,date,recieved_nit,emmited_nit)
        self.nits_array.append(new)
        print("Se registró un nuevo Nit!!")
        return True
    
    def print_nits(self):
        for nit in self.nits_array:
            print(nit.code,nit.date,nit.recieved_nit,nit.emmited_nit)



    def prettify_xml(self,element, indent='  '):
        queue = [(0, element)]  # (level, element)
        while queue:
            level, element = queue.pop(0)
            children = [(level + 1, child) for child in list(element)]
            if children:
                element.text = '\n' + indent * (level+1) 
            if queue:
                element.tail = '\n' + indent * queue[0][0]  
            else:
                element.tail = '\n' + indent * (level-1)  
            queue[0:0] = children