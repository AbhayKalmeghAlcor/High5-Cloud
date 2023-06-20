from django.shortcuts import render

# Create your views here.
from .models import Posts
from .serializers import PostSerializer
from rest_framework import generics


class Index(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
