from django.urls import path
from .views import Index

urlpatterns = [
    path('index/homepage/', Index.as_view(), name='index'),

]
