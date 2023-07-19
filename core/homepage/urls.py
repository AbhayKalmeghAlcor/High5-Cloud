from django.urls import path
from .views import Index, Property, TodayEventView, TopEmployees, Transaction, PointsTransferListCreateView,\
    CommentApi, Comment

urlpatterns = [
    path('homepage/transaction/', Index.as_view(), name='index'),
    path('homepage/properties/', Property.as_view(), name='property'),
    path('api/today-events/', TodayEventView.as_view(), name='today-events'),
    path('top-employees/', TopEmployees.as_view(), name='top-employee'),
    # path('employee/<str:employee_id>/recognitions/count/', EmployeeRecognitionCount.as_view()),
    # path('api/posts/', PostListView.as_view(), name='api-post-sender-receiver'),
    path('comments/', Comment.as_view(), name='api-post-sender-receiver'),
    path('transaction/comments/', CommentApi.as_view(), name='api-post-sender-receiver'),
    path('transaction/', Transaction.as_view(), name='sender-receiver'),
    path('points/transfer/', PointsTransferListCreateView.as_view(), name='create_points_transfer'),
]
