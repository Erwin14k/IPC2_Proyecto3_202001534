from django.urls import path
from Guatemalan_Tax_System import views

urlpatterns = [
    path("",views.home, name="Home"),
    path("upload",views.upload, name="Upload"),
    path("petitions",views.petitions, name="Petitions"),
    path("help",views.help, name="Help"),
    path("send",views.send ,name="Send"),
]