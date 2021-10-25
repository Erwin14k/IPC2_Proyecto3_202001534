from xml.dom import minidom
import json



def xml_to_jason(route):
    data = {}
    data['dte'] = []
    xml_file = minidom.parse(route)
    dtes = xml_file.getElementsByTagName('DTE')
    for dte in dtes:
        false_counter=0
        try:
            if dte.getElementsByTagName("TIEMPO")[0].childNodes[0].data!=None:
                false_counter=false_counter
        except:
            print("No se pudo")
            false_counter+=1
            pass
        try:
            if dte.getElementsByTagName("REFERENCIA")[0].childNodes[0].data!=None:
                false_counter=false_counter
        except:
            print("No se pudo")
            false_counter+=1
            pass

        try:
            if dte.getElementsByTagName("NIT_EMISOR")[0].childNodes[0].data!=None:
                false_counter=false_counter
        except:
            print("No se pudo")
            false_counter+=1
            pass
        
        try:
            if dte.getElementsByTagName("NIT_RECEPTOR")[0].childNodes[0].data!=None:
                false_counter=false_counter
        except:
            print("No se pudo")
            false_counter+=1
            pass

        try:
            if dte.getElementsByTagName("VALOR")[0].childNodes[0].data!=None:
                false_counter=false_counter
        except:
            print("No se pudo")
            false_counter+=1
            pass

        try:
            if dte.getElementsByTagName("IVA")[0].childNodes[0].data!=None:
                false_counter=false_counter
        except:
            print("No se pudo")
            false_counter+=1
            pass

        try:
            if dte.getElementsByTagName("TOTAL")[0].childNodes[0].data!=None:
                false_counter=false_counter
        except:
            print("No se pudo")
            false_counter+=1
            pass
        if false_counter==0:
            date = dte.getElementsByTagName("TIEMPO")[0].childNodes[0].data
            reference = dte.getElementsByTagName("REFERENCIA")[0].childNodes[0].data
            emmiter_nit = dte.getElementsByTagName("NIT_EMISOR")[0].childNodes[0].data 
            reciever_nit = dte.getElementsByTagName('NIT_RECEPTOR')[0].childNodes[0].data 
            value = dte.getElementsByTagName('VALOR')[0].childNodes[0].data 
            tax = dte.getElementsByTagName('IVA')[0].childNodes[0].data 
            total = dte.getElementsByTagName('TOTAL')[0].childNodes[0].data
            print(reference,"=000000000000000000000000000000000000000000")
            data['dte'].append({
                            'date' : date,
                            'reference' : reference,
                            'emmiter_nit' : emmiter_nit,
                            'reciever_nit' : reciever_nit,
                            'value' : value,
                            'tax' : tax,
                            'total' : total
                        })
        else:
            print("Pasemos al siguiente")
    with open('C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/tools/data.json', 'w', encoding='utf-8') as file:
        dataJson = json.dump(data, file, indent=4)