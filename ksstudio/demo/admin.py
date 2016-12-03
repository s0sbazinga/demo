from django.contrib import admin

# Register your models here.
from .models import Document, EdlRecord

admin.site.register(Document)
admin.site.register(EdlRecord)