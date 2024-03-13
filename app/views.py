from io import BytesIO
import os
from django.shortcuts import render
from django.views.generic import *
from app.models import *
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.db.models import Count
from datetime import datetime
from django.db.models.functions import ExtractMonth
from django.db.models import Count, F

class HomeView(TemplateView):
    template_name = 'index.html'
    
class PacientesListView(ListView):
    template_name = 'relatorios/pacientes.html'
    model = Paciente
    context_object_name = 'pacientes'
    
class RelatPdfPacientes(View):
    
    def get(self, request):
        pacientes = Paciente.objects.all()
        data = {
            'pacientes': pacientes,
        }
        
        template = get_template("relatorios/pdf/pdfpacientes.html")
        html = template.render(data)
        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
            return HttpResponse(result.getvalue(),
                                content_type='application/pdf')
        except Exception as e:
            print(e)
            return None
    
class PacientesConvenioListView(ListView):
    template_name = 'relatorios/pacientes_por_convenio.html'
    model = Convenio
    context_object_name = 'convenios'
    
    def get_queryset(self):
        # Recuperar todos os convênios
        convenios = Convenio.objects.all()
        # Iterar sobre os convênios e anotar os pacientes associados a cada um
        for convenio in convenios:
            pacientes = Paciente.objects.filter(possui__convenio=convenio)
            convenio.pacientes = pacientes
        return convenios
        
class RelatPdfPacientesConvenio(View):

    def get(self, request):
        convenios = Convenio.objects.all()
        for convenio in convenios:
            pacientes = Paciente.objects.filter(possui__convenio=convenio)
            convenio.pacientes = pacientes
        
        data = {
            'convenios': convenios,
            'pacientes': pacientes,
        }
        
        template = get_template("relatorios/pdf/pdfpacientes_por_convenio.html")  # Ajustado o caminho do template
        html = template.render(data)
        response = HttpResponse(content_type='application/pdf')
        
        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
            response.write(result.getvalue())
            return response
        except Exception as e:
            print(e)
            return None
        
class ConsultaEspecialidadeListView(ListView):
    model = Consulta
    template_name = 'relatorios/consultas_por_especialidade_mes.html'
    context_object_name = 'consultas_por_especialidade'

    def get_queryset(self):
        return Consulta.objects.values('medico__especialidade').annotate(total=Count('id')).order_by('medico__especialidade')
    
            
class RelatPdfEspecialidadeConsultas(View):

    def get(self, request):
        
        consultas_por_especialidade = Consulta.objects.values('medico__especialidade').annotate(total=Count('id')).order_by('medico__especialidade')
        
        data = {
            'consultas_por_especialidade': consultas_por_especialidade,
        }
        
        template = get_template("relatorios/pdf/pdfconsultas_por_especialidades.html")  # Ajustado o caminho do template
        html = template.render(data)
        
        response = HttpResponse(content_type='application/pdf')
        
        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
            if not pdf.err:
                response.write(result.getvalue())
                return response
        except Exception as e:
            print(e)
        
        return HttpResponse('Ocorreu um erro ao gerar o PDF.', content_type='text/plain')