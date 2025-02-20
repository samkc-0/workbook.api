from django.core.management.base import BaseCommand
from django.db import connection
from workbook.models import DotProductProblem

data = [
    {
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
            "data": [[15]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "15"}
        ],
        "answers": ["15"],
    },
    {
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
            "data": [[8]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "8"}
        ],
        "answers": ["8"],
    },
    {
        "left": {
            "data": [[2]],
            "rows": 1,
            "columns": 1,
            "name": "b",
        },
        "top": {
            "data": [[-3]],
            "rows": 1,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[-6]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "-6"}
        ],
        "answers": ["-6"],
    },
    {
        "left": {
            "data": [[2]],
            "rows": 1,
            "columns": 1,
            "name": "b",
        },
        "top": {
            "data": [[3]],
            "rows": 1,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[6]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "6"}
        ],
        "answers": ["6"],
    },
    {
        "left": {
            "data": [[-3]],
            "rows": 1,
            "columns": 1,
            "name": "b",
        },
        "top": {
            "data": [[-3]],
            "rows": 1,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[9]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "9"}
        ],
        "answers": ["9"],
    },
    {
        "left": {
            "data": [
                [1, 2],
            ],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [1],
                [1],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [
                [3],
            ],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "3"}
        ],
        "answers": ["3"],
    },
    {
        "left": {
            "data": [
                [1, 2],
            ],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [1],
                [2],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [
                [5],
            ],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "5"}
        ],
        "answers": ["5"],
    },
    {
        "left": {
            "data": [[1, 3]],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [4],
                [1],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [
                [7],
            ],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "7"}
        ],
        "answers": ["7"],
    },
    {
        "left": {
            "data": [[1, -1]],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [4],
                [1],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[3]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "3"}
        ],
        "answers": ["3"],
    },
    {
        "left": {
            "data": [[0, -1]],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [4],
                [1],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[-1]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "-1"}
        ],
        "answers": ["-1"],
    },
    {
        "left": {
            "data": [[0, -3]],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [-4],
                [2],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[-6]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "-6"}
        ],
        "answers": ["-6"],
    },
    {
        "left": {
            "data": [
                [0, -3],
            ],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [-4],
                [0],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[0]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "0"}
        ],
        "answers": ["0"],
    },
    {
        "left": {
            "data": [
                [1, 1],
            ],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [2],
                [3],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[5]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "left", "row": 0, "column": 1, "symbol": "", "keys": "1"}
        ],
        "answers": ["1"],
    },
    {
        "left": {
            "data": [[1, 0]],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [2],
                [3],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[2]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "left", "row": 0, "column": 1, "symbol": "", "keys": "0"}
        ],
        "answers": ["0"],
    },
    {
        "left": {
            "data": [[1, -1]],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [4],
                [3],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[1]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "left", "row": 0, "column": 1, "symbol": "", "keys": "-1"}
        ],
        "answers": ["-1"],
    },
    {
        "left": {
            "data": [[1, 2]],
            "rows": 1,
            "columns": 2,
            "name": "b",
        },
        "top": {
            "data": [
                [2],
                [3],
            ],
            "rows": 2,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[8]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "left", "row": 0, "column": 1, "symbol": "", "keys": "2"}
        ],
        "answers": ["2"],
    },
    {
        "left": {
            "data": [[1, 1, 1]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [1],
                [2],
                [3],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[6]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "6"}
        ],
        "answers": ["6"],
    },
    {
        "left": {
            "data": [[1, 0, -1]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [4],
                [9],
                [3],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[1]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "1"}
        ],
        "answers": ["1"],
    },
    {
        "left": {
            "data": [[1, 0, -1]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [0],
                [1],
                [0],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[0]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "product", "row": 0, "column": 0, "symbol": "", "keys": "0"}
        ],
        "answers": ["0"],
    },
    {
        "left": {
            "data": [[1, 0, -1]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [8],
                [4],
                [5],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[3]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "left", "row": 0, "column": 2, "symbol": "", "keys": "-1"}
        ],
        "answers": ["-1"],
    },
    {
        "left": {
            "data": [[1, 1, 0]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [4],
                [2],
                [9],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[6]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "left", "row": 0, "column": 0, "symbol": "", "keys": "1"}
        ],
        "answers": ["1"],
    },
    {
        "left": {
            "data": [[-1, 1, 0]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [4],
                [2],
                [9],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[-2]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "left", "row": 0, "column": 0, "symbol": "", "keys": "-1"}
        ],
        "answers": ["-1"],
    },
    {
        "left": {
            "data": [[3, 1, -2]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [1],
                [1],
                [-1],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[6]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "top", "row": 2, "column": 0, "symbol": "", "keys": "-1"}
        ],
        "answers": ["-1"],
    },
    {
        "left": {
            "data": [[3, 1, -2]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [1],
                [4],
                [0],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[7]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [{"matrix": "top", "row": 2, "column": 0, "symbol": "", "keys": "0"}],
        "answers": ["0"],
    },
    {
        "left": {
            "data": [[2, -1, -9]],
            "rows": 1,
            "columns": 3,
            "name": "b",
        },
        "top": {
            "data": [
                [1],
                [3],
                [0],
            ],
            "rows": 3,
            "columns": 1,
            "name": "a",
        },
        "product": {
            "data": [[-1]],
            "rows": 1,
            "columns": 1,
            "name": "a·b",
        },
        "blanks": [
            {"matrix": "left", "row": 0, "column": 1, "symbol": "", "keys": "-1"}
        ],
        "answers": ["-1"],
    },
]


def test_data(item) -> bool:
    import numpy as np

    left = item["left"]
    top = item["top"]
    product = item["product"]
    blanks = item["blanks"]
    answers = item["answers"]
    L, T, P = np.array(left["data"]), np.array(top["data"]), np.array(product["data"])
    print(f"testing problem: {L} @ {T} = {P}")
    assert L.shape == (left["rows"], left["columns"]), f"{L[0]}, {L.shape}"
    assert T.shape == (top["rows"], top["columns"]), f"{T[0]}, {T.shape}"
    assert P.shape == (product["rows"], product["columns"]), f"{P[0]}, {P.shape}"
    assert L @ T == P, f"{L} @ {T} = {L @ T} = {P}?"
    for blank, answer in zip(blanks, answers):
        matrix_key = blank["matrix"]
        i = blank["row"]
        j = blank["column"]
        blanked = item[matrix_key]["data"][i][j]
        print(blanked, i, j)
        assert float(blanked) == float(answer), f"{blanked} is not {answer}"
        assert blank["keys"] == answer


class Command(BaseCommand):
    MODE_REFRESH = "refresh"
    MODE_CLEAR = "clear"
    help = "Seed the BasicProblem table with 25 random problems."

    def handle(self, *args, **kwargs):
        # delete existing questions
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name='workbook_dotproductproblem';"
            )
        self.stdout.write("Seeding new problems...")
        for i, item in enumerate(data):
            print(f"problem #{i}")
            test_data(item)
            DotProductProblem.objects.create(question=item, answer=item["answers"])

        self.stdout.write(
            self.style.SUCCESS(
                "Previous questions deleted and 25 questions have been added to DotProductProblems!"
            )
        )
