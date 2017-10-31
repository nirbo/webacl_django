import logging

import unicodedata
from django.http import JsonResponse

from webacl.models import Node
import hashlib
import datetime
import uuid
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_token(token, remote_ip):
    """
    :param token: client token
    :param remote_ip: client IP
    :return: Node object
    """
    token = unicodedata.normalize('NFKD', token).encode('ascii', 'ignore')
    current_timestamp = str(datetime.datetime.utcnow().strftime("%Y-%m-%d_%H:%M"))
    salt = settings.SALT
    hash = hashlib.sha256("{}|{}|{}".format(current_timestamp, str(remote_ip), salt)
                          .encode("UTF-8")).hexdigest()

    if str(hash) == str(token):
        return get_or_create_node_for_ip(remote_ip)
    else:
        logger.warning('Tokens do not match for IP: %s' % remote_ip)
        return None


def get_or_create_node_for_ip(remote_ip):
    """
    Get or Create a Node for IP
    :param remote_ip:
    :return:
    """
    node, created = Node.objects.get_or_create(remote_ip=remote_ip,
                                               defaults={'username': uuid.uuid4(), 'password': uuid.uuid4()})
    if not created:
        print("The IP {} already exists in the DB, skipping...".format(remote_ip))
    return node


def authenticate_node(form_request_ip):
    """
    Runs bash script to grant access in the firewall
    :param form_request_ip:
    :param form_username:
    :param form_password:
    :return:
    """
    try:
        node = Node.objects.get(remote_ip=form_request_ip)
    except Node.DoesNotExist:
        logger.critical('Node with IP: %s doesnt exist' % str(form_request_ip))

    # TODO Run the script


def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')