from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse
from authentication.models import User
from .models import People
from .serializers import PeopleSerializer

@api_view(['GET'])
def peopleList(request):
    people = People.objects.filter(public = True)
    serializer = PeopleSerializer(people, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def peopleDetail(request, pk):
    people = People.objects.get(pk=pk)
    serializer = PeopleSerializer(people, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def peopleCreate(request):
    serializer = PeopleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
def peopleUpdate(request, pk):
    people = People.objects.get(pk=pk)
    serializer = PeopleSerializer(instance=people, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def peopleDelete(request, pk):
    admin = User.objects.get(pk=pk)
    if admin.is_staff:
        people = People.objects.get(pk=pk)
        if people.delete():
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    
    return Response("You do not have permissions to perform this action")

