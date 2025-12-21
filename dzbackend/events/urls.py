from django.urls import path
from .views import (
    EventListCreate,
    EventDetail,
    EventUserList,
    EventFilteredList,
    EventSearch,
    EventDeleteAll,
    NotifyCloseEvent
)

urlpatterns = [
    path('', EventListCreate.as_view(), name='events-list-create'),  # GET all, POST create
    path('association/<int:user_id>/', EventUserList.as_view(), name='events-user-list'),  # GET by user
    path('filtered/', EventFilteredList.as_view(), name='events-filtered'),  # POST with filters
    path('search/', EventSearch.as_view(), name='events-search'),  # POST with searchStr
    path('<int:id>/', EventDetail.as_view(), name='event-detail'),  # GET, PUT, DELETE
    path('delete/all/', EventDeleteAll.as_view(), name='event-delete-all'),  # DELETE all
    path("notify-close-events", NotifyCloseEvent.as_view(), name="notify-close-events")
]
