from rest_framework import serializers
from message.models import Message
from django.utils import timezone
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    receiver = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    class Meta:
        model = Message
        exclude = ['is_read']
    
    def create(self, validated_data):
        validated_data['creation_date'] = timezone.now()
        return super().create(validated_data)


