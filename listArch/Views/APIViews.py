from rest_framework.response import Response
from rest_framework.views import APIView

from listArch.models import Product, Subscriber, Profile
from listArch.models.Company import Company
from listArch.models.APIObject import APIObject
from listArch.serializers.CompanySerializer import CompanyResponseSerializer
from listArch.serializers.ProfileSerializer import ProfileResponseSerializer
from listArch.serializers.SubscriberSerializer import SubscriberResponseSerializer


class GetCompany(APIView):

    def post(self, request, format=None):
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        company_total = Company.objects.count()
        companies = Company.objects.filter(
            name__icontains=request.data['search[value]']).order_by('id')[
                    int(start):end]
        filteredTotal = Company.objects.filter(
            name__icontains=request.data['search[value]']).count()

        apiObject = APIObject()
        apiObject.data = companies
        apiObject.draw = int(request.POST['draw'])
        apiObject.recordsTotal = int(company_total)
        apiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = CompanyResponseSerializer(apiObject, context=serializer_context)
        return Response(serializer.data)

class GetSubscriber(APIView):

    def post(self, request, format=None):
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        subscriber_total = Subscriber.objects.count()
        subscribers = Subscriber.objects.filter(
            email__icontains=request.data['search[value]']).order_by('id')[
                    int(start):end]
        filteredTotal = Subscriber.objects.filter(
            email__icontains=request.data['search[value]']).count()

        apiObject = APIObject()
        apiObject.data = subscribers
        apiObject.draw = int(request.POST['draw'])
        apiObject.recordsTotal = int(subscriber_total)
        apiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = SubscriberResponseSerializer(apiObject, context=serializer_context)
        return Response(serializer.data)




class GetCategoryProduct(APIView):

    def post(self, request, format=None):
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        product_count = Product.objects.count()
        products = Product.objects.filter(
            name__icontains=request.data['search[value]']).order_by('id')[
                    int(start):end]
        filteredTotal = Company.objects.filter(
            name__icontains=request.data['search[value]']).count()

        apiObject = APIObject()
        apiObject.data = products
        apiObject.draw = int(request.POST['draw'])
        apiObject.recordsTotal = int(product_count)
        apiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = CompanyResponseSerializer(apiObject, context=serializer_context)
        return Response(serializer.data)


class GetProfile(APIView):

    def post(self, request, format=None):
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        profile_total = Profile.objects.count()
        profile = Profile.objects.filter(
            user__first_name__icontains=request.data['search[value]']).order_by('id')[
                    int(start):end]
        filteredTotal = Profile.objects.filter(
            user__first_name__icontains=request.data['search[value]']).count()

        apiObject = APIObject()
        apiObject.data = profile
        apiObject.draw = int(request.POST['draw'])
        apiObject.recordsTotal = int(profile_total)
        apiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = ProfileResponseSerializer(apiObject, context=serializer_context)
        return Response(serializer.data)