# cia_tracker/models.py
from django.db import models

# import other models
from app_auth.models import (
    ScrapUser
)







class DataPull(models.Model):
    pull_time = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)


class CIAData(models.Model):
    data_pull = models.ForeignKey(DataPull, on_delete=models.CASCADE)
    provider = models.TextField()
    city = models.CharField(max_length=512)
    state = models.CharField(max_length=512)
    effective = models.CharField(max_length=20)
    press_release = models.URLField(null=True, blank=True)
    record_hash = models.CharField(max_length=64)  # SHA-256 hash of record data
    created_by = models.ForeignKey(
        ScrapUser, on_delete=models.CASCADE, 
        related_name='CIA_data_created_by', null=True, blank=True
    )
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_by = models.ForeignKey(
        ScrapUser, on_delete=models.CASCADE, 
        related_name='CIA_data_updated_by', null=True, blank=True
    )
    updated_at = models.DateTimeField('updated at', auto_now=True)


class DataChange(models.Model):
    CHANGE_TYPES = [
        ('added', 'Added'),
        ('removed', 'Removed'),
        ('modified', 'Modified'),
    ]
    data_pull = models.ForeignKey(DataPull, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES)
    provider = models.TextField()
    previous_data = models.JSONField(null=True, blank=True)
    current_data = models.JSONField(null=True, blank=True)
    change_time = models.DateTimeField(auto_now_add=True)