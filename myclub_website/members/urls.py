from django.urls import path
from . import views


urlpatterns = [
    # path converter <int:year>/<str:month>/
    # int: number
    # str: string
    # path: url
    # slug: hyphen - and _ underscore
    # UUID: universally unique identifier

    path("", views.login_user, name="login_user"),
    path("logout", views.logout_user, name="logout_user"),
    path("register", views.register_user, name="register_user"),
    path("user_profile", views.user_profile, name="user_profile"),
    path("update_user_profile/<user_name>", views.update_user_profile, name="update_user_profile"),
]
