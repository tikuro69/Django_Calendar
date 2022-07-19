from django.db import models
from django.urls import reverse
# Create your models here.


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    event_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.event_name
    
    def get_absolute_url(self):
        return reverse("Event_detail", args=(self.pk,))