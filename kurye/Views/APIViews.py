from django import apps
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from kurye.models import Neighborhood
from kurye.models.Log import Log
from kurye.models.Company import Company
from kurye.models.LogAPIObject import LogAPIObject
from kurye.models.Notification import Notification
from kurye.models.Profile import Profile
from kurye.models.Request import Request
from kurye.models.Task import Task
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.serializers.CompanySerializer import CompanyResponseSerializer
from kurye.serializers.GenericSerializer import DataTableSerializer
from kurye.serializers.LogSerializer import LogSerializer, LogResponseSerializer
from kurye.serializers.NeighborhoodSerializer import NeighborhoodSerializer, NeighborhoodResponseSerializer
from kurye.serializers.NotificationSerializer import NotificationResponseSerializer
from kurye.serializers.TaskSerializer import TaskResponseSerializer

'''  order: asc
    start: 20
    length: 10 '''


class GetLogs(APIView):

    def post(self, request, format=None):
        array_category = []
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        logs = Log.objects.filter(content__contains=request.data['search[value]']).order_by('id')[
               int(request.data['start']):end]
        filteredTotal = Log.objects.filter(content__contains=request.data['search[value]']).count()
        logApiObject = LogAPIObject()
        logApiObject.data = logs
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(Log.objects.count())
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = LogResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetCompany(APIView):

    def post(self, request, format=None):
        array_category = []
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        user = request.user
        profile = Profile.objects.get(user=user)
        companiess = Company.objects.all().filter(~Q(profile_id=profile.pk)).count()

        companies = Company.objects.filter(~Q(profile_id=profile.pk)).filter(
            companyName__icontains=request.data['search[value]']).order_by('id')[
                    int(start):end]

        filteredTotal = Company.objects.filter(~Q(profile_id=profile.pk)).filter(
            companyName__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = companies
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(companiess)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = CompanyResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetNotification(APIView):

    def post(self, request, format=None):
        array_category = []
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        notification_total = Notification.objects.all().count()

        notifications = Notification.objects.filter(
            message__icontains=request.data['search[value]']).order_by('isRead')[
                        int(start):end]

        filteredTotal = Notification.objects.filter(
            message__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = notifications
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(notification_total)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = NotificationResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetRequestReport(APIView):

    def post(self, request, format=None):
        array_category = []
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        user = request.user
        profile = Profile.objects.get(user=user)
        company = Company.objects.get(profile=profile)

        tasks = TaskSituationTask.objects.filter(task__request__company=request.data['search[value]']).order_by(
            'id')[
                int(start):end]

        task_all = TaskSituationTask.objects.filter(task__request__company_id=company.pk)

        filteredTotal = TaskSituationTask.objects.filter(task__request__company=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = tasks
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(task_all)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = TaskResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetNeighborhood(APIView):

    def post(self, request, format=None):
        array_category = []
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        neighborhoods = Neighborhood.objects.filter(
            neighborhood_name__icontains=request.data['search[value]']).order_by('neighborhood_name')[
                        int(request.data['start']):end]
        filteredTotal = Neighborhood.objects.filter(neighborhood_name__icontains=request.data['search[value]']).count()
        logApiObject = LogAPIObject()
        logApiObject.data = neighborhoods
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(Neighborhood.objects.count())
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
            'model': Neighborhood,
            'fields': ['id', 'city', 'district', 'neighborhood_name', 'price']
        }
        serializer = NeighborhoodResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)


class GetDataGeneric(APIView):

    def post(self, request, format=None):
        log = apps.apps.get_model('kurye', 'Log')

        array_category = []
        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        logs = log.objects.filter(content__contains=request.data['search[value]']).order_by('id')[
               int(request.data['start']):end]
        filteredTotal = Log.objects.filter(content__contains=request.data['search[value]']).count()
        logApiObject = LogAPIObject()
        logApiObject.data = logs
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(log.objects.count())
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
            'model': Log,
            'fields': ['content', 'creationDate']
        }
        datatableSerializer = DataTableSerializer(logApiObject, context=serializer_context)
        # datatableSerializer.data1.Meta.model = log
        # datatableSerializer.data1.Meta.fields = ['content', 'creationDate']
        # serializer = DataTableSerializer(logApiObject, context=serializer_context).data.Meta.model = log
        serializer = datatableSerializer
        return Response(serializer.data)
