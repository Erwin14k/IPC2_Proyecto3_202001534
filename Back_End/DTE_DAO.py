from DTE import DTE
import json 
from datetime import datetime
from xml.dom import minidom
import xml.etree.ElementTree as ET
import re
from ERROR_DAO import ERROR_DAO
error_dao_handler=ERROR_DAO()

class DTE_DAO:
    def __init__(self):
        self.dte_array = []


    #Función para crear nuevos DTE(Documento Tributario Electrónico)
    def new_dte(self,id_reference,emmiter_nit,reciever_nit,date,value,tax,total):
        value=value.replace(" ","")
        tax=tax.replace(" ","")
        total=total.replace(" ","")
        id_reference=id_reference.replace(" ","")
        emmiter_nit=emmiter_nit.replace(" ","")
        reciever_nit=reciever_nit.replace(" ","")
        date_buffer=""
        date_state=0
        for c in date:
            if date_state==0:
                if c.isdigit():
                    date_state=1
            if date_state==1:
                if c.isdigit() or c=="/":
                    date_buffer+=c
                else:
                    break
        print(date_buffer)


        date=date.replace(" ","")
        for dte in self.dte_array:
            if dte.id_reference == id_reference:
                print('El Número de referencia ya existe, intente de nuevo!')
                error_dao_handler.new_error(date_buffer,"DUPLICADO")
                return False
        new = DTE(id_reference,emmiter_nit,reciever_nit,date_buffer,float(value),float(tax),float(total))
        self.dte_array.append(new)
        print("Se creo un nuevo DTE")
        return True
    
    #Función que valida los datos numéricos
    def validate_value_tax_and_total(self,date,value,tax,total):
        value=value.replace(" ","")
        tax=tax.replace(" ","")
        total=total.replace(" ","")
        tax_goal=round((float(value)*0.12),2)
        total_goal=float(value)+float(tax)
        date_buffer=""
        date_state=0
        for c in date:
            if date_state==0:
                if c.isdigit():
                    date_state=1
            if date_state==1:
                if c.isdigit() or c=="/":
                    date_buffer+=c
                else:
                    break
        if tax_goal==float(tax) and total_goal==float(total):
            return True
        elif tax_goal!=float(tax):
            error_dao_handler.new_error(date_buffer,"IVA")
            return False
        else:
            error_dao_handler.new_error(date_buffer,"TOTAL")
            return False
    
    #Función que valida los nits de emisores
    def validate_emitter_nit(self,date,nit):
        #Primero se recolecta la fecha
        date_buffer=""
        date_state=0
        for c in date:
            if date_state==0:
                if c.isdigit():
                    date_state=1
            if date_state==1:
                if c.isdigit() or c=="/":
                    date_buffer+=c
                else:
                    break


        nit=nit.replace(" ","")
        #print("nit:"+nit+"ok")
        #el nit es un entero, por lo tanto necesitamos tenerlo como string para su posterior análisis.
        nit=str(nit)
        #Necesitamos un contador, el cuál está inicializado en 2.
        counter=2
        #Necesitamos conocer que longitud tiene este nit.
        nit_length=len(nit)
        #Esta variable almacenará el número importante del int, puede ser un dígito del 0 al 9 o una letra k.
        important_number=nit[nit_length-1]
        #Para una mejor comodiad de evaluación almacenamos en esta variable el nit al revés.
        reverserd_nit=nit[::-1]
        #Esta variable almacenará la suma total en el recorrido.
        total_sum=0
        for c in reverserd_nit[1:nit_length]:
            total_sum+=int(c)*counter
            counter+=1
        #Una varibale que almacenará el módulo 11 de la sumatoria
        mod_11=total_sum%11
        #variable que almacena la resta= "11-(mod11(sumatoria))"
        subtract=11-mod_11
        #variable que le calcula el modulo 11 a substract
        final_result=subtract%11
        #print(important_number+str(final_result))
        if str(final_result)==important_number:
            print("nit: ",nit,"El número final debería ser: ",important_number," Y es: ",final_result,"TRUE")
            return True
        elif important_number=="K"and final_result==10 :
            print("nit: ",nit,"El número final debería ser: ",important_number," Y es: ","k","TRUE")
            return True
        else:
            print("nit: ",nit,"El número final debería ser: ",important_number," Y es: ",final_result,"FALSE")
            error_dao_handler.new_error(date_buffer,"NIT_EMISOR")
            return False


    #Función que valida los nits de los receptroes
    def validate_reciever_nit(self,date,nit):
        #Primero se recolecta la fecha
        date_buffer=""
        date_state=0
        for c in date:
            if date_state==0:
                if c.isdigit():
                    date_state=1
            if date_state==1:
                if c.isdigit() or c=="/":
                    date_buffer+=c
                else:
                    break
        nit=nit.replace(" ","")
        #print("nit:"+nit+"ok")
        #el nit es un entero, por lo tanto necesitamos tenerlo como string para su posterior análisis.
        nit=str(nit)
        #Necesitamos un contador, el cuál está inicializado en 2.
        counter=2
        #Necesitamos conocer que longitud tiene este nit.
        nit_length=len(nit)
        #Esta variable almacenará el número importante del int, puede ser un dígito del 0 al 9 o una letra k.
        important_number=nit[nit_length-1]
        #Para una mejor comodiad de evaluación almacenamos en esta variable el nit al revés.
        reverserd_nit=nit[::-1]
        #Esta variable almacenará la suma total en el recorrido.
        total_sum=0
        for c in reverserd_nit[1:nit_length]:
            total_sum+=int(c)*counter
            counter+=1
        #Una varibale que almacenará el módulo 11 de la sumatoria
        mod_11=total_sum%11
        #variable que almacena la resta= "11-(mod11(sumatoria))"
        subtract=11-mod_11
        #variable que le calcula el modulo 11 a substract
        final_result=subtract%11
        #print(important_number+str(final_result))
        if str(final_result)==important_number:
            print("nit: ",nit,"El número final debería ser: ",important_number," Y es: ",final_result,"TRUE")
            return True
        elif important_number=="K"and final_result==10 :
            print("nit: ",nit,"El número final debería ser: ",important_number," Y es: ","k","TRUE")
            return True
        else:
            print("nit: ",nit,"El número final debería ser: ",important_number," Y es: ",final_result,"FALSE")
            error_dao_handler.new_error(date_buffer,"NIT_RECEPTOR")
            return False
        



    #Función básica que imprime en consola todos los "dte" validados existentes
    def print_all_dte(self):
        for dte in self.dte_array:
            print(dte.id_reference,dte.emmiter_nit,dte.reciever_nit,dte.date,dte.value,dte.tax,dte.total)
    
    #Función para leer xml
    def read_xml(self,route):
        xml_file = minidom.parse(route)
        dtes = xml_file.getElementsByTagName('DTE')
        for dte in dtes:
            date = dte.getElementsByTagName("TIEMPO")[0].childNodes[0].data
            reference = dte.getElementsByTagName("REFERENCIA")[0].childNodes[0].data
            emmiter_nit = dte.getElementsByTagName("NIT_EMISOR")[0].childNodes[0].data 
            reciever_nit = dte.getElementsByTagName('NIT_RECEPTOR')[0].childNodes[0].data 
            value = dte.getElementsByTagName('VALOR')[0].childNodes[0].data 
            tax = dte.getElementsByTagName('IVA')[0].childNodes[0].data 
            total = dte.getElementsByTagName('TOTAL')[0].childNodes[0].data 
            self.new_dte(reference,emmiter_nit,reciever_nit,date,float(value),float(tax),float(total))
        self.print_all_dte()
        return("archivo cargado con éxito!")