import logging
import uuid

import unicodedata
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.utils.encoding import force_text
from django_unixdatetimefield import UnixDateTimeField
from django.utils import six, timezone
from django.utils.translation import ugettext as _

from webacl_django.behaviors.base_behaviors import Timestamp

logger = logging.getLogger(__name__)


class Node(Timestamp):
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.SlugField(max_length=255,
                                unique=True,
                                default=uuid.uuid4,
                                help_text=_('Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator],
                                error_messages={
                                    'unique': _("A node with that username already exists."),
                                }, )
    password = models.CharField(max_length=255, default=uuid.uuid4)
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
        return "Username: {} --- Password: {}".format(self.username, self.password)

    def clean(self):
        setattr(self, self.username, self.normalize_username(self.username))

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', force_text(username))

    class Meta:
        verbose_name = _('Node')
        verbose_name_plural = _('Nodes')
