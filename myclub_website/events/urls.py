from django.urls import path
from . import views


urlpatterns = [
    # path converter <int:year>/<str:month>/
    # int: number
    # str: string
    # path: url
    # slug: hyphen - and _ underscore
    # UUID: universally unique identifier

    path('', views.home, name='home'),
    path("<int:year>/<str:month>/", views.home, name="home"),
    path("events", views.all_events, name="event_list"),
    path("add_venue", views.add_venue, name="add_venue"),
    path("add_user", views.add_user, name="add_user"),
    path("venues", views.all_venues, name="venue_list"),
    path("show_venue/<venue_id>", views.show_venue, name="show_venue"),
    path("users", views.all_users, name="user_list"),
    path("show_user/<user_id>", views.show_user, name="show_user"),
    path("custom_calendar", views.custom_calendar, name="custom_calendar"),
    path("search_venue", views.search_venue, name="search_venue"),
    path("search", views.search, name="search"),
    path("show_event/<event_id>", views.show_event, name="show_event"),
    path("update_venue/<venue_id>", views.update_venue, name="update_venue"),
    path("update_user/<user_id>", views.update_user, name="update_user"),
    path("add_event", views.add_event, name="add_event"),
    path("update_event/<event_id>", views.update_event, name="update_event"),
    path("delete_event/<event_id>", views.delete_event, name="delete_event"),
    path("delete_user/<user_id>", views.delete_user, name="delete_user"),
    path("delete_venue/<venue_id>", views.delete_venue, name="delete_venue"),
    path("venue_text", views.venue_text, name="venue_text"),
    path("venue_csv", views.venue_csv, name="venue_csv"),
    path("venue_pdf", views.venue_pdf, name="venue_pdf"),
    path("my_events", views.my_events, name="my_events"),
]
