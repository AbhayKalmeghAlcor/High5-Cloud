from .models import Posts, Properties, Comments
from .serializers import PostSerializer, PropertiesSerializer, PropertiesSubSerializer, RecognitionSerializer, \
    CommentsSerializer
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
from rest_framework.pagination import PageNumberPagination, CursorPagination
from django.db.models import Sum
from django.db.models import Count
from .paginations import CustomPagination, PaginationHandlerMixin

from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


# from .models import PointsTransfer
# from .serializers import PointsTransferSerializer


class Index(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class Comment(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class Property(generics.ListCreateAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSerializer


class PropertySub(generics.ListCreateAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSubSerializer


class TodayEventView(APIView):
    def get(self, request):
        today = date.today()
        # users = Account.objects.filter(birth_date__day=today.day, birth_date__month=today.month)
        users = Account.objects.filter(Q(birth_date__month=today.month, birth_date__day=today.day) |
                                       Q(hire_date__month=today.month, hire_date__day=today.day))
        serializer = AccountSubSerializer(users, many=True)
        return Response(serializer.data)


class TopEmployees(APIView):
    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)

        # Count the number of times each recipient received points
        recipient_counts = Posts.objects.filter(
            created__gte=thirty_days_ago
        ).values('recipients').annotate(
            count=Count('recipients')
        ).order_by('-count')[:5]

        top_employees = []
        for count_data in recipient_counts:
            recipient_id = count_data['recipients']
            count = count_data['count']
            recipient = Account.objects.get(pk=recipient_id)
            top_employees.append({'recipient': recipient.full_name,
                                  'count': count,
                                  'avtar': recipient.avtar.url,
                                  'id': recipient.id}
                                 )

        return Response(top_employees)


class SenderReceiverFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        sender = request.query_params.get('sender')
        recipients = request.query_params.get('recipients')
        date_range = request.query_params.get('date_range')

        if sender:
            queryset = queryset.filter(sender=sender)

        if recipients:
            queryset = queryset.filter(recipients=recipients)

        if date_range == 'thisMonth':
            thirty_days_ago = date.today() - timedelta(days=30)
            queryset = queryset.filter(created__gte=thirty_days_ago)

        if date_range == 'lastMonth':
            today = date.today()
            last_month_end = date(today.year, today.month, 1) - timedelta(days=1)
            last_month_start = date(last_month_end.year, last_month_end.month, 1)
            queryset = queryset.filter(created__range=(last_month_start, last_month_end))
            # thirty_days_ago = date.today() - timedelta(days=30)
            # one_year_ago = thirty_days_ago - timedelta(days=365)
            # queryset = queryset.filter(created__gte=one_year_ago)

        if date_range == 'lastQuarter':
            one_year_ago = date.today() - timedelta(days=90)
            queryset = queryset.filter(created__gte=one_year_ago)

        if date_range == 'last6Months':
            one_year_ago = date.today() - timedelta(days=183)
            queryset = queryset.filter(created__gte=one_year_ago)

        if date_range == 'last1Year':
            one_year_ago = date.today() - timedelta(days=365)
            queryset = queryset.filter(created__gte=one_year_ago)

        return queryset


class PostListView(generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SenderReceiverFilterBackend]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['sender__id']
    # queryset = Posts.objects.all()
    # serializer_class = PostSerializer
    # pagination_class = CursorPagination


# thisMonth
# lastMonth
# lastQuarter
# last6Months
# last1Year

# class Transaction(APIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostSerializer


# def _filter_orders(
#
#         business_id,
#
#         filter_type=None,
#
#         options=None,
#
#         custom_date1=None,
#
#         custom_date2=None,
#
# ):
#      TODO: Optimization: We can merge this conditions
#
#     if options == "this_month":
#
#         this_month, this_year = get_current_month_year("this_month")
#
#         return get_filter_type(filter_type, business_id, this_month, this_year)
#
#
#
#
#     elif options == "last_month":
#
#         p_month, p_year = get_current_month_year("last_month")
#
#         return get_filter_type(filter_type, business_id, p_month, p_year)
#
#
#
#
#     elif options == "this_quarter":
#
#         first_date, last_date = get_quaterly_dates("this_quarter")
#
#         return get_filter(filter_type, business_id, first_date, last_date)
#
#
#
#
#     elif options == "last_quarter":
#
#         first_date, last_date = get_quaterly_dates("last_quarter")
#
#         return get_filter(filter_type, business_id, first_date, last_date)
#
#
#
#
#     elif options == "year_to_date":
#
#         current_date = datetime.now()
#
#         current_year = current_date.year
#
#         first_date = f"{current_year}-01-01"
#
#         return get_filter(filter_type, business_id, first_date, current_date)
#
#
#
#
#     elif options == "custom_range":
#
#         return get_filter(filter_type, business_id, custom_date1, custom_date2)
#
#
#
#
#     elif options == "last_7_days":
#
#         date2 = datetime.now()
#
#         date1 = date2 - timedelta(days=7)
#
#         return get_filter(filter_type, business_id, date1, date2)
#
#
class Transaction(APIView, PaginationHandlerMixin):
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):

        sender = self.request.GET.get('sender', None)
        recipients = self.request.GET.get('recipients', None)
        date_range = self.request.GET.get('date_range', None)
        pagination = self.request.GET.get('pagination', None)
        qs = []
        if sender:
            qs = Posts.objects.filter(sender=sender)

        if recipients:
            qs = Posts.objects.filter(recipients=recipients)

        if date_range == 'thisMonth':
            thirty_days_ago = date.today() - timedelta(days=30)
            qs = Posts.objects.filter(created__gte=thirty_days_ago)

        if date_range == 'lastMonth':
            today = date.today()
            last_month_end = date(today.year, today.month, 1) - timedelta(days=1)
            last_month_start = date(last_month_end.year, last_month_end.month, 1)
            qs = Posts.objects.filter(created__range=(last_month_start, last_month_end))

        if date_range == 'lastQuarter':
            one_year_ago = date.today() - timedelta(days=90)
            qs = Posts.objects.filter(created__gte=one_year_ago)

        if date_range == 'last6Months':
            one_year_ago = date.today() - timedelta(days=183)
            qs = Posts.objects.filter(created__gte=one_year_ago)

        if date_range == 'last1Year':
            one_year_ago = date.today() - timedelta(days=365)
            qs = Posts.objects.filter(created__gte=one_year_ago)

        if pagination:
            page = self.paginate_queryset(qs)
            serializer = PostSerializer(page, many=True)
            return Response({"response": self.get_paginated_response(serializer.data).data})

        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PointsTransferListCreateView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        sender = self.request.user
        receivers_data = self.request.data.get('receivers', [])

        total_points = int(self.request.data.get('points_available', 0))

        num_receivers = len(receivers_data)
        points_per_receiver = total_points // num_receivers
        remaining_points = total_points % num_receivers

        transfer = serializer.save(sender=sender, points_available=total_points)

        for receiver_data in receivers_data:
            receiver_id = receiver_data.get('id')
            receiver = Account.objects.get(id=receiver_id)

            points_to_receive = points_per_receiver
            if remaining_points > 0:
                points_to_receive += 1
                remaining_points -= 1

            receiver.points_received += points_to_receive
            receiver.save()

            transfer.receivers.add(receiver)

        sender.points_available -= total_points
        sender.save()
