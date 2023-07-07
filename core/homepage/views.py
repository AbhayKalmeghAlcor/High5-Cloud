from .models import Posts, Properties, Recognition
from .serializers import PostSerializer, PropertiesSerializer, PropertiesSubSerializer, RecognitionSerializer
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import ListAPIView
from datetime import date
from django.db.models import Q
from accounts.models import Account
from accounts.serializers import AccountSubSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination


# from .models import PointsTransfer
# from .serializers import PointsTransferSerializer


class Index(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class Property(generics.ListCreateAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSerializer


class PropertySub(generics.ListCreateAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSubSerializer


# class PhotoList(APIView):
#     def post(self, request, format=None):
#         serializer = PropertiesSubSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodayEventView(APIView):
    def get(self, request):
        today = date.today()
        # users = Account.objects.filter(birth_date__day=today.day, birth_date__month=today.month)
        users = Account.objects.filter(Q(birth_date__month=today.month, birth_date__day=today.day) |
                                       Q(hire_date__month=today.month, hire_date__day=today.day))
        serializer = AccountSubSerializer(users, many=True)
        return Response(serializer.data)


class EmployeeRecognitionCount(APIView):
    def get(self, request, employee_id):
        employee = Account.objects.get(pk=employee_id)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recognitions = Recognition.objects.filter(
            employee=employee,
            date__gte=thirty_days_ago
        )
        count = recognitions.count()
        return Response({'count': count})


class TopEmployees(APIView):
    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        employee_recognition_counts = Recognition.objects.filter(
            date__gte=thirty_days_ago
        ).values('employee').annotate(count=models.Count('employee')).order_by('-count')[:5]

        top_employees = []
        for count_data in employee_recognition_counts:
            employee_id = count_data['employee']
            recognition_count = count_data['count']
            employee = Account.objects.get(pk=employee_id)
            top_employees.append({'employee': employee.name, 'count': recognition_count})

        return Response(top_employees)


class PointsTransferListCreateView(generics.ListCreateAPIView):
    # queryset = PointsTransfer.objects.all()
    # serializer_class = PointsTransferSerializer

    def perform_create(self, serializer):
        # Get the sender and receivers from the request data
        sender = self.request.user
        receivers_data = self.request.data.get('receivers', [])

        # Calculate total points to be transferred
        total_points = int(self.request.data.get('points_available', 0))

        # Calculate points to be transferred to each receiver
        num_receivers = len(receivers_data)
        points_per_receiver = total_points // num_receivers
        remaining_points = total_points % num_receivers

        # Create the PointsTransfer instance for the sender
        transfer = serializer.save(sender=sender, points_available=total_points)

        # Transfer points to each receiver
        for receiver_data in receivers_data:
            receiver_id = receiver_data.get('id')
            receiver = Account.objects.get(id=receiver_id)
            points_to_receive = points_per_receiver
            if remaining_points > 0:
                points_to_receive += 1
                remaining_points -= 1

            # Update points_received for the receiver
            receiver.points_received += points_to_receive
            receiver.save()

            # Add the receiver to the ManyToMany field
            transfer.receivers.add(receiver)

            # Save the updated transfer instance
            transfer.save()


class SenderReceiverFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        sender = request.query_params.get('sender')
        recipients = request.query_params.get('recipients')

        if sender:
            queryset = queryset.filter(sender=sender)
        if recipients:
            queryset = queryset.filter(recipients=recipients)

        return queryset


class PostListView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SenderReceiverFilterBackend]
    # queryset = Posts.objects.all()
    # serializer_class = PostSerializer
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 10
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['sender__id']
