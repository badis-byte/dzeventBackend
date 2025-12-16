from django.urls import path
from .views import (
    UserList, UserCreate, UserDeleteAll,
    UserLogin, UserDetail, UserUpdate,
    UserSetFcmtoken
)

urlpatterns = [
    path('', UserList.as_view()),
    path('create/', UserCreate.as_view()),
    path('delete-all/', UserDeleteAll.as_view()),
    path('login/', UserLogin.as_view()),
    path('<int:id>/', UserDetail.as_view()),
    path('<int:id>/update/', UserUpdate.as_view()),
    path('<int:id>/set-fcmtoken', UserSetFcmtoken.as_view())
]
