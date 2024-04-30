from django.urls import path
from .views import index,how_it_works,register_view,login_view,logout_view,HomePageView,ProfilePageView,room_detail, whiteboard_empty
from .api import remaining_time_api,delete_room,leave_room, get_rooms, get_coordinates, delete_coordinates

urlpatterns = [
    path("", index, name="main"),
    path("guide/", how_it_works,name="how_it_works"),
    path("register/", register_view, name = "register"),
    path("login/", login_view, name = "login"),
    path("logout/", logout_view, name = "logout"),
    path("home/", HomePageView, name = "home"),
    path("profile/",ProfilePageView, name="profile"),
    path("<int:id>/",room_detail, name="room_detail"),
    path("whiteboard_empty/",whiteboard_empty, name="whiteboard_empty"),
    # API urls
    path('remaining-time/<int:room_id>/', remaining_time_api, name='remaining_time_api'),
    path('delete-room/<int:room_id>/', delete_room, name='delete_room'),
    path('leave-room/<int:id>/', leave_room, name='leave_room'),
    path("get_rooms/", get_rooms, name="get_rooms"),
    path("get_coordinates/<int:id>/", get_coordinates, name="get_coordinates"),
    path("delete_coordinates/<int:id>/", delete_coordinates, name="delete_coordinates"),
]