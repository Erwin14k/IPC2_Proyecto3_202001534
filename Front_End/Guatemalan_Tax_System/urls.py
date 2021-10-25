from django.urls import path
from Guatemalan_Tax_System import views

urlpatterns = [
    path("",views.home, name="Home"),
    path("upload",views.upload, name="Upload"),
    path("date_filter",views.date_filter, name="Date_filter"),
    path("help",views.help, name="Help"),
    path("send",views.send ,name="Send"),
    path("get_output_xml",views.get_output_xml ,name="Get_output_xml"),
    path("documentation",views.documentation ,name="Documentation"),
]