from django.urls import path
from .views import (
    AssocList, AssocCreate, AssocDeleteAll, AssocLogin,
    AssocUnverified, AssocDetail, AssocVerify, AssocDelete
)

urlpatterns = [
    path('', AssocList.as_view()),
    path('create/', AssocCreate.as_view()),
    path('delete-all/', AssocDeleteAll.as_view()),
    path('login/', AssocLogin.as_view()),
    path('unverified/', AssocUnverified.as_view()),
    path('<int:id>/', AssocDetail.as_view()),
    path('<int:id>/verify/', AssocVerify.as_view()),
    path('<int:id>/delete/', AssocDelete.as_view()),
]
