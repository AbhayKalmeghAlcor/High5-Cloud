from django.urls import path
from .views import Index, Property, TodayEventView, TopEmployees, EmployeeRecognitionCount, PostListView

urlpatterns = [
    path('homepage/transaction/', Index.as_view(), name='index'),
    path('homepage/properties/', Property.as_view(), name='property'),
    path('api/today-events/', TodayEventView.as_view(), name='today-events'),
    path('top-employees/', TopEmployees.as_view()),
    path('employee/<str:employee_id>/recognitions/count/', EmployeeRecognitionCount.as_view()),
    path('api/posts/', PostListView.as_view(), name='api-post-sender-receiver'),
]
