from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User,AbstractUser

class SuperAdmMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id = self.request.user.id)
        if user.is_superuser == 'True':
            return super().dispatch(request, *args, **kwargs)
        return redirect('home_old')