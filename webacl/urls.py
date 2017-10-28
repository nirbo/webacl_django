from django.conf.urls import url
from webacl import views

app_name = 'webacl'

urlpatterns = [
    url(r'^$', views.index, name='index')
]