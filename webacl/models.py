import logging

from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django_unixdatetimefield import UnixDateTimeField
from django.utils import six, timezone
from django.utils.translation import ugettext as _

from webacl_django.behaviors.base_behaviors import Timestamp

logger = logging.getLogger(__name__)


class Node(Timestamp):

    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.SlugField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    remote_ip = models.GenericIPAddressField(blank=False, unique=True, null=False, protocol='both')
    login_time = UnixDateTimeField(auto_now_add=True)

    def __str__(self):
        return "Username: {} --- Password: {}".format(self.username, self.password)

    def clean(self):
        setattr(self, self.username, self.normalize_username(self.get_username()))

    class Meta:
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')