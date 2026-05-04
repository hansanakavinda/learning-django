# jobs/management/commands/seed.py

from django.core.management.base import BaseCommand
from faker import Faker
import random
from jobs.models import Company, Job, Application

fake = Faker()

class Command(BaseCommand):

    help = 'Seed the database with fake data for testing'

    def add_arguments(self, parser):
        # this lets you pass a number when running the command
        # example: python manage.py seed --companies 10
        parser.add_argument(
            '--companies',
            type=int,
            default=5,
            help='Number of companies to create'
        )
        parser.add_argument(
            '--jobs',
            type=int,
            default=20,
            help='Number of jobs to create'
        )
        parser.add_argument(
            '--applications',
            type=int,
            default=50,
            help='Number of applications to create'
        )

    def handle(self, *args, **kwargs):
        companies_count = kwargs['companies']
        jobs_count = kwargs['jobs']
        applications_count = kwargs['applications']

        self.create_companies(companies_count)
        self.create_jobs(jobs_count)
        self.create_applications(applications_count)

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created:'
            f'\n  {companies_count} companies'
            f'\n  {jobs_count} jobs'
            f'\n  {applications_count} applications'
        ))

    def create_companies(self, count):
        self.stdout.write('Creating companies...')
        for _ in range(count):
            Company.objects.create(
                name=fake.company(),
                website=fake.url(),
                location=fake.city(),
            )

    def create_jobs(self, count):
        self.stdout.write('Creating jobs...')

        companies = list(Company.objects.all())

        if not companies:
            self.stdout.write(self.style.ERROR('No companies found. Create companies first.'))
            return

        job_titles = [
            'Backend Developer', 'Frontend Developer', 'Full Stack Developer',
            'Data Scientist', 'ML Engineer', 'DevOps Engineer',
            'Product Manager', 'UX Designer', 'QA Engineer',
            'Mobile Developer', 'Cloud Architect', 'Security Engineer',
        ]

        job_types = ['full_time', 'part_time', 'contract', 'remote']

        for _ in range(count):
            Job.objects.create(
                company=random.choice(companies),
                title=random.choice(job_titles),
                description=fake.paragraph(nb_sentences=5),
                salary_min=random.randint(30000, 80000),
                salary_max=random.randint(80000, 150000),
                job_type=random.choice(job_types),
                is_active=random.choice([True, True, True, False]),
                # True appears 3 times so most jobs will be active
            )

    def create_applications(self, count):
        self.stdout.write('Creating applications...')

        jobs = list(Job.objects.all())

        if not jobs:
            self.stdout.write(self.style.ERROR('No jobs found. Create jobs first.'))
            return

        statuses = ['pending', 'reviewed', 'rejected', 'accepted']

        for _ in range(count):
            Application.objects.create(
                job=random.choice(jobs),
                applicant_name=fake.name(),
                applicant_email=fake.email(),
                cover_letter=fake.paragraph(nb_sentences=3),
                status=random.choice(statuses),
            )