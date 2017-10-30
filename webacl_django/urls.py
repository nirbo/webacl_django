from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from webacl.views import login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('webacl.urls')),
    # All login
    url(r'^', login, name='login'),
]
