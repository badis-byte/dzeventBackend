from django.urls import path
from .views import (
    FollowersCountView,
    FollowUnfollowView,
    FollowedAssociationsView,
)

urlpatterns = [
    path("<int:assoc_id>/count/", FollowersCountView.as_view()),
    path("", FollowUnfollowView.as_view()),
    path("user/<int:user_id>/", FollowedAssociationsView.as_view()),
]
