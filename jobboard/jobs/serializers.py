from rest_framework import serializers
from .models import Company, Job, Application


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'    # include every field


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source='company.name',    # pull from related model
        read_only=True
    )
    company_location = serializers.CharField(
        source='company.location',
        read_only=True
    )
    job_type_display = serializers.CharField(
        source='get_job_type_display',   # get the human readable choice
        read_only=True
    )
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'job_type',
            'job_type_display', 'salary_min', 'salary_max',
            'is_active', 'posted_at', 'company', 'company_name',
            'company_location', 'application_count', 'created_by'
        ]
        read_only_fields = ['created_by', 'posted_at']


    def get_application_count(self, obj):
        # Custom field - call a method to compute it
        return obj.applications.count()


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['status', 'applied_at']  # user can't set these