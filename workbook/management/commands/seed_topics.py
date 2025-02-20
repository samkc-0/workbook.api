from django.core.management.base import BaseCommand
from workbook.models import BasicProblem, Topic

data = ["Basic Problem"]


class Command(BaseCommand):
    help = "Seed the BasicProblem table with 25 random problems."

    def handle(self, *args, **kwargs):
        # delete existing questions
        Topic.objects.all().delete()

        for item in data:
            Topic.objects.create(name=item)

        n_topics = len(data)
        self.stdout.write(
            self.style.SUCCESS(f"Previous topics deleted and {n_topics} topic created.")
        )
