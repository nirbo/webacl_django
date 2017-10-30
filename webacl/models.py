from django.db import models
from django_unixdatetimefield import UnixDateTimeField


class Node(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    remote_ip = models.GenericIPAddressField(blank=False, unique=True, null=False, protocol='both')
    login_time = UnixDateTimeField(auto_now_add=True)

    def __str__(self):
        return "Username: {} --- Password: {}".format(self.username, self.password)
