from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job, Company, Application
from .serializers import JobSerializer, CompanySerializer, ApplicationSerializer

# filtering
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import JobFilter

# token authentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

# custom permissions
from .permissions import (IsAdminOrReadOnly, IsAuthenticatedOrPostOnly, IsJobOwnerOrAdmin, IsJobOwner)


@api_view(['POST'])
@permission_classes([AllowAny])     # override default - no auth needed here
def register(request):
    """POST /api/auth/register/"""
    from django.contrib.auth.models import User

    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already taken'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """POST /api/auth/login/"""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user_id': user.id})


@api_view(['POST'])
def logout(request):
    """POST /api/auth/logout/ — requires token"""
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})

class CompanyViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet gives you ALL of these for free:
    GET    /companies/       → list()
    POST   /companies/       → create()
    GET    /companies/{id}/  → retrieve()
    PUT    /companies/{id}/  → update()
    PATCH  /companies/{id}/  → partial_update()
    DELETE /companies/{id}/  → destroy()
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filterset_class = JobFilter
    permission_classes = [IsJobOwnerOrAdmin]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'company__name']
    ordering_fields = ['posted_at', 'salary_min', 'salary_max']
    ordering = ['-posted_at']    # default ordering    

    def get_serializer_class(self):
        if self.action == 'apply':
            return ApplicationSerializer
        if self.action == 'applications':
            return ApplicationSerializer
        return JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()
        job_type = self.request.query_params.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        return queryset.filter(is_active=True)
    
    def perform_create(self, serializer):
        """
        perform_create runs when a POST request is made.
        We intercept it here to automatically attach created_by.

        Without this, the user would have to send created_by in the request body.
        With this, we set it automatically from the logged-in user.
        """
        serializer.save(created_by=self.request.user)
        #                               ↑
        #                   Automatically set to whoever is logged in

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def apply(self, request, pk=None):
        job = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(job=job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[IsJobOwner])
    def applications(self, request, pk=None):
        job = self.get_object()
        apps = job.applications.all()
        serializer = self.get_serializer(apps, many=True)
        return Response(serializer.data)
    

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminUser]