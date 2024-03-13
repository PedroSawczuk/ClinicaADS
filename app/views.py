from django.views.generic import *
from app.models import *
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.db.models import Count
from django.db.models.functions import *
from django.db.models import Count, F
from django.template.loader import render_to_string

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
        convenios = Convenio.objects.all()
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
        
        template = get_template("relatorios/pdf/pdfpacientes_por_convenio.html") 
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
        
        template = get_template("relatorios/pdf/pdfconsultas_por_especialidades.html") 
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
        
class AtendimentoEspecialidadeListView(ListView):
    template_name = 'relatorios/atendimento_por_especialidade.html'
    context_object_name = 'atendimento_por_especialidade'

    def get_queryset(self):
        especialidades = Medico.objects.values_list('especialidade', flat=True).distinct()

        atendimentos_por_especialidade = []
        for especialidade in especialidades:
            atendimentos = Consulta.objects.filter(medico__especialidade=especialidade).annotate(month=ExtractMonth('data'),
                                                      year=ExtractYear('data'))\
                                            .values('month', 'year')\
                                            .annotate(total=Count('id'))
            atendimentos_por_especialidade.append({'especialidade': especialidade, 'atendimentos': atendimentos})

        return atendimentos_por_especialidade
    
class RelatPdfAtendimentoEspecialidadeListView(View):
    
    def get(self, request):
        atendimento_por_especialidade = AtendimentoEspecialidadeListView().get_queryset()

        html_string = render_to_string('relatorios/pdf/pdfatendimento_por_especialidade.html', {'atendimento_por_especialidade': atendimento_por_especialidade})

        result = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            return response

        return HttpResponse('Erro ao gerar PDF: %s' % pdf.err)