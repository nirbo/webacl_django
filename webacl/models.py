from django.db import models


class Node(models.Model):
    username = models.CharField(max_length=255, unique=True)
    api_secret = models.CharField(max_length=255)
    remote_ip = models.GenericIPAddressField(blank=False, unique=True, null=False, protocol='both')
    login_time = models.IntegerField()

    def __str__(self):
        return "Username: {} --- API Secret: {}".format(self.username, self.api_secret)
