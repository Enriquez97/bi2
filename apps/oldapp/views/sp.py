import uuid
from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from ...management.models import Profile
from ...handler_data.models import StoreProcedure
from backend.mixins import SuperAdmMixin
from backend.connector import fetch_data_from_api
from asgiref.sync import sync_to_async
from ...oldapp.app.data_show import dashShowSP
from django_plotly_dash import DjangoDash
from datetime import datetime,timedelta
import json

class ShowAPI(View):#LoginRequiredMixin,SuperAdmMixin,
    
    async def get(self, request,sp):#async 
        unique_id = str(uuid.uuid4())
        model_data = await sync_to_async(self.get_model_data)(sp)#await sync_to_async(
        
        data_api = await fetch_data_from_api(
            model_data["ip"],model_data["token"],sp, model_data["parameters"]
        )
        api_data_json = json.dumps(data_api, indent=4)
        #app = DjangoDash(name = "test")
        return render(request, 'apis.html',{'unique_id': unique_id, 'api_data_json': api_data_json})#,#'dashboard':app,
    
    def get_model_data(self,sp_name):
        profile = Profile.objects.get(user_id = self.request.user.id)
        sp_model = StoreProcedure.objects.get(sp_name = sp_name)
        sp_parameters = sp_model.parameters
        values_model_user = {}
        values_model_user["ip"] = profile.company.ip
        values_model_user["token"] = profile.company.token
        values_model_user["parameters"] = None if sp_parameters == "" else eval(sp_parameters)
        return values_model_user
    

class NewTheme(View):
    def get(self, request):
        code = str(uuid.uuid4())
        #profile = Profile.objects.get(user_id = self.request.user.id)
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': dashShowSP(code=code),
            'code': code
        }
        return render(request,'test.html',context)