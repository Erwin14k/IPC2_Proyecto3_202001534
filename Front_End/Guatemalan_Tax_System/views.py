from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage

#All views

def home(request):
    return render(request,"Guatemalan_Tax_System/home.html")

def upload(request):
    context = {}
    if request.method == 'POST':
        xml_upload_file = request.FILES['document']
        route = xml_upload_file.name
        file_storage =  FileSystemStorage()
        file_storage.save(route, xml_upload_file)
        #Se obtiene la ruta del archivo xml 
        local_route = "C:/Users/Erwin14k/Desktop/"
        local_route = local_route + route
        
        text_area = ""
        with open(local_route, 'r', encoding='utf-8') as c:
            lines = c.readlines()
            print(lines)
            for content in lines:
                content.rstrip('\n')
                text_area = text_area + content
                print(content)
        context['isEmpty'] = text_area       
        print(local_route)
    return render(request,"Guatemalan_Tax_System/upload.html",context)




def petitions(request):
    return render(request,"Guatemalan_Tax_System/petitions.html")

def help(request):
    return render(request,"Guatemalan_Tax_System/help.html")


