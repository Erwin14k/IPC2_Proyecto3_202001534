from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from . import controller
import json
import requests

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

def send(request):
    #print("se llega aquí 1")
    if request.method == "POST":
        #print("se llega aquí 2")
        zelda = 'http://127.0.0.1:5000/send'
        ruta = "C:/Users/Erwin14k/Documents/IPC2_Proyecto3_202001534/Tools/data.json"
        #print("se llega aquí3")
        with open(ruta, 'r') as file:
            contents = json.loads(file.read())
        #print("se llega aquí")
        response = requests.post(zelda, json=contents)
        print("Informacion enviada para validar en el backend!!!")
        return render(request, 'Guatemalan_Tax_System/upload.html')




def petitions(request):
    return render(request,"Guatemalan_Tax_System/petitions.html")

def help(request):
    return render(request,"Guatemalan_Tax_System/help.html")


