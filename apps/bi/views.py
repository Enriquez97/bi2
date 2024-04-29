from django.shortcuts import render
from apps.bi.app.home import example_dash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
from dash import Dash, dcc, Input, Output, dash_table, callback
import dash_mantine_components as dmc
import plotly.express as px
from django_plotly_dash import DjangoDash

ip_ = '68.168.108.10'

import requests
from celery import shared_task
@shared_task
def getApi(token):
    response = requests.get("http://68.168.108.10:3005/api/consulta/nsp_etl_situacion_financiera", headers={'Authorization': "Bearer {}".format(token)})
    objeto=response.json()
    list_objetos=objeto['objeto']
    return list_objetos
@login_required
def home(request):
    token_ = '0U10F10O10S10F10M10D10X10Z1lpu0N10O10H10T10I1sgk0Q10D10N10D10O10Z1lpu0T10o10d10e10i10z10x10b1lpu0S10n10r10N1rtg0I10Q1njh0M10J10q10I1lpumkimkiqwslpuertsdfasdasdlpuertnjhertqwsdfgnjhmkidfgloinjhmkiloisdf'
    
    import pandas as pd
    g = getApi(token = token_)
    print(pd.DataFrame(g))
    return render(request, 'home.html',{'dashboard':example_dash()})