from django.urls import path
from . import views


urlpatterns = [
    path('',views.csvFileExport, name="csv_form"),
    path('export_data_in_excel/',views.exportDataInExcel, name="export_data_in_excel"),
]