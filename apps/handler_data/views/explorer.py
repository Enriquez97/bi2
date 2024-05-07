from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy

from ...resource.utils.identifiers import code_dashboard
from ..app.explorer_data import DashExplorerData
from ..models import DataConfig, StoreProcedure
from backend.mixins import SuperAdmMixin

ip_ = '68.168.108.10'
token_ = '0U10F10O10S10F10M10D10X10Z1lpu0N10O10H10T10I1sgk0Q10D10N10D10O10Z1lpu0T10o10d10e10i10z10x10b1lpu0S10n10r10N1rtg0I10Q1njh0M10J10q10I1lpumkimkiqwslpuertsdfasdasdlpuertnjhertqwsdfgnjhmkidfgloinjhmkiloisdf'

class ExplorerData(LoginRequiredMixin,SuperAdmMixin,View): #LoginRequiredMixin,
    #login_url = reverse_lazy('login')
    template_name = 'explorer.html'
    def get(self,request):
        sp_model = StoreProcedure.objects.filter(config_id=None)# MiModelo.objects
        identifiers = code_dashboard(ruc = '10728021859',user='1')
        dashboard = DashExplorerData(ip=ip_,token = token_,)
        app = dashboard.create_app(code = identifiers,model = sp_model)
        
        return render(request, 'handler.html',{'dashboard':app,'code': identifiers})