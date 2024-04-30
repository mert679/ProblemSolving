from django.urls import re_path
from . import consumer

websocket_urlpatterns =[
    re_path(r'ws/(?P<room_name>\d+)/',consumer.ChatConsumer.as_asgi()),
    re_path(r'ws/whiteboard/(?P<room_name>\d+)/', consumer.WhiteboardConsumer.as_asgi()),
    re_path(r'ws/whiteboard_delete/(?P<room_name>\d+)/', consumer.WhiteboardDeleteConsumer.as_asgi()),
    re_path(r'ws/voice/(?P<room_name>\d+)/', consumer.VoiceChatConsumer.as_asgi()),
]