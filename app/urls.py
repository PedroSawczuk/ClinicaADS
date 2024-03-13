from django.urls import path

from app.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("relatorios/pacientes", PacientesListView.as_view(),
        name="relat_pacientes"),
    path('relatorios/pdf/pdfpacientes', RelatPdfPacientes.as_view(),
         name='pdf_pacientes'),
    
    path("relatorios/pacientes_por_convenio", PacientesConvenioListView.as_view(),
        name="relat_pacientes_por_convenio"),
    path('relatorios/pdf/pdfpacientes_por_convenio', RelatPdfPacientesConvenio.as_view(),
         name='pdf_pacientes_por_convenio'),
    
    path("relatorios/consultas_por_especialidades", ConsultaEspecialidadeListView.as_view(),
        name="relat_consultas_por_especialidades"),
        path("relatorios/pdf/pdfconsultas_por_especialidades", RelatPdfEspecialidadeConsultas.as_view(),
        name="pdf_consultas_por_especialidades"),
    
    path("relatorios/atendimento_por_especialidade", AtendimentoEspecialidadeListView.as_view(),
        name="relat_atendimento_por_especialidade"),
        path("relatorios/pdf/pdfatendimento_por_especialidade", RelatPdfAtendimentoEspecialidadeListView.as_view(),
        name="pdf_atendimento_por_especialidade"),

]

