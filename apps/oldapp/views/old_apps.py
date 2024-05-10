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
from asgiref.sync import sync_to_async
from backend.connector import APIConnector
from ...resource.utils.data import decoding_avatar,status_cliente


class HomeOld(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)
        values_login = {}
        values_login["name_user"] = profile.name +" "+ profile.surname
        values_login["empresa"] = profile.company.description
        values_login["rol"] = profile.role.description
        values_login["rubro"] = profile.company.category.description
        values_login["avatar_profile"] = decoding_avatar(profile.avatar_profile,400,400)
        values_login["status_service"] = status_cliente(profile.company.ip)
        
        context = {
            'dashboard': DashHomeOld(
                #ip = profile.company.ip, 
                #token = profile.company.token
            ).index(code = code, user_index = values_login),
            'code': code,
            
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
        df = APIConnector( 
            ip = profile.company.ip, 
            token = profile.company.token
        ).send_get_dataframe(endpoint="nsp_rpt_ventas_detallado", params=None)
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashComercial(
                dataframe = df, 
            ).comercial_informe(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)
    

class ResumenVentas(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)
        df = APIConnector( 
            ip = profile.company.ip, 
            token = profile.company.token
        ).send_get_dataframe(endpoint="nsp_rpt_ventas_detallado", params=None)
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashComercial(
                dataframe = df,
            ).resumen_ventas(code = code),
            'code': code
        }
        return render(request,'comercial.html',context)