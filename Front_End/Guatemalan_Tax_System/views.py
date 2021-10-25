from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from . import controller
import json
import requests
from django.http import FileResponse

#All views

def home(request):
    return render(request,"Guatemalan_Tax_System/home.html")
context_upload = {}
def upload(request):
    
    if request.method == 'POST':
        xml_upload_file = request.FILES['document']
        route = xml_upload_file.name
        file_storage =  FileSystemStorage()
        #file_storage.save(route, xml_upload_file)
        #Se obtiene la ruta del archivo xml 
        local_route = "C:/Users/Erwin14k/Desktop/"
        local_route = local_route + route
        
        text_area = ""
        with open(local_route, 'r', encoding='utf-8') as c:
            lines = c.readlines()
            #print(lines)
            for content in lines:
                content.rstrip('\n')
                text_area = text_area + content
                print(content)
        context_upload['isEmpty'] = text_area       
        controller.xml_to_jason(local_route)
    return render(request,"Guatemalan_Tax_System/upload.html",context_upload)

context_ouput_xml = {}
def get_output_xml(request):
    if request.method == 'POST':
        text_area = ""
        with open("C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Tools/out.xml", 'r', encoding='utf-8') as c:
            lines = c.readlines()    
            for content in lines:
                content.rstrip('\n')
                text_area = text_area + content
                print(content)
        context_ouput_xml['isEmpty2'] = text_area       
    return render(request,"Guatemalan_Tax_System/upload.html",context_ouput_xml)

def send(request):
    #print("se llega aquí 1")
    if request.method == "POST":
        #print("se llega aquí 2")
        zelda = 'http://127.0.0.1:5000/send'
        route = "C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Tools/data.json"
        #print("se llega aquí3")
        with open(route, 'r') as file:
            contents = json.loads(file.read())
        #print("se llega aquí")
        response = requests.post(zelda, json=contents)
        print("Informacion enviada para validar en el backend!!!")
        return render(request, 'Guatemalan_Tax_System/upload.html')

def documentation(request):
    url = "C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Ensayo/ejemplo.pdf"
    response = FileResponse(open(url, 'rb'), content_type='application/pdf')
    return response

def date_filter(request):
    date = {}
    
    if request.method == 'GET':
        dates_list = []
        direction = "http://127.0.0.1:5000/date_filter"
        response = requests.get(direction)
        data = response.json()
        obj = json.loads(data)
        
        for datum in obj:
            try:
                for x in range(0,100):
                    print(datum,"0000")
                    key = obj[datum]['AUTORIZACION'][x]['FECHA']
                    print(key)
                    dates_list.append(key)
            except IndexError:
                print("noooooooo")
                pass
        date['date'] = dates_list
    
    return render(request, 'Guatemalan_Tax_System/date_filter.html', context={"date": date})




def petitions(request):
    return render(request,"Guatemalan_Tax_System/petitions.html")

def help(request):
    return render(request,"Guatemalan_Tax_System/help.html")


