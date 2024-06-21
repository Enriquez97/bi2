from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
import uuid
from ...resource.utils.identifiers import code_dashboard
from ..app.explorer_data import DashExplorerData
from ..models import DataConfig, StoreProcedure
from backend.mixins import SuperAdmMixin
from ...management.models import Profile

class ExplorerData(LoginRequiredMixin,SuperAdmMixin,View): #LoginRequiredMixin,
    #login_url = reverse_lazy('login')
    template_name = 'explorer.html'
    
    def get(self,request):
        code = str(uuid.uuid4())
        sp_model = StoreProcedure.objects.filter(config_id=None)# MiModelo.objects
        profile = Profile.objects.get(user_id = self.request.user.id)
        dashboard = DashExplorerData(ip=profile.company.ip,token = profile.company.token,)
        app = dashboard.create_app(code = code,model = sp_model)
        
        return render(request, 'handler.html',{'dashboard':app,'code': code})