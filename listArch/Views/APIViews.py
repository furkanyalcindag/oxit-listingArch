from rest_framework.response import Response
from rest_framework.views import APIView

from listArch.models import Product
from listArch.models.Company import Company
from listArch.models.APIObject import APIObject
from listArch.serializers.CompanySerializer import CompanyResponseSerializer


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
