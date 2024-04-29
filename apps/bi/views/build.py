import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
from ...resource.utils.data import decoding_avatar
from ...management.models import Profile
from ...bi.app.create_dash import DashCreate
from ...bi.app.build_dash import DashBuild
from ...handler_data.models import StoreProcedure
from ...bi.models import Dashboard



class CreateDash(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        sp_model = StoreProcedure.objects.exclude(config = None)
        profile = Profile.objects.get(user_id = self.request.user.id)
        values_login = {}
        values_login["name_user"] = profile.name +" "+ profile.surname
        values_login["avatar_profile"] = decoding_avatar(profile.avatar_profile,200,200)
        values_login["avatar_company"] = decoding_avatar(profile.company.avatar_profile,115,40)
        
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashCreate().create_app(code = code, data_login = values_login, model_sp = sp_model),
            'code': code
        }
        return render(request,'home.html',context)
    
    

class BuildDash(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)
        dashboard_build = Dashboard.objects.all()
        
        diccionario = {obj.name: obj.dashboard_layout for obj in dashboard_build}
        print(diccionario)
        values_login = {}
        values_login["name_user"] = profile.name +" "+ profile.surname
        values_login["avatar_profile"] = decoding_avatar(profile.avatar_profile,200,200)
        values_login["avatar_company"] = decoding_avatar(profile.company.avatar_profile,115,40)
        
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashBuild().create_app(code = code, data_login = values_login,dash_create =eval(diccionario["Dashboard Save"])),
            'code': code
        }
        return render(request,'home.html',context)