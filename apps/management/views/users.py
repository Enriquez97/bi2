import uuid
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ...management.app.forms import DashFormUser
from django.contrib.auth.models import User
from backend.mixins import SuperAdmMixin
from ..models import Role,Profile,Company,Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from ...resource.utils.data import *


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
                login(request, user)
                return redirect('home_old')#('/cuentas_por_pagar/')
        else:
                return render(request,'login.html',{'error':'Invalid username and password'})
    return render (request,'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

#### FORMS DASH 
class FormNewuserDash(LoginRequiredMixin,View):
    def get(self,request):
        data_inputs = {}
        code = str(uuid.uuid4())
        rol = Role.objects.all()
        user = User.objects.get(pk =  self.request.user.id)
        if user.is_staff == True and user.is_superuser == True and user.is_active == True:
            company = Company.objects.all()
            data_inputs['empresas'] = [(str(fila.id), fila.description) for fila in company]
            data_inputs['empresa_'] = None
            data_inputs['disabled_select'] = False
            
        else:
            profile = Profile.objects.get(user_id = user.pk)
            data_inputs['empresas'] = [(str(profile.company.id), profile.company.description)]
            data_inputs['empresa_'] = str(profile.company.id)
            data_inputs['disabled_select'] = True
            #print(profile.company.description)
        #print(type(profile.company.id))
        data_inputs['roles'] = [(str(fila.id), fila.description) for fila in rol]
        context = {
                'dashboard': DashFormUser(
                    #ip = profile.company.ip, 
                    #token = profile.company.token
                ).app_form_new_user(code = code, data_inputs = data_inputs),# user_index = values_login
                'code': code,
                
                
            }
        return render (request,'forms.html',context)


class FormNewCompanyDash(LoginRequiredMixin,SuperAdmMixin,View):
    def get(self,request):
        data_inputs = {}
        code = str(uuid.uuid4())
        rubro = Category.objects.all()
        data_inputs['rubros'] = [(str(fila.id), fila.description) for fila in rubro]
        context = {
                'dashboard': DashFormUser(
                    #ip = profile.company.ip, 
                    #token = profile.company.token
                ).app_form_new_company(code = code, data_inputs = data_inputs),#, data_inputs = data_inputs
                'code': code,
                
                
            }
        return render (request,'forms.html',context)
    

class ShowUsuarios(LoginRequiredMixin,View):
    def get(self,request):
        usuariox =User.objects.get(pk =  self.request.user.id)
        if usuariox.is_staff == True and usuariox.is_superuser == True and usuariox.is_active == True:
            profile = Profile.objects.all()
        else:
            profile = Profile.objects.filter(user_id = usuariox.pk)
        
        return render(request, 'usuarios.html',{'users':profile})#,{'empresas':lista_empresas,'roles':lista_roles}

        
class ShowEmpresa(LoginRequiredMixin,SuperAdmMixin,View):
    def get(self,request):
        usuariox =User.objects.get(pk =  self.request.user.id)
        if usuariox.is_staff == True and usuariox.is_superuser == True and usuariox.is_active == True:
            empresas = Company.objects.all()
            lista_ip = [status_cliente(fila.ip) for fila in empresas]
            empresas_ = zip(empresas,lista_ip)
            return render(request, 'empresas.html',{'empresas':empresas_})#,{'empresas':lista_empresas,'roles':lista_roles}
        else:
            return render(request, 'index.html')
        
    
class FormModuserDash(LoginRequiredMixin,View):
    def get(self,request,id):
        data_inputs = {}
        code = str(uuid.uuid4())
        rol = Role.objects.all()
        user = User.objects.get(pk =  self.request.user.id)
        profile = Profile.objects.get(pk = id)
        data_inputs['name_user'] = profile.user.username
        data_inputs['name_profile'] = profile.name
        data_inputs['surname_profile'] = profile.surname
        data_inputs['phone'] = profile.phone
        data_inputs['email']  = profile.user.email
        data_inputs['image'] = profile.avatar_profile
        data_inputs['rol'] = str(profile.role.id)
        data_inputs["is_active"] = profile.user.is_active
        data_inputs['roles'] = [(str(fila.id), fila.description) for fila in rol]
        data_inputs['id'] = id
        context = {
                'dashboard': DashFormUser(
                    #ip = profile.company.ip, 
                    #token = profile.company.token
                ).app_form_mod_user(code = code, data_inputs = data_inputs),# user_index = values_login
                'code': code,
                
                
            }
        return render (request,'forms.html',context)