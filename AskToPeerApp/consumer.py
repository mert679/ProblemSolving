import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from .models import Room, MessageRoom,User,DrawingData
from asgiref.sync import async_to_sync
import asyncio
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%d' % int(self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self,code):
          await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
      # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room_id_ = data['room_id']

        await self.save_message(username, room_id_, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
      
        if message and username:
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
            
            }))
        
    @sync_to_async
    def save_message(self, username, room_id, message):
        user = User.objects.get(username=username)
        room_ = Room.objects.get(id=room_id)

        MessageRoom.objects.create(user=user, room=room_, content=message)



class WhiteboardConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'whiteboard_%d' % int(self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept() 

    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        coordinates = text_data_json['message']['coordinates']
        room_id_ = text_data_json['roomName']
        async_to_sync(self.save_draw)(room_id_,coordinates)
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'whiteboard_message',
                'message': message
            }
        )
       


    def whiteboard_message(self, event):
        message = event['message']['coordinates'] 
        self.send(text_data=json.dumps({
                'message': message
            }))

    @sync_to_async
    def save_draw(self, room_id, coordinate):
        room_ = Room.objects.get(id=room_id)
        DrawingData.objects.create(room=room_, coordinates=coordinate)


class WhiteboardDeleteConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'whiteboard_delete_%d' % int(self.room_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept() 

    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        room_id_ = text_data_json['roomName']
        async_to_sync(self.delete_draw)(room_id_)
        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'drawing_data_deleted',
                    'room_id': room_id_
                }
            )

        

    @sync_to_async
    def delete_draw(self, room_id):
        room_ = Room.objects.get(id=room_id)
        draw_data_queryset = DrawingData.objects.filter(room=room_)
        for draw_data in draw_data_queryset:
            draw_data.delete()
        
        
    def drawing_data_deleted(self, event):
        room_id = event['room_id']
        message = {'action': 'delete', 'room_id': room_id}
        self.send(text_data=json.dumps({
            'message': message
        }))
        

class VoiceChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'voice_%d' % int(self.room_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept() 

    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # data = json.loads(text_data)

        sdp = text_data
        # sdp = data['sdp']
        # print("sdp"+sdp)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'sdp_message',
                'sdp': sdp
            }
        )
    
    def sdp_message(self, event):
        sdp = event['sdp']
        print(sdp)
        self.send(text_data=sdp)
        # sdp = event['sdp']
        # message = { 'sdp': sdp}
        # print(message)
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))


        # await self.send(text_data=json.dumps({'sdp': sdp}))
        # async_to_sync(self.channel_layer.group_send)(
        #         self.room_group_name,
        #         {
        #             'type': 'drawing_data_deleted',
        #             'room_id': room_id_
        #         }
        #     )
  


    