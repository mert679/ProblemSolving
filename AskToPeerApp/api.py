from .models import Room, DrawingData
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import reverse

def remaining_time_api(request, room_id):
    room = Room.objects.get(id=room_id)
    remaining_time = room.remaining_time()
    seconds = remaining_time.seconds % 60
    minutes = (remaining_time.seconds // 60) % 60
    return JsonResponse({'delete': False, 'minutes': minutes, 'seconds': seconds})

def delete_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        room.delete()
        return JsonResponse({'delete': True})
    except Room.DoesNotExist:
        return JsonResponse({'delete': False, 'error': 'Room not found'}, status=404)
  

def leave_room(request, id):
    room = Room.objects.get(id=id)
    if request.user in room.users.all():
        room.users.remove(request.user)
    return redirect('/home')

def get_rooms(request):
    rooms = Room.objects.all()
    data = [{
        'id': room.id,
        'img_question_url': room.img_question.url,
        'users_count': room.users.count(),
        'name':room.name
    } for room in rooms]
    return JsonResponse(data, safe=False)

def get_coordinates(request,id):
    room = Room.objects.get(id=id)
    coordinates = DrawingData.objects.filter(room=room)
    data_list = [{"x": coord['coordinates'].split(',')[0], "y": coord['coordinates'].split(',')[1]} for coord in coordinates.values()]
    print(data_list)
    return JsonResponse(data_list, safe=False)

def delete_coordinates(request,id):
    room = Room.objects.get(id=id)
    coordinates = DrawingData.objects.filter(room=room)
    coordinates.delete()
    return JsonResponse({'coor_delete': True})
