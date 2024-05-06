import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
from ...management.models import Profile
from ..app.finanzas import DashFinanzas
from ..app.home import DashHomeOld
from ..app.logistica import DashLogistica
from ..app.comercial import DashComercial
from ...resource.constants import * 
from ...resource.helpers.make_handler_models import user_loggedin

class HomeOld(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        #profile = Profile.objects.get(user_id = self.request.user.id)
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashHomeOld(
                #ip = profile.company.ip, 
                #token = profile.company.token
            ).index(code = code),
            'code': code
        }
        return render(request,'home_.html',context)

#################FINANZAS
class FinanzasBg(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashFinanzas(
                ip = profile.company.ip, 
                token = profile.company.token
            ).finanzas_bg(code = code),
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
            'dashboard': DashFinanzas(
                ip = profile.company.ip, 
                token = profile.company.token, 
            ).finanzas_balance_ap(code = code),
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
            'dashboard': DashFinanzas(
                ip = profile.company.ip, 
                token = profile.company.token
            ).finanzas_analisis_activo(code = code),
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
            'dashboard': DashFinanzas(
                ip = profile.company.ip, 
                token = profile.company.token
            ).finanzas_analisis_pasivo(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)
    

#################LOGISTICA
class LogisticaStocks(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)
        context = {
            'dashboard': DashLogistica(
                ip = profile.company.ip, 
                token = profile.company.token
            ).logistica_stocks(code = code),
            'code': code
        }
        return render(request,'logistica.html',context)

class EstadoInventario(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)

        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashLogistica(
                ip = profile.company.ip, 
                token = profile.company.token
            ).estado_inventario(code = code),
            'code': code
        }
        return render(request,'logistica.html',context)
    
class GestionStocks(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)

        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashLogistica(
                ip = profile.company.ip, 
                token = profile.company.token
            ).gestion_stock(code = code),
            'code': code
        }
        return render(request,'logistica.html',context)
    
###############################################
class InformeVentas(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)

        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashComercial(
                ip = profile.company.ip, 
                token = profile.company.token
            ).comercial_informe(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)
    

class ResumenVentas(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)

        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashComercial(
                ip = profile.company.ip, 
                token = profile.company.token
            ).resumen_ventas(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)