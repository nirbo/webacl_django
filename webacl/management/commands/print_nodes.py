# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand

from webacl.models import Node


class Command(BaseCommand):
    def handle(self, *args, **options):

        # Prints entire node list
        nodes = Node.objects.all()

        for node in nodes:
            try:
                print(str(node))

            except Exception as e:
                print('Print Error: %s for node' % (str(e)))
                continue
