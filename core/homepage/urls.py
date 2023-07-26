from django.urls import path
from .views import Index, Property, TodayEventView, TopEmployees, TransactionView, PointsTransferListCreateView,\
    CommentApi, Comment, TransactionReactionAPIView, AddUserReactionAPIView

urlpatterns = [
    path('homepage/transaction/', Index.as_view(), name='index'),
    path('homepage/properties/', Property.as_view(), name='property'),
    path('api/today-events/', TodayEventView.as_view(), name='today-events'),
    path('top-employees/', TopEmployees.as_view(), name='top-employee'),
    # path('api/posts/', PostListView.as_view(), name='api-post-sender-receiver'),
    path('comments/', Comment.as_view(), name='api-post-sender-receiver'),
    path('transaction/comments/', CommentApi.as_view(), name='api-post-sender-receiver'),
    path('transaction/', TransactionView.as_view(), name='sender-receiver'),
    path('points/transfer/', PointsTransferListCreateView.as_view(), name='create_points_transfer'),
    path('transaction-reactions/<uuid:transaction_id>/', TransactionReactionAPIView.as_view(), name='transaction-reactions'),
    path('transaction-reactions/<uuid:transaction_id>/<str:reaction_hash>/', TransactionReactionAPIView.as_view(), name='transaction-reactions-with-reaction-hash'),
    path('add-reaction/', AddUserReactionAPIView.as_view(), name='add-reaction'),
]
