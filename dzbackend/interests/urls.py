from django.urls import path
from .views import (
    InterestCreateView,
    InterestDeleteView,
    UserInterestsView,
    InterestDetailView,
    UserInterestedEventsView,
    fetchAssoUserInterest,
)

urlpatterns = [
    path("create/", InterestCreateView.as_view()),
    path("delete/", InterestDeleteView.as_view()),
    path("user/<int:user_id>/", UserInterestsView.as_view()),
    path("<int:user_id>/<int:event_id>/", InterestDetailView.as_view()),
    path("user/<int:user_id>/events/", UserInterestedEventsView.as_view()),
    path("assoUserInterest/<int:asso_Id>/",fetchAssoUserInterest.as_view()),
]
