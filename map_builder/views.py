from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from core.models import Floor, Room, Building
from equipment.models import Equipment


@login_required
def map_view(request):
    buildings = Building.objects.prefetch_related('floors').all()
    floor_id = request.GET.get('floor')
    selected_floor = None
    if floor_id:
        selected_floor = get_object_or_404(Floor, pk=floor_id)
    elif buildings.exists() and buildings.first().floors.exists():
        selected_floor = buildings.first().floors.first()
    return render(request, 'map_builder/map.html', {
        'buildings': buildings,
        'selected_floor': selected_floor,
    })


@login_required
def map_editor(request):
    if not request.user.is_admin:
        from django.shortcuts import redirect
        return redirect('map')
    buildings = Building.objects.prefetch_related('floors').all()
    rooms = Room.objects.select_related('floor').all()
    floor_id = request.GET.get('floor')
    selected_floor = None
    if floor_id:
        selected_floor = get_object_or_404(Floor, pk=floor_id)
    return render(request, 'map_builder/editor.html', {
        'buildings': buildings,
        'rooms': rooms,
        'selected_floor': selected_floor,
    })


@login_required
@require_POST
def save_floor_map(request, pk):
    if not request.user.is_admin:
        return JsonResponse({'error': 'Нет прав'}, status=403)
    floor = get_object_or_404(Floor, pk=pk)
    data = json.loads(request.body)
    floor.map_data = data.get('map_data', {})
    floor.save()
    # Save room shapes
    for shape in data.get('shapes', []):
        room_id = shape.get('room_id')
        if room_id:
            Room.objects.filter(pk=room_id).update(shape_data=shape)
    return JsonResponse({'ok': True})


@login_required
def room_info_api(request, pk):
    room = get_object_or_404(Room, pk=pk)
    equipment = Equipment.objects.filter(room=room).select_related('equipment_type')
    items = [{'id': e.id, 'name': f'{e.brand} {e.model}', 'condition': e.condition,
              'condition_display': e.get_condition_display(), 'reg_number': e.reg_number} for e in equipment]
    return JsonResponse({
        'id': room.id,
        'name': room.name,
        'number': room.number,
        'status_color': room.status_color,
        'equipment': items,
        'url': f'/rooms/{room.id}/',
    })
