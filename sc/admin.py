from django.contrib import admin

# Register your models here.
from django import forms
from . import models

class ScAdminForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = "__all__"
        
class ScAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'start',
        'end',
        'event_name',
    )
    
admin.site.register(models.Event, ScAdmin)