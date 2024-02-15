from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from message.models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User

@api_view(['GET'])
def getMessages(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def writeMessage(request):
    serializer=MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(f"ERROR: {serializer.errors} ", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def specificMessage(request, id):
    message = get_object_or_404(Message, pk=id)
    data = MessageSerializer(message).data
    stat = status.HTTP_200_OK
    if request.method == 'GET':
        message.is_read = True
        message.save()
    elif request.method == 'DELETE':
        stat = status.HTTP_204_NO_CONTENT
        message.delete()
    return Response(data, status=stat)

@api_view(['GET'])
def unreadMessages(request):
    messages = Message.objects.filter(is_read=False)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
        