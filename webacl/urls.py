from django.conf.urls import url
from webacl import views

app_name = 'webacl'

urlpatterns = [
    url(r'^register/(?P<token>.*)$', views.register, name='register'),
    url(r'^login/(?P<username>[0-9a-zA-Z\-\_]+)/(?P<password>[0-9a-zA-Z\-\_]+)$', views.login, name='login'),
]
