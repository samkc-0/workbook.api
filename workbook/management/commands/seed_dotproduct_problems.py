from copy import deepcopy
from django.core.management.base import BaseCommand
from django.db import connection
from workbook.models import DotProductProblem


data = [
    {
        "id": 0,
        "question": {
            "left": {
                "data": [[3]],
                "rows": 1,
                "columns": 1,
                "name": "b",
            },
            "top": {
                "data": [[5]],
                "rows": 1,
                "columns": 1,
                "name": "a",
            },
            "product": {
                "data": [[""]],
                "rows": 1,
                "columns": 1,
                "name": "a·b",
            },
        },
        "answer": [
            {
                "matrix": "product",
                "row": 0,
                "column": 0,
                "key": "1",
                "value": "1_",
            },
            {
                "matrix": "product",
                "row": 0,
                "column": 0,
                "key": "5",
                "value": "15",
            },
        ],
    },
    {
        "id": 1,
        "question": {
            "left": {
                "data": [[2]],
                "rows": 1,
                "columns": 1,
                "name": "b",
            },
            "top": {
                "data": [[4]],
                "rows": 1,
                "columns": 1,
                "name": "a",
            },
            "product": {
                "data": [[""]],
                "rows": 1,
                "columns": 1,
                "name": "a·b",
            },
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "8", "value": "8"}
        ],
    },
    {
        "id": 2,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 1, "data": [[2]]},
            "top": {"name": "a", "rows": 1, "columns": 1, "data": [[-3]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "-", "value": "-_"},
            {"matrix": "product", "row": 0, "column": 0, "key": "6", "value": "-6"},
        ],
    },
    {
        "id": 3,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 1, "data": [[2]]},
            "top": {"name": "a", "rows": 1, "columns": 1, "data": [[3]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "6", "value": "6"}
        ],
    },
    {
        "id": 4,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[1, 2]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[1], [1]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "3", "value": "3"}
        ],
    },
    {
        "id": 5,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[1, 2]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[1], [2]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "5", "value": "5"}
        ],
    },
    {
        "id": 6,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[1, 3]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[4], [1]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "7", "value": "7"}
        ],
    },
    {
        "id": 7,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[1, -1]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[4], [1]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "3", "value": "3"}
        ],
    },
    {
        "id": 8,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[0, -1]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[4], [1]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "-", "value": "-_"},
            {"matrix": "product", "row": 0, "column": 0, "key": "1", "value": "-1"},
        ],
    },
    {
        "id": 9,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[0, -3]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[-4], [2]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "-", "value": "-_"},
            {"matrix": "product", "row": 0, "column": 0, "key": "6", "value": "-6"},
        ],
    },
    {
        "id": 10,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[0, -3]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[-4], [0]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "0", "value": "0"}
        ],
    },
    {
        "id": 11,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[1, ""]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[2], [3]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[5]]},
        },
        "answer": [{"matrix": "left", "row": 0, "column": 1, "key": "1", "value": "1"}],
    },
    {
        "id": 12,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[1, ""]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[2], [3]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[2]]},
        },
        "answer": [{"matrix": "left", "row": 0, "column": 1, "key": "0", "value": "0"}],
    },
    {
        "id": 13,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[1, ""]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[4], [3]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[1]]},
        },
        "answer": [
            {"matrix": "left", "row": 0, "column": 1, "key": "-", "value": "-_"},
            {"matrix": "left", "row": 0, "column": 1, "key": "1", "value": "-1"},
        ],
    },
    {
        "id": 14,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 2, "data": [[1, ""]]},
            "top": {"name": "a", "rows": 2, "columns": 1, "data": [[2], [3]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[8]]},
        },
        "answer": [{"matrix": "left", "row": 0, "column": 1, "key": "2", "value": "2"}],
    },
    {
        "id": 15,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [[1, 1, 1]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[1], [2], [3]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "6", "value": "6"}
        ],
    },
    {
        "id": 16,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [[1, 0, -1]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[4], [9], [3]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "1", "value": "1"}
        ],
    },
    {
        "id": 17,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [[1, 0, -1]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[0], [1], [0]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[""]]},
        },
        "answer": [
            {"matrix": "product", "row": 0, "column": 0, "key": "0", "value": "0"}
        ],
    },
    {
        "id": 18,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [[1, 0, ""]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[8], [4], [5]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[3]]},
        },
        "answer": [
            {"matrix": "left", "row": 0, "column": 2, "key": "-", "value": "-_"},
            {"matrix": "left", "row": 0, "column": 2, "key": "1", "value": "-1"},
        ],
    },
    {
        "id": 19,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [["", 1, 0]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[4], [2], [9]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[6]]},
        },
        "answer": [{"matrix": "left", "row": 0, "column": 0, "key": "1", "value": "1"}],
    },
    {
        "id": 20,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [["", 1, 0]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[4], [2], [9]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[-2]]},
        },
        "answer": [
            {"matrix": "left", "row": 0, "column": 0, "key": "-", "value": "-_"},
            {"matrix": "left", "row": 0, "column": 0, "key": "1", "value": "-1"},
        ],
    },
    {
        "id": 21,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [[3, 1, -2]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[1], [1], [""]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[6]]},
        },
        "answer": [
            {"matrix": "top", "row": 2, "column": 0, "key": "-", "value": "-_"},
            {"matrix": "top", "row": 2, "column": 0, "key": "1", "value": "-1"},
        ],
    },
    {
        "id": 22,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [[3, 1, -2]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[1], [4], [""]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[7]]},
        },
        "answer": [{"matrix": "top", "row": 2, "column": 0, "key": "0", "value": "0"}],
    },
    {
        "id": 23,
        "question": {
            "left": {"name": "b", "rows": 1, "columns": 3, "data": [[2, "", -9]]},
            "top": {"name": "a", "rows": 3, "columns": 1, "data": [[1], [3], [0]]},
            "product": {"name": "a·b", "rows": 1, "columns": 1, "data": [[-1]]},
        },
        "answer": [
            {"matrix": "left", "row": 0, "column": 1, "key": "-", "value": "-_"},
            {"matrix": "left", "row": 0, "column": 1, "key": "1", "value": "-1"},
        ],
    },
]


def test_data(item) -> bool:
    import numpy as np

    question = item["question"]
    test_subject = deepcopy(question)

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def do_substition(blank):
        matrix = blank["matrix"]
        row = blank["row"]
        column = blank["column"]
        try:
            value = float(blank["value"])
        except ValueError:
            value = blank["value"]
            pass
        test_subject[matrix]["data"][row][column] = value

    answer = item["answer"]
    for sub in answer:
        print(sub)
        do_substition(sub)

    left = test_subject["left"]
    top = test_subject["top"]
    product = test_subject["product"]

    L, T, P = np.array(left["data"]), np.array(top["data"]), np.array(product["data"])
    print(f"testing problem: {L} @ {T} = {P}")
    assert L.shape == (left["rows"], left["columns"]), f"{L[0]}, {L.shape}"
    assert T.shape == (top["rows"], top["columns"]), f"{T[0]}, {T.shape}"
    assert P.shape == (product["rows"], product["columns"]), f"{P[0]}, {P.shape}"
    assert L @ T == P, f"{L} @ {T} = {L @ T} = {P}?"


class Command(BaseCommand):
    MODE_REFRESH = "refresh"
    MODE_CLEAR = "clear"
    help = "Seed the DotProduct table with 25 prepared problems."

    def handle(self, *args, **kwargs):
        # Step 1: Delete all existing records
        print("Clearing existing problems...")
        DotProductProblem.objects.all().delete()

        # Step 2: Reset auto-increment
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='workbook_dotproductproblem';"
            )

        self.stdout.write("Seeding new problems...")

        # Step 3: Insert new records
        for i, item in enumerate(data):
            print(f"problem #{item['id']}")
            test_data(item)
            DotProductProblem.objects.create(
                id=item["id"], question=item["question"], answer=item["answer"]
            )
            print(f"Inserted problem with id={item['id']}")

        self.stdout.write(
            self.style.SUCCESS(
                "Previous questions deleted and 25 questions have been added to DotProductProblems!"
            )
        )
