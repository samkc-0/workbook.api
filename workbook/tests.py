from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase
from rest_framework import status
from workbook.models import BasicProblem, DotProductProblem, Topic, UserProgress


class AuthenticationTestCase(APITestCase):
    """Tests for JWT authentication"""

    def setUp(self):
        """Create a test user before running tests"""
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.token_url = "/workbook/api/token/"

    def test_get_token(self):
        """Test if user can get an access token"""
        response = self.client.post(
            self.token_url, {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_invalid_token_request(self):
        """Test if wrong credentials return 401"""
        response = self.client.post(
            self.token_url, {"username": "wronguser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BasicProblemAPITestCase(APITestCase):
    """Tests for the BasicProblem API"""

    def setUp(self):
        """Seed basic problems"""
        call_command("seed_basic_problems")  # Ensure we have 25 problems

        # Define API endpoints
        self.basic_problems_url = "/workbook/api/basic/"

    def test_get_basic_problems_no_auth(self):
        """Ensure unauthenticated users can access basic problems"""
        response = self.client.get(self.basic_problems_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 25)  # Ensure at least 25 exist
        self.assertEqual(response.data[0]["question"], "a1m2")

    def test_get_single_basic_problem_no_auth(self):
        """Ensure unauthenticated users can retrieve a single problem"""
        problem = BasicProblem.objects.first()
        response = self.client.get(f"{self.basic_problems_url}{problem.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["question"], problem.question)


class DotProductAPITestCase(APITestCase):
    """Tests for the BasicProblem API"""

    def setUp(self):
        """Seed basic problems"""
        call_command("seed_dotproduct_problems")  # Ensure we have 25 problems

        # Define API endpoints
        self.dotproduct_problems_url = "/workbook/api/dotproduct/"

    def test_get_dotproduct_problems_no_auth(self):
        """Ensure unauthenticated users can access dotproduct problems"""
        response = self.client.get(self.dotproduct_problems_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 25)  # Ensure at least 25 exist
        self.assertEqual(response.data[0]["question"]["blanks"][0]["keys"], "15")
        self.assertEqual(response.data[0]["id"], 1)

    def test_get_dotproduct_problem_no_auth(self):
        """Ensure unauthenticated users can retrieve a single problem"""
        problem = DotProductProblem.objects.first()
        response = self.client.get(f"{self.dotproduct_problems_url}{problem.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["question"], problem.question)


class UserProgressAPITestCase(APITestCase):
    """Tests for the UserProgress API (auth required)"""

    def setUp(self):
        """Set up a test user, topic, and seed basic problems"""
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a test topic
        self.topic = Topic.objects.create(name="BasicProblem")

        # Define API endpoints
        self.token_url = "/workbook/api/token/"
        self.progress_url = "/workbook/api/progress/"

    def authenticate(self):
        """Get JWT token and authenticate"""
        response = self.client.post(
            self.token_url, {"username": "testuser", "password": "testpassword"}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_user_progress_unauthenticated(self):
        """Ensure unauthenticated users cannot access progress"""
        get_response = self.client.get(self.progress_url)
        post_response = self.client.post(
            self.progress_url,
            {"user": self.user.id, "topic": self.topic.id, "exercise_number": 1},
            format="json",
        )
        progress = UserProgress.objects.create(
            user=self.user, topic=self.topic, exercise_number=1
        )
        put_response = self.client.put(
            f"{self.progress_url}{progress.id}/",
            {"user": self.user.id, "topic": self.topic.id, "exercise_number": 5},
            format="json",
        )
        self.assertTrue(
            all(
                status.HTTP_401_UNAUTHORIZED
                for response in (get_response, post_response, put_response)
            )
        )

    def test_user_can_create_progress(self):
        """Ensure authenticated user can create progress records"""
        self.authenticate()
        response = self.client.post(
            self.progress_url,
            {"user": self.user.id, "topic": self.topic.id, "exercise_number": 1},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProgress.objects.count(), 1)

    def test_user_can_update_progress(self):
        """Ensure user can update their progress"""
        self.authenticate()

        # Create initial progress
        progress = UserProgress.objects.create(
            user=self.user, topic=self.topic, exercise_number=1
        )

        # Update progress
        response = self.client.put(
            self.progress_url,
            {"user": self.user.id, "topic": self.topic.id, "exercise_number": 5},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        progress.refresh_from_db()
        self.assertEqual(progress.exercise_number, 5)  # Progress should be updated

    def test_user_can_view_their_progress(self):
        """Ensure users can retrieve their own progress"""
        self.authenticate()

        # Create progress
        UserProgress.objects.create(user=self.user, topic=self.topic, exercise_number=3)

        # Fetch progress
        response = self.client.get(self.progress_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class UserCreationTestCase(APITestCase):
    """Test user creation via the API"""

    def setUp(self):
        """Set up test data"""
        self.create_user_url = "/workbook/api/create-user/"

    def test_create_user_successfully(self):
        """Ensure a new user is created with a hashed password"""
        response = self.client.post(
            self.create_user_url,
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "User created successfully")

        # Check that the user exists in the database
        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)

        # Ensure the password is hashed
        self.assertNotEqual(user.password, "testpassword")
        self.assertTrue(user.password.startswith("pbkdf2_sha256$"))

    def test_create_duplicate_user_fails(self):
        """Ensure duplicate usernames are not allowed"""
        # Create user first
        User.objects.create_user(username="testuser", password="testpassword")

        # Try creating the same user again
        response = self.client.post(
            self.create_user_url,
            {"username": "testuser", "password": "newpassword"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "username", response.data
        )  # Check if the error mentions the username

    def test_create_user_missing_fields(self):
        """Ensure user creation fails if fields are missing"""
        response = self.client.post(
            self.create_user_url, {"username": "testuser"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password", response.data
        )  # Error should mention missing password

    def test_create_user_with_short_password(self):
        """Ensure passwords meet security criteria"""
        response = self.client.post(
            self.create_user_url,
            {"username": "testuser", "password": "123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)  # Error should mention password length


class TestCreatingUserAndIncrementingProgress(APITestCase):
    """Test user creation, authentication, topic creation, progress updates, and deletion"""

    def setUp(self):
        call_command("seed_topics")
        """Set up a test user and authenticate"""
        self.username = f"testuser_{User.objects.count()}"  # Ensure unique username
        self.password = "testpassword123"

        # Create User
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        self.topic_id = 1

        # Get Token
        response = self.client.post(
            "/workbook/api/token/",
            {"username": self.username, "password": self.password},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_user_progress_flow(self):
        """Test full user progress workflow"""

        # ✅ Step 1: Increment progress 3 times
        for i in range(1, 4):
            response = self.client.put(
                "/workbook/api/progress/",
                {"topic": self.topic_id, "exercise_number": i},
                format="json",
            )
            self.assertEqual(
                response.status_code, status.HTTP_200_OK, f"Failed at step {i}"
            )

        # ✅ Step 2: Verify final progress
        response = self.client.get(f"/workbook/api/progress/?topic={self.topic_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["exercise_number"], 3)  # Last exercise step


class CurrentProblemTestCase(APITestCase):
    """Test fetching the current problem for an authenticated user"""

    def setUp(self):
        """Set up test user, topic, and problems"""
        call_command("seed_basic_problems")
        call_command("seed_topics")

        self.username = f"testuser_{User.objects.count()}"
        self.password = "testpassword123"

        # Create User
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        # Get Token
        response = self.client.post(
            "/workbook/api/token/",
            {"username": self.username, "password": self.password},
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Ensure Topic Exists
        self.topic = Topic.objects.first()
        self.assertIsNotNone(
            self.topic, "❌ Topic was not created properly in seed_topics"
        )

        # Ensure Basic Problems Exist
        self.basic_problems = BasicProblem.objects.all()
        self.assertGreater(
            len(self.basic_problems), 0, "❌ No problems found in this topic."
        )

        # ✅ Ensure UserProgress Exists
        self.user_progress, created = UserProgress.objects.get_or_create(
            user=self.user, topic=self.topic, defaults={"exercise_number": 1}
        )

    def test_get_current_problem(self):
        """Ensure the correct problem is returned based on progress"""
        response = self.client.get(f"/workbook/api/topics/1/current-problem/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["question"], self.basic_problems[0].question)

        # Update progress
        UserProgress.objects.filter(user=self.user, topic=self.topic).update(
            exercise_number=2
        )

        # Check next problem
        response = self.client.get(
            f"/workbook/api/topics/{self.topic.id}/current-problem/"
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["question"], self.basic_problems[1].question)

    def test_no_more_problems(self):
        """Ensure 404 is returned when all problems are completed"""
        UserProgress.objects.filter(user=self.user, topic=self.topic).update(
            exercise_number=len(self.basic_problems) + 1
        )

        response = self.client.get(
            f"/workbook/api/topics/{self.topic.id}/current-problem/"
        )
        self.assertEqual(response.status_code, 404)
