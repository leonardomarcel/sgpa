"""django_base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
#from django.conf.urls import url, include
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

from auth_local.auth_local import AuthLocal
from passagem.views.manter_painel import PainelView
#from publico.views.manter_publico import IndexPublica, PublicoErro404, PublicoErro400, PublicoErro403, PublicoErro500

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('basico/', include('basico.urls', namespace='basico')),
    path('', PainelView.as_view(), name="passagem"),
    
    
    #url(r'^cidadao/cadastro/', AuthLocal.cadastro_cidadao, name='cadastro_cidadao'),
    #url(r'^cidadao/login/', AuthLocal.login_cidadao, name='login_cidadao'),
    path('login/', AuthLocal.login, name='login'),
    path('logout/', AuthLocal.logout, name='logout'),
    
    #url(r'^publico/', include('publico.urls')),
     path('passagem/', include('passagem.urls', namespace='passagem')),
     path('relatorio/', include('relatorio.urls', namespace='relatorio')),
     path('auth_local/', include('auth_local.urls', namespace='auth_local')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
#handler400 = PublicoErro400.as_view()
#handler403 = PublicoErro403.as_view()
#handler404 = PublicoErro404.as_view()
#handler500 = PublicoErro500.as_view()