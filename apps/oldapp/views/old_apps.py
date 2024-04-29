import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
from ...management.models import Profile
from ..app.finanzas import DashFinanzas
from ...resource.constants import * 
from ...resource.helpers.make_handler_models import user_loggedin

class FinanzasBg(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)

        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashFinanzas(ip = IP, token=TOKEN, data_login= user_loggedin(profile)).finanzas_bg(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)
    
class FinanzasBap(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)

        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashFinanzas(ip = IP, token=TOKEN, data_login= user_loggedin(profile)).finanzas_balance_ap(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)

class FinanzasActivo(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)

        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashFinanzas(ip = IP, token=TOKEN, data_login= user_loggedin(profile)).finanzas_analisis_activo(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)

class FinanzasPasivo(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)

        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashFinanzas(ip = IP, token=TOKEN, data_login= user_loggedin(profile)).finanzas_analisis_pasivo(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)