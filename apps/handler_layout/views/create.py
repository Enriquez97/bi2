import pandas as pd
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy

from ...resource.utils.identifiers import code_dashboard
from ..app.create_layout import DashCreateLayout
from ..app.show_layout import DashShowLayout
from ...handler_data.models import StoreProcedure
from ..models import KPI
from backend.mixins import SuperAdmMixin
from ...management.models import Profile


class CreateLayout(LoginRequiredMixin,SuperAdmMixin,View):
    template_name = 'create.html'
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)
        sp_model = StoreProcedure.objects.exclude(config = None)
        list_sp = [fila.sp_name for fila in sp_model]
        dashboard = DashCreateLayout(ip=profile.company.ip,token = profile.company.token)
        app = dashboard.create_app(code = code,sp=list_sp)
        return render(request, 'create.html',{'dashboard':app,'code': code})


class ShowLayout(LoginRequiredMixin,SuperAdmMixin,View):
    def get(self,request):
        code = str(uuid.uuid4())
        #owo =DataConfig.objects.all()
        kpi_layout = KPI.objects.all()
        #kpi_layout_list_fig = [fila.figure for fila in kpi_layout]
        #kpi_layout_list_name = [fila.name for fila in kpi_layout]
        list_df = [[fila.figure,fila.name,fila.sp.sp_name ]for fila in kpi_layout]
        df = pd.DataFrame(list_df, columns = ["figure","name_kpi","name_sp"])
        #list_data_config =[[fila.config] for fila in owo]
        dashboard = DashShowLayout()
        app = dashboard.create_app(code = code, kpi_df = df)
        return render(request, 'create.html',{'dashboard':app,'code': code})