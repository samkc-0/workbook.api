from django.db import models
from django.contrib.auth.models import User
import numpy as np


from django.db import models


class BasicProblem(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class DotProductProblem(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.JSONField()
    answer = models.JSONField()

    def __str__(self):
        top = self.question["top"]
        left = self.question["left"]
        product = self.question["product"]
        blank = self.question["blank"]
        return f"{top} · {left} = {product}; blank {blank['matrix']}[{blank['row']}][{blank['column']}]..."

    def validate(self) -> bool:
        item = self.question
        left = item["left"]
        top = item["top"]
        product = item["product"]
        blanks = item["blanks"]
        answers = item["answers"]
        L, T, P = (
            np.array(left["data"]),
            np.array(top["data"]),
            np.array(product["data"]),
        )
        assert L.shape == (left["rows"], left["columns"])
        assert T.shape == (top["rows"], top["columns"])
        assert P.shape == (product["rows"], product["columns"])
        assert L @ T == P
        for blank, answer in zip(blanks, answers):
            assert float(item[blank["matrix"]][blank["row"]][blank["column"]]) == float(
                answer
            )
            assert blank["keys"] == answer
        return True


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="progress")
    exercise_number = models.PositiveIntegerField(
        default=1
    )  # The latest exercise reached

    class Meta:
        unique_together = ("user", "topic")  # Ensures one row per (user, topic)

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - Exercise {self.exercise_number}"
