from django.shortcuts import render

# Create your views here.
from .models import Posts, Properties
from .serializers import PostSerializer, PropertiesSerializer
from rest_framework import generics


class Index(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class Property(generics.ListCreateAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSerializer
