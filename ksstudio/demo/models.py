from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import hashlib

# Create your models here.
def write_as(instance, filename):
	return (instance.upfile_hash + '_' + filename.split('.')[0]
           + '.' + instance.upfile_type)

class Document(models.Model):
    upfile_hash = models.CharField(primary_key=True,
                                   max_length=256,
                                   default=hashlib.md5('').hexdigest())
    upfile_name = models.CharField(max_length=256, default='')
    upfile_type = models.CharField(max_length=10, default='')
    process_time = models.FloatField(default=0.0)
    upload_time = models.DateTimeField(default=timezone.now)
    # up_file = models.FileField(upload_to=write_as)

class EdlRecord(models.Model):
    original_file = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
    )
    result_file = models.CharField(primary_key=True,
                                   max_length=128)