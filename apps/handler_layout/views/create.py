import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy

from ...resource.utils.identifiers import code_dashboard
from ..app.create_layout import DashCreateLayout
from ..app.show_layout import DashShowLayout
from ...handler_data.models import StoreProcedure
from ..models import KPI

ip_ = '68.168.108.10'
token_ = '0U10F10O10S10F10M10D10X10Z1lpu0N10O10H10T10I1sgk0Q10D10N10D10O10Z1lpu0T10o10d10e10i10z10x10b1lpu0S10n10r10N1rtg0I10Q1njh0M10J10q10I1lpumkimkiqwslpuertsdfasdasdlpuertnjhertqwsdfgnjhmkidfgloinjhmkiloisdf'

class CreateLayout(View):
    template_name = 'create.html'
    def get(self,request):
        #owo =DataConfig.objects.all()
        sp_model = StoreProcedure.objects.exclude(config = None)
        #list_data_config =[[fila.config] for fila in owo]
        list_sp = [fila.sp_name for fila in sp_model]
        identifiers = code_dashboard(ruc = '10728021859',user='1')
        dashboard = DashCreateLayout(ip=ip_,token = token_)
        app = dashboard.create_app(code = identifiers,sp=list_sp)
        return render(request, 'create.html',{'dashboard':app,'code': identifiers})


class ShowLayout(View):
    def get(self,request):
        #owo =DataConfig.objects.all()
        kpi_layout = KPI.objects.all()
        #kpi_layout_list_fig = [fila.figure for fila in kpi_layout]
        #kpi_layout_list_name = [fila.name for fila in kpi_layout]
        list_df = [[fila.figure,fila.name,fila.sp.sp_name ]for fila in kpi_layout]
        df = pd.DataFrame(list_df, columns = ["figure","name_kpi","name_sp"])
        #list_data_config =[[fila.config] for fila in owo]
        identifiers = code_dashboard(ruc = '10728021859',user='1')
        dashboard = DashShowLayout()
        app = dashboard.create_app(code = identifiers, kpi_df = df)
        return render(request, 'create.html',{'dashboard':app,'code': identifiers})