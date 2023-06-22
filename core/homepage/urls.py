from django.urls import path
from .views import Index, Property

urlpatterns = [
    path('homepage/transaction/', Index.as_view(), name='index'),
    path('homepage/properties/', Property.as_view(), name='property'),

]
