from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os



class Command(BaseCommand):

    def handle(self, *args, **options):
        username = os.environ['db_user']
        password = os.environ['db_pwd']
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username, "admin@translator-app.com", password)