from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    subject = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['creation_date']

