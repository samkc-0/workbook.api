from django.urls import include, path
from .views import (
    BasicProblemViewSet,
    CurrentProblemView,
    DotProductProblemViewSet,
    UserProgressView,
    RegisterUserView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r"basic", BasicProblemViewSet, basename="basic")
router.register(r"dotproduct", DotProductProblemViewSet, basename="dotproduct")

urlpatterns = [
    path("", include(router.urls)),
    path("progress/", UserProgressView.as_view(), name="user-progress"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create-user/", RegisterUserView.as_view(), name="create-user"),
    path(
        "topics/<int:topic_id>/current-problem/",
        CurrentProblemView.as_view(),
        name="current-problem",
    ),
]
