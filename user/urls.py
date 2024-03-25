from django.urls import path

from user.views import CreateUserView, AllUserView

urlpatterns = [
    path('register/', CreateUserView.as_view()),
    # path('mail-verification/<str:id>/', MailView.as_view()),
    # path('token/', ObtainTokenView.as_view()),
    path('all/', AllUserView.as_view()),
    # path('<str:id>/', ManageView.as_view()),
]
