from django.db import models

# Translation Model
class Translation(models.Model):
    source_text = models.TextField(max_length=300, null=True, blank=False)
    target_text = models.TextField(max_length=1000, null=True, blank=False)
    source_lang = models.CharField(max_length=10, null=True, blank=False)
    target_lang = models.CharField(max_length=10, null=True, blank=False)
    date_time = models.DateTimeField(auto_now=True, null=True)
    
