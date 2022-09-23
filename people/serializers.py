from rest_framework import serializers
from .models import People

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['user', 'food', 'location', 'hobby', 'title', 'image', 'public']
