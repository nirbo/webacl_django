from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from webacl_django.utils.get_current_user import get_current_user


class Timestamp(models.Model):
    '''
    Basic Timestamp Abstract Model/Behaviour
    Uses get_current_user middleware to get logged in user from local thread
    '''
    # Timestamp
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Created By'), default=get_current_user, blank=True, null=True, editable=False, related_name="%(class)s_related_create_userprofile")
    created_at = models.DateTimeField(_('Created Date'), auto_now_add=True, editable=False, db_index=True)
    modified_at = models.DateTimeField(_('Last Edit Date'), auto_now=True, editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Last Modify By'), blank=True, null=True, default=get_current_user, editable=False, related_name="%(class)s_related_modify_userprofile")

    class Meta:
        abstract = True