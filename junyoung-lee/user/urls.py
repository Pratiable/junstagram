from django.urls import path

from user.views    import SignupView, SigninView
from follows.views import FollowView, FollowerView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
    path('/<int:user_id>/follow', FollowView.as_view()),
    path('/<int:user_id>/followers', FollowerView.as_view()),
]