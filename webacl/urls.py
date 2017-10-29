from django.conf.urls import url
from webacl import views

app_name = 'webacl'

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^login/success/$', views.LoginSuccessView.as_view()),
    url(r'^login/failure/$', views.LoginFailureView.as_view()),
]