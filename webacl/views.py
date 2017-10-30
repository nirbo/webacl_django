from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from webacl.forms import LoginForm
from webacl.models import Node
import hashlib
import datetime
import uuid

from django.conf import settings


def register(request, token):
    generate_token(request, get_client_ip(request))

    context = {'token': token}
    return render(request, 'webacl/register.html', context)


def login(request, username=None, password=None):
    """
    You can pass username and password as arguments
    :param request:
    :param username:
    :param password:
    :return:
    """

    username = request.POST.get('username', username)
    password = request.POST.get('password', password)

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            authenticate_node(get_client_ip(request), username, password)
    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'webacl/login.html', context)


def login_success(request):
    context = {}
    return render(request, 'webacl/login_success.html', context)


def login_failure(request):
    context = {}
    return render(request, 'webacl/login_failure.html', context)


def authenticate_node(form_request_ip, form_username, form_password):
    node = Node.objects.get(remote_ip=form_request_ip)

    if node:
        print("{}, {}, {}, {}".format(node.username, node.password, node.remote_ip, int(node.login_time.timestamp())))
        print("{}, {}, {}".format(form_username, form_password, form_request_ip))

        if node.username == form_username and node.password == form_password and node.remote_ip == form_request_ip:
            # TODO: Add firewall rule for node
            return HttpResponseRedirect(reverse('login_success', args=()))

    else:
        return HttpResponseRedirect(reverse('login_failure', args=()))


def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')


def generate_token(request, remote_ip):
    current_timestamp = str(datetime.datetime.utcnow().strftime("%Y-%m-%d_%H:%M"))
    salt = settings.SALT
    hash = hashlib.sha256("{}|{}|{}".format(current_timestamp, str(remote_ip), salt)
                          .encode("UTF-8")).hexdigest()

    try:
        client_token = str(request.get_full_path()).split("/")[3]
        print(client_token)
    except Exception as e:
        return HttpResponseRedirect(reverse('register', args=()))

    if str(hash) == str(client_token):
        register_client(remote_ip)


def register_client(remote_ip):

    node, created = Node.objects.get_or_create(remote_ip=remote_ip, defaults={'username': uuid.uuid4(), 'password': uuid.uuid4()})
    if not created:
        print("The IP {} already exists in the DB, skipping...".format(remote_ip))
    return node

