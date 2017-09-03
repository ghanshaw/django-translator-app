from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Translation(models.Model):
    # user = models.ForeignKey(User, null=True, blank=True)
    source_text = models.TextField(max_length=1000, null=True, blank=False)
    target_text = models.TextField(max_length=1000, null=True, blank=False)
    source_lang = models.CharField(max_length=100, null=True, blank=False)
    target_lang = models.CharField(max_length=100, null=True, blank=False)
    date_time = models.DateTimeField(auto_now=True, null=True)
    # user_id = models.IntegerField()
    
