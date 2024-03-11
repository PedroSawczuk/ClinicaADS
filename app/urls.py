from django.urls import path

from app.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("relatorios/pacientes", PacientesListView.as_view(),
        name="relat_pacientes"),
    path('relatorios/pdf/pdfpacientes', RelatPdfPacientes.as_view(),
         name='pdf_pacientes'),
]

