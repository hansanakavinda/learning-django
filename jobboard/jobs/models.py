from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)          # blank=True = optional
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)  # auto set on creation

    def __str__(self):
        return self.name    # what shows in admin panel


class Job(models.Model):

    # Choices = dropdown options
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
    ]

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='jobs',
        null=True,              # null=True because existing jobs have no creator
        blank=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,    # if company deleted, delete its jobs too
        related_name='jobs'          # lets you do company.jobs.all() later
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    salary_min = models.IntegerField(null=True, blank=True)   # optional field
    salary_max = models.IntegerField(null=True, blank=True)
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='full_time'
    )
    is_active = models.BooleanField(default=True)     # True/False field
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class Application(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} → {self.job.title}"