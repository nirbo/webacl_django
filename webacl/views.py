from django.shortcuts import render, redirect
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


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            authenticate_node(get_client_ip(request), request.POST['username'], request.POST['password'])
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
            return redirect('login_success')

    else:
        return redirect('login_failure')


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
        return redirect('/webacl/register/')

    if str(hash) == str(client_token):
        register_client(remote_ip)


def register_client(remote_ip):
    node = Node()

    if Node.objects.filter(remote_ip=remote_ip).exists():
        print("The IP {} already exists in the DB, skipping...".format(remote_ip))
    else:
        node.username = uuid.uuid4()
        node.password = uuid.uuid4()
        node.remote_ip = remote_ip
        node.save()

