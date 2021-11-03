from DTE import DTE
import json 
from datetime import datetime
from xml.dom import minidom
import xml.etree.ElementTree as ET
import re
from ERROR_DAO import ERROR_DAO
from DAY_DAO import DAY_DAO
from NIT_DAO import NIT_DAO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
nit_dao_handler=NIT_DAO()
error_dao_handler=ERROR_DAO()
day_dao_handler=DAY_DAO()


class DTE_DAO:
    def __init__(self):
        self.dte_array = []
        self.emmiters=[]
        self.recievers=[]


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
        day=""
        month=""
        year=""
        day=date_buffer[0:2]
        month=date_buffer[3:5]
        year=date_buffer[6:10]
        code=""
        counter=0
        counter=self.total_dte_counter_by_date(date_buffer)
        if counter ==0 or counter <=9:
            code=year+month+day+"0000000"+str(counter+1)
        elif counter >9 and counter<=99:
            code=year+month+day+"000000"+str(counter+1)
        elif counter >99 and counter<=999:
            code=year+month+day+"00000"+str(counter+1)
        elif counter >999 and counter<=9999:
            code=year+month+day+"0000"+str(counter+1)
        elif counter >9999 and counter<=99999:
            code=year+month+day+"000"+str(counter+1)
        elif counter >99999 and counter<=999999:
            code=year+month+day+"00"+str(counter+1)
        elif counter >999999 and counter<=9999999:
            code=year+month+day+"0"+str(counter+1)
        elif counter >9999999 and counter<=99999999:
            code=year+month+day+str(counter+1)
        new = DTE(code,id_reference,emmiter_nit,reciever_nit,date_buffer,float(value),float(tax),float(total),"APROBADA")
        self.dte_array.append(new)
        day_dao_handler.new_day(date_buffer,float(value),float(total))
        nit_dao_handler.new_nit(emmiter_nit,date_buffer,float(0),float(tax))
        nit_dao_handler.new_nit(reciever_nit,date_buffer,float(tax),float(0))
        print("Se creo un nuevo DTE")
        
        return True
    def new_declined_dte(self,id_reference,emmiter_nit,reciever_nit,date,value,tax,total):
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
        new = DTE("none",id_reference,emmiter_nit,reciever_nit,date_buffer,float(value),float(tax),float(total),"REPROBADA")
        self.dte_array.append(new)
        print("se recivió un DTE Rechazado")
        day_dao_handler.new_day(date_buffer,float(value),float(total))
        return True

    def validate_reference(self,date,reference):
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
        reference_=reference.replace(" ","")
        if len(self.dte_array)!=0:
            for dte in self.dte_array:
                if dte.id_reference == reference_:
                    print('El Número de referencia ya existe, intente de nuevo!')
                    error_dao_handler.new_error(date_buffer,"DUPLICADO")
                    print("FALSE REFERENCE")
                    return False
                else:
                    print("TOOOODO BIEEEEN")
                    return True
        else:
            print("TOOOODO BIEEEEN")
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
            print("TODO BIEN EN CUANTO VALORES")
            return True
        elif tax_goal!=float(tax):
            error_dao_handler.new_error(date_buffer,"IVA")
            print("error iva")
            return False
        else:
            print("ERROR TOTAL")
            error_dao_handler.new_error(date_buffer,"TOTAL")
            return False
    
    #Función que valida los nits de emisores
    def validate_emitter_nit(self,date,nit):
        #Primero se recolecta la fecha
        nit=nit.replace(" ","")
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
        nit=nit.replace(" ","")
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
    

    def total_dte_counter_by_date(self,date):
        counter=0
        for dte in self.dte_array:
            if dte.date==date:
                counter+=1
        return counter
    def total_approved_dte_counter_by_date(self,date):
        counter=0
        for dte in self.dte_array:
            if dte.date==date and dte.state=="APROBADA":
                counter+=1
        return counter

        



    #Función básica que imprime en consola todos los "dte" validados existentes
    def print_all_dte(self):
        for dte in self.dte_array:
            if dte.state=="APROBADA":
                print(dte.id_reference,dte.emmiter_nit,dte.reciever_nit,dte.date,dte.value,dte.tax,dte.total,dte.state,dte.code)
    
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
    
    def emmiters_by_date(self,date):
        self.emmiters=[]
        for dte in self.dte_array:
            counter=0
            if dte.date==date and dte.state=="APROBADA":
                for c in self.emmiters:
                    if dte.emmiter_nit==c:
                        counter+=1
                if counter==0:
                    self.emmiters=[*self.emmiters,dte.emmiter_nit]
        return len(self.emmiters)

    def recievers_by_date(self,date):
        self.recievers=[]
        for dte in self.dte_array:
            counter=0
            if dte.date==date and dte.state=="APROBADA":
                for c in self.recievers:
                    if dte.reciever_nit==c:
                        counter+=1
                if counter==0:
                    self.recievers=[*self.recievers,dte.reciever_nit]
        return len(self.recievers)

    #Función que devuelve todos los DTE en base a su estado 
    def get_dte_by_state_and_date(self,state,date):
        if state=="APROBADA":
            return json.dumps([DTE.dump() for DTE in self.dte_array if DTE.state == "APROBADA" and DTE.date==date ]) 
        else:
            return json.dumps([DTE.dump() for DTE in self.dte_array if DTE.state == "REPROBADA" and DTE.date==date ]) 

    


    

    def xml_creator(self):
        route='C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/tools/out.xml'
        autorization_list=ET.Element("LISTAAUTORIZACIONES")
        for day in day_dao_handler.days:
            #VARIABLES TEMPORALES, QUE SE ACTUALIZARÁN POR CADA DÍA
            temporal_errors=[]
            day_totals=0
            temporal_errors=error_dao_handler.errors_counter_by_date(day.date)
            #SE CREA UNA AUTORIZACIÓN CADA DÍA
            autorization= ET.SubElement(autorization_list,"AUTORIZACION")
            #FECHA DEL DÍA QUE ESTÉ EN EL CICLO
            date= ET.SubElement(autorization,"FECHA")
            date.text=day.date
            #CANTIDAD DE FACTURAS RECIBIDAS
            day_totals=self.total_dte_counter_by_date(day.date)
            bills=ET.SubElement(autorization,"FACTURAS_RECIBIDAS")
            bills.text=str(day_totals)
            #ERRORES
            errors=ET.SubElement(autorization,"ERRORES")
            #ERRORES DE NIT DE EMISOR
            emmiter_nit_errors=ET.SubElement(errors,"NIT_EMISOR")
            emmiter_nit_errors.text=str(temporal_errors[0])
            #ERRORES DE NIT DE RECEPTOR
            reciever_nit_errors=ET.SubElement(errors,"NIT_RECEPTOR")
            reciever_nit_errors.text=str(temporal_errors[1])
            #ERRORES DE IVA
            tax_errors=ET.SubElement(errors,"IVA")
            tax_errors.text=str(temporal_errors[2])
            #ERRORES DE TOTALES
            total_errors=ET.SubElement(errors,"TOTAL")
            total_errors.text=str(temporal_errors[3])
            #ERRORES DE REFERENCIAS DUPLICADAS
            duplicate_errors=ET.SubElement(errors,"REFERENCIA_DUPLICADA")
            duplicate_errors.text=str(temporal_errors[4])
            #TOTAL DE DTES ACEPTADOS
            approved=0
            aprpoved_bills=ET.SubElement(autorization,"FACTURAS_CORRECTAS")
            approved=self.total_approved_dte_counter_by_date(day.date)
            aprpoved_bills.text=str(approved)
            #CANTIDAD DE EMISORES
            total_emmiters=0
            emmi=ET.SubElement(autorization,"CANTIDAD_EMISORES")
            total_emmiters=self.emmiters_by_date(day.date)
            emmi.text=str(total_emmiters)
            #CANTIDAD DE RECEPTORES
            total_recievers=0
            recie=ET.SubElement(autorization,"CANTIDAD_RECEPTORES")
            total_recievers=self.recievers_by_date(day.date)
            recie.text=str(total_recievers)
            #LISTADO DE AUTORIZACIONES
            autorizations=ET.SubElement(autorization,"LISTADO_AUTORIZACIONES")
            #CICLO DE APROBACIONES
            for dte in self.dte_array:
                if dte.date==day.date and dte.state=="APROBADA":
                    #EMPIEZA EL CICLO DE APROBACIONES POR DÍA
                    aprobation=ET.SubElement(autorizations,"APROBACION")
                    #CADA APROBACIÓN TIENE UN NIT DEL EMISOR
                    emmiter_n=ET.SubElement(aprobation,"NIT_EMISOR")
                    emmiter_n.set("ref",str(dte.id_reference))
                    emmiter_n.text=str(dte.emmiter_nit)
                    #CADA APROBACIÓN TIENE SU CÓDIGO
                    code=ET.SubElement(aprobation,"CODIGO_APROBACION")
                    code.text=str(dte.code)
                    tax_of_this=ET.SubElement(aprobation,"IVA")
                    tax_of_this.text=str(dte.tax)
                    provisional_nit=ET.SubElement(aprobation,"NIT_SIN_REFERENCIA")
                    provisional_nit.text=str(dte.emmiter_nit)
            total_approbations=ET.SubElement(autorizations,"TOTAL_APROBACIONES")
            total_approbations.text=str(approved)
        mydata= ET.tostring(autorization_list)
        mydata=str(mydata)
        self.prettify_xml(autorization_list)
        tree=ET.ElementTree(autorization_list)
        tree.write(route,encoding="UTF-8",xml_declaration=True)
        return True

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

    def nit_xml_creator(self):
        route='C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/tools/nits.xml'
        nits_list=ET.Element("LISTANITS")
        for day in day_dao_handler.days:
            #SE CREA UN LISTADO DE NITS POR CADA DÍA
            date_= ET.SubElement(nits_list,"FECHA")
            date_.text=day.date
            for nit in nit_dao_handler.nits_array:
                if nit.date==day.date:
                    register= ET.SubElement(date_,"REGISTRO")
                    nit_= ET.SubElement(register,"NIT")
                    nit_.text=nit.code
                    rec= ET.SubElement(register,"NIT_RECIBIDO")
                    rec.text=str(nit.recieved_nit)
                    emm= ET.SubElement(register,"NIT_EMITIDO")
                    emm.text=str(nit.emmited_nit)
        mydata= ET.tostring(nits_list)
        mydata=str(mydata)
        self.prettify_xml(nits_list)
        tree=ET.ElementTree(nits_list)
        tree.write(route,encoding="UTF-8",xml_declaration=True)
        return True
    
    def graphics_information(self):
        data = {}
        data['dte'] = []
        for dte in self.dte_array:
            if dte.state=="APROBADA":
                data['dte'].append({
                            'date' : dte.date,
                            'reference' : dte.id_reference,
                            'emmiter_nit' : dte.emmiter_nit,
                            'reciever_nit' : dte.reciever_nit,
                            'value' : dte.value,
                            'tax' : dte.tax,
                            'total' : dte.total
                        })
        with open('C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/tools/graphics_info.json', 'w', encoding='utf-8') as file:
            dataJson = json.dump(data, file, indent=4)


    def date_filter_recieved(self,date):
        nits=[]
        rec=[]
        for nit in nit_dao_handler.nits_array:
            if nit.date==date :
                nits=[*nits,nit.code]
                rec=[*rec,nit.recieved_nit]
        #nit_dao_handler.print_nits()
        #print(nits)
        #print(rec)
        colors=["blue","gray","purple","orange","yellow","green","red","pink","palegreen","lightgreen","olive","teal","cyan"]
        plt.title("RESUMEN DE IVA RECIBIDO POR CADA NIT EN LA FECHA: "+date)
        plt.bar(nits,height=rec,color=colors,width=0.5)
        plt.ylabel("Iva Recibido")
        plt.savefig("C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Front_End/Guatemalan_Tax_System/static/Guatemalan_Tax_System/images/recibido_fecha.png")
        plt.close()
        return "hola"
        #pyplot.show()

    def date_filter_emmited(self,date):
        nits=[]
        emm=[]
        for nit in nit_dao_handler.nits_array:
            if nit.date==date:
                nits=[*nits,nit.code]
                emm=[*emm,nit.emmited_nit]
        #print("")
        #print("")
        #print(nits)
        #print(emm)
        colors=["blue","gray","purple","orange","yellow","green","red","pink","palegreen","lightgreen","olive","teal","cyan"]
        plt.title("RESUMEN DE IVA EMITIDO POR CADA NIT EN LA FECHA: "+date)
        plt.bar(nits,height=emm,color=colors,width=0.5)
        plt.ylabel("Iva Emitido")
        plt.savefig("C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Front_End/Guatemalan_Tax_System/static/Guatemalan_Tax_System/images/emitido_fecha.png")
        plt.close()
        return "hola"
        #pyplot.show()
    def range_filter_total_with_iva(self):
        days=[]
        values=[]
        for day in day_dao_handler.days:
            values=[*values,day.total]
            days=[*days,day.date]
        print(days)
        print(values)
        colors=["blue","gray","purple","orange","yellow","green","red","pink","palegreen","lightgreen","olive","teal","cyan"]
        plt.title("RESUMEN DE TOTAL CON IVA ")
        plt.bar(days,height=values,color=colors,width=0.5)
        plt.ylabel("Total Con Iva")
        plt.savefig("C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Front_End/Guatemalan_Tax_System/static/Guatemalan_Tax_System/images/total_iva.png")
        plt.close()
        return "hola"

    def range_filter_total_without_iva(self):
        counter=0.00
        days=[]
        values=[]
        for day in day_dao_handler.days:
            values=[*values,day.value]
            days=[*days,day.date]
        print(days)
        print(values)
        colors=["blue","gray","purple","orange","yellow","green","red","pink","palegreen","lightgreen","olive","teal","cyan"]
        plt.title("RESUMEN DE TOTAL SIN IVA ")
        plt.bar(days,height=values,color=colors,width=0.5)
        plt.ylabel("Total Con Iva")
        plt.savefig("C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Front_End/Guatemalan_Tax_System/static/Guatemalan_Tax_System/images/total_siniva.png")
        plt.close()
        return "hola"