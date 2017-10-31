import logging
import uuid

import unicodedata
from django.db import models
from django.utils.encoding import force_text
from django_unixdatetimefield import UnixDateTimeField
from django.utils import six, timezone
from django.utils.translation import ugettext as _

from webacl_django.behaviors.base_behaviors import Timestamp

logger = logging.getLogger(__name__)


class Node(Timestamp):
    """
    Node Model with username and password stored as UUID
    """
    username = models.UUIDField(max_length=255,
                                unique=True,
                                default=uuid.uuid4,
                                help_text=_('Required. 255 characters or fewer. UUID compatbile'),
                                error_messages={
                                    'unique': _("A node with that username already exists."),
                                }, )
    password = models.UUIDField(max_length=255, default=uuid.uuid4)
    remote_ip = models.GenericIPAddressField(blank=False, unique=True, null=False, protocol='both')
    login_time = UnixDateTimeField(auto_now_add=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this node should be treated as active. '
            'Unselect this instead of deleting nodes.'
        ),
    )

    def __str__(self):
        return "Username: %s - Password: %s - IP: %s - LoginTime: %s" % (self.username, self.password, self.remote_ip, self.login_time)

    def clean(self):
        setattr(self, self.username, self.normalize_username(self.username))

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', force_text(username))

    class Meta:
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')
