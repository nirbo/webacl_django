from django.conf.urls import url
from webacl import views

app_name = 'webacl'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^login/success/$', views.login_success, name='login_success'),
    url(r'^login/failure/$', views.login_failure, name='login_failure'),
]
