from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Job, Company, Application
from .serializers import JobSerializer, CompanySerializer, ApplicationSerializer


@api_view(['GET'])               # only allow GET requests
def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    serializer = JobSerializer(jobs, many=True)    # many=True for lists
    return Response(serializer.data)


@api_view(['GET'])
def job_detail(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response(
            {'error': 'Job not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = JobSerializer(job)        # single object, no many=True
    return Response(serializer.data)


@api_view(['POST'])              # only allow POST requests
def apply_to_job(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)

    # DRF handles validation for you!
    serializer = ApplicationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(job=job)     # pass job automatically
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # If invalid, serializer.errors tells you exactly what's wrong
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def company_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)