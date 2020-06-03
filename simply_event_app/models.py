from datetime import timedelta
from typing import Dict

from django.conf import settings
from django.db import models
from django.urls import reverse, reverse_lazy


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/events/', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('simply_event_app:event_detail', kwargs={'id': self.id})


class Guest(models.Model):
    name = models.CharField(max_length=200)
    delay = models.SmallIntegerField(verbose_name='Delay in minutes', null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def add_delay_to_date(self):
        if self.delay:
            return self.event.start_date + timedelta(minutes=self.delay)
        else:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'delay': self.delay,
        }