from django.core.management.base import BaseCommand
from django.db import connection
from workbook.models import BasicProblem

data = [
    "a1m2",
    "522d",
    "v8vz",
    "8uep",
    "oxl4",
    "x366",
    "jbr2",
    "bfg3",
    "ketr",
    "vyos",
    "25mz",
    "07b7",
    "4xze",
    "4b1q",
    "q3dq",
    "ahiu",
    "qyyo",
    "3xnx",
    "5gjw",
    "dhe9",
    "euub",
    "8xrm",
    "wpj5",
    "gcz2",
    "9vuq",
]


class Command(BaseCommand):
    help = "Seed the BasicProblem table with 25 random problems."

    def handle(self, *args, **kwargs):

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='workbook_basicproblem';"
            )

        self.stdout.write("Seeding new problems...")

        for item in data:
            BasicProblem.objects.create(question=item, answer=item)

        self.stdout.write(
            self.style.SUCCESS(
                "Previous questions deleted and 25 questions have been added to BasicProblems!"
            )
        )
