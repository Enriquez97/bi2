from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


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