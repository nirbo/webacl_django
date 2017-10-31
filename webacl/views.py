import logging

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from webacl.forms import LoginForm
from webacl.models import Node
import hashlib
import datetime
import uuid
from django.conf import settings

from webacl.utils import generate_token, get_client_ip, authenticate_node

logger = logging.getLogger(__name__)


def register(request, token):
    node = generate_token(token, get_client_ip(request))

    if node:
        return JsonResponse({'password': node.password, 'username': node.username, 'message': 'Access granted'}, status=200)
    else:
        return JsonResponse({'message': 'Request rejected'}, status=403)


def login(request, username=None, password=None):
    """
    You can pass username and password as arguments
    :param request:
    :param username:
    :param password:
    :return:
    """

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            # if login is valid we grant the access
            authenticate_node(get_client_ip(request))
            return JsonResponse({'message': 'Access granted'}, status=200)
        else:
            return JsonResponse({'message': 'Request rejected'}, status=403)
    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'webacl/login.html', context)







