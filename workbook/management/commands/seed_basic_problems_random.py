from django.core.management.base import BaseCommand
from workbook.models import BasicProblem
import random
import string


class Command(BaseCommand):
    help = "Seed the BasicProblem table with 25 random problems."

    def generate_random_string(self, length=4):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def handle(self, *args, **kwargs):
        # delete existing questions
        BasicProblem.objects.all().delete()

        for _ in range(25):
            random_string = self.generate_random_string(4)
            BasicProblem.objects.create(question=random_string, answer=random_string)

        self.stdout.write(
            self.style.SUCCESS(
                "Previous questions deleted and 25 random questions have been added to BasicProblems!"
            )
        )
