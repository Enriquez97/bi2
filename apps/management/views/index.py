from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
import uuid
from ..models import Profile, Company
from ..app.home import DashHome
from ...resource.utils.data import decoding_avatar


class Home(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self,request):
        code = str(uuid.uuid4())
        profile = Profile.objects.get(user_id = self.request.user.id)
        values_login = {}
        values_login["name_user"] = profile.name +" "+ profile.surname
        values_login["avatar_profile"] = decoding_avatar(profile.avatar_profile,200,200)
        values_login["avatar_company"] = decoding_avatar(profile.company.avatar_profile,115,40)
        
        #print(profile.company.avatar_profile)
        context = {
            'dashboard': DashHome().create_app(code = code, data_login = values_login),
            'code': code
        }
        return render(request,'index.html',context)
    

class Error404View(TemplateView):
    template_name = "error_404.html"


class Error505View(TemplateView):
    template_name = "error_500.html"

    @classmethod
    def as_error_view(cls):

        v = cls.as_view()
        def view(request):
            r = v(request)
            r.render()
            return r
        return view