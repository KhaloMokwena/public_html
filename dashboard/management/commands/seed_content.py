from django.core.management.base import BaseCommand
from django.db import transaction

from dashboard import seed_data
from dashboard.models import Service, JobPosting, Division, Faq


class Command(BaseCommand):
    help = (
        "Load the starting Services, Job postings, About divisions and FAQs from the ZuriKO content document. "
        "Safe to run more than once: items whose title/question already exists are left alone."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--replace', action='store_true',
            help="Delete ALL existing services, job postings, divisions and FAQs first, then load the starting content.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        verbose = options['verbosity'] > 0   # tests call this with verbosity=0
        if options['replace']:
            for model in (Service, JobPosting, Division, Faq):
                deleted, _ = model.objects.all().delete()
                if verbose:
                    self.stdout.write(f"Removed {deleted} existing {model.__name__} row(s)")

        created = {'Service': 0, 'JobPosting': 0, 'Division': 0, 'Faq': 0}

        for index, (category, title, description) in enumerate(seed_data.SERVICES, start=1):
            _, was_created = Service.objects.get_or_create(
                title=title, category=category,
                defaults={'description': description, 'order': index},
            )
            created['Service'] += was_created

        # Careers lists newest first, so load in reverse to keep the document's order on the page.
        for job in reversed(seed_data.JOBS):
            _, was_created = JobPosting.objects.get_or_create(
                title=job['title'],
                defaults={k: v for k, v in job.items() if k != 'title'},
            )
            created['JobPosting'] += was_created

        for index, division in enumerate(seed_data.DIVISIONS, start=1):
            _, was_created = Division.objects.get_or_create(
                title=division['title'],
                defaults={**{k: v for k, v in division.items() if k != 'title'}, 'order': index},
            )
            created['Division'] += was_created

        for index, (question, answer) in enumerate(seed_data.FAQS, start=1):
            _, was_created = Faq.objects.get_or_create(
                question=question, defaults={'answer': answer, 'order': index},
            )
            created['Faq'] += was_created

        if verbose:
            for name, count in created.items():
                self.stdout.write(self.style.SUCCESS(f"{name}: {count} added"))
