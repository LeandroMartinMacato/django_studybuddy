from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from base.models import Room

@api_view(['GET'])
def getRoutes(requests):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(requests):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms , many=True) # serialize the query set to json
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(requests ,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room , many=False)
    return Response(serializer.data)