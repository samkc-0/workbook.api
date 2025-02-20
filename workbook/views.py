from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import BasicProblem, DotProductProblem, Topic, UserProgress
from .serializers import (
    BasicProblemSerializer,
    DotProductProblemSerializer,
    UserProgressSerializer,
    UserSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated


# User Registration API
class RegisterUserView(APIView):
    """API View to create a new user"""

    permission_classes = [AllowAny]  # Open for user registration

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            return Response(
                {"message": "User created successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasicProblemViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """API to list all basic problems and retrieve a single problem by ID"""

    queryset = BasicProblem.objects.all()
    serializer_class = BasicProblemSerializer
    permission_classes = [AllowAny]


class DotProductProblemViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """API to list all dotproduct problems and retrieve a single problem by ID"""

    queryset = DotProductProblem.objects.all()
    serializer_class = DotProductProblemSerializer
    permission_classes = [AllowAny]


# API to track user progress
class UserProgressView(APIView):
    """Allows users to submit a new progress report or update an existing one"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieve the authenticated user's progress"""
        user = request.user
        topic_id = request.query_params.get("topic", None)  # Optional topic filter

        if topic_id:
            progress = UserProgress.objects.filter(user=user, topic_id=topic_id).first()
            if progress:
                return Response(UserProgressSerializer(progress).data)
            return Response({"error": "No progress found for this topic."}, status=404)

        # If no topic filter, return all progress records for the user
        progress = UserProgress.objects.filter(user=user)
        return Response(UserProgressSerializer(progress, many=True).data)

    def post(self, request, *args, **kwargs):
        """Create a new progress entry (or prevent duplicates)"""
        user = request.user
        topic_id = request.data.get("topic")
        exercise_number = request.data.get("exercise_number")

        # Ensure topic is provided
        if not topic_id:
            return Response({"error": "Topic ID is required"}, status=400)

        # Check if progress already exists for this user and topic
        if UserProgress.objects.filter(user=user, topic_id=topic_id).exists():
            return Response(
                {"error": "Progress for this topic already exists."}, status=400
            )

        # Create a new progress report
        progress = UserProgress.objects.create(
            user=user, topic_id=topic_id, exercise_number=exercise_number
        )
        return Response(UserProgressSerializer(progress).data, status=201)

    def put(self, request, *args, **kwargs):
        """Update an existing progress entry"""
        user = request.user
        topic_id = request.data.get("topic")
        exercise_number = request.data.get("exercise_number")

        # Ensure topic is provided
        if not topic_id:
            return Response({"error": "Topic ID is required"}, status=400)

        # Get or create progress entry for the user & topic
        progress, created = UserProgress.objects.get_or_create(
            user=user, topic_id=topic_id
        )
        progress.exercise_number = exercise_number
        progress.save()

        return Response(UserProgressSerializer(progress).data)


class CurrentProblemView(APIView):
    """Returns the next problem for a given topic based on the user's progress"""

    permission_classes = [IsAuthenticated]

    def get(self, request, topic_id):
        """Retrieve the next problem based on user progress"""
        user = request.user

        # Ensure topic exists
        topic = get_object_or_404(Topic, id=topic_id)

        # Get user progress for this topic (default to first exercise if none exists)
        progress, created = UserProgress.objects.get_or_create(user=user, topic=topic)

        # Find the next problem based on progress
        problem = (
            BasicProblem.objects.all()
            .order_by("id")[progress.exercise_number - 1 : progress.exercise_number]
            .first()
        )

        if not problem:
            return Response(
                {"message": "No more problems available for this topic."}, status=404
            )

        return Response(BasicProblemSerializer(problem).data, status=200)
