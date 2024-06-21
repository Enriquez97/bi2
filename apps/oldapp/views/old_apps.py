import uuid
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.urls import reverse_lazy
from ...management.models import Profile
from ..app.finanzas import DashFinanzas
from ..app.home import DashHomeOld
from ..app.logistica import DashLogistica
from ..app.comercial import DashComercial
from ..app.produccion import DashProduccion
from ...resource.constants import * 
from ...resource.helpers.make_handler_models import user_loggedin
from asgiref.sync import sync_to_async
from backend.connector import APIConnector
from ...resource.utils.data import decoding_avatar,status_cliente
from datetime import datetime,timedelta

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
        values_login["is_superuser"] = profile.user.is_superuser
        values_login["is_staff"] =profile.user.is_staff
        
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
    
class AgricolaCampania(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashProduccion().ejecucion_campania(code = code),
            'code': code
        }
        return render(request,'produccion.html',context)
       
    
    
    
    
    
    
###TEST

import httpx
import pandas as pd
url_api = "http://64.150.180.23:3005/api/consulta/nsp_etl_situacion_financiera"
token = "0G10O10F10F10Q10T10O10A10D10M10N1lpu0N10O10H10G10T1sgk0Q10D10N10D10O10Z1lpu0q10d10n10d10o10z1lpu0B10m10K10r10z1asd0C1sdf0Z10S10Y10i1qws0u1lpumkimkiertlpuertsdfasdasdlpuertnjhertbhgloiasddfgnjhnjhbhgloirtgmki"


async def fetch_data_from_api(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()  # Esto lanzará una excepción si la respuesta no es 2xx
        obj = response.json()
        obj_ = obj['objeto']
        return pd.DataFrame(obj_)
    
class AsyncHomeView(View):
    async def get(self, request):

        try:
            data = await fetch_data_from_api(url = url_api, token = token)
        except httpx.HTTPStatusError as e:
            data = {'error': f'Error al consumir la API externa: {e.response.status_code}'}
        except httpx.RequestError as e:
            data = {'error': f'Error de solicitud: {str(e)}'}
        print(data)
        return render(request, 'test.html')
