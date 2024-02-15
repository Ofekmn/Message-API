from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from message.models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMessages(request):
    messages = Message.objects.filter(receiver=request.user)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def writeMessage(request):
    request.data['sender'] = request.user.username
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(f"ERROR: {serializer.errors} ", status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
@api_view(['GET', 'DELETE'])
def specificMessage(request, id):
    message = get_object_or_404(Message, pk=id)

    if message.sender != request.user and message.receiver != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    data = MessageSerializer(message).data
    stat = status.HTTP_200_OK

    if request.method == 'GET':
        if (message.receiver != request.user):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        message.is_read = True
        message.save()
    elif request.method == 'DELETE':
        stat = status.HTTP_204_NO_CONTENT
        message.delete()
    return Response(data, status=stat)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def unreadMessages(request):
    messages = Message.objects.filter(receiver=request.user, is_read=False)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
        