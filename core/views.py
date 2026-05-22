from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db.models import Count, Q
from django.utils import timezone
from .models import Building, Floor, Room, Notification, ChangeLog
from accounts.models import User
from equipment.models import Equipment


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    ctx = {}

    if user.is_admin or user.is_ahc:
        ctx['total'] = Equipment.objects.count()
        ctx['broken'] = Equipment.objects.filter(condition='broken').count()
        ctx['repair'] = Equipment.objects.filter(condition='repair').count()
        ctx['written_off'] = Equipment.objects.filter(condition='written_off').count()
        ctx['ok'] = Equipment.objects.filter(condition='ok').count()
        ctx['overdue_rooms'] = Room.objects.filter(
            equipment_items__next_check_date__lt=timezone.now().date()
        ).distinct()[:10]
        from requests_app.models import RepairRequest
        ctx['recent_requests'] = RepairRequest.objects.select_related('room', 'created_by').order_by('-created_at')[:5]
        ctx['recent_logs'] = ChangeLog.objects.select_related('user').order_by('-created_at')[:10]

    elif user.is_keeper:
        rooms = user.rooms_kept.all()
        ctx['rooms'] = rooms
        ctx['total'] = Equipment.objects.filter(room__in=rooms).count()
        ctx['broken'] = Equipment.objects.filter(room__in=rooms, condition='broken').count()
        ctx['repair'] = Equipment.objects.filter(room__in=rooms, condition='repair').count()
        ctx['my_equipment'] = Equipment.objects.filter(room__in=rooms).order_by('-date_added')[:10]
        from requests_app.models import RepairRequest
        ctx['my_requests'] = RepairRequest.objects.filter(created_by=user).order_by('-created_at')[:5]

    elif user.is_accountant:
        from django.db.models import Sum
        ctx['total_cost'] = Equipment.objects.filter(cost__isnull=False).aggregate(s=Sum('cost'))['s'] or 0
        ctx['active_cost'] = Equipment.objects.filter(cost__isnull=False).exclude(condition='written_off').aggregate(s=Sum('cost'))['s'] or 0
        ctx['written_off_cost'] = Equipment.objects.filter(cost__isnull=False, condition='written_off').aggregate(s=Sum('cost'))['s'] or 0

    elif user.is_technician:
        from requests_app.models import RepairRequest
        ctx['my_requests'] = RepairRequest.objects.filter(assigned_to=user).order_by('-created_at')

    ctx['unread_notifications'] = Notification.objects.filter(user=user, is_read=False).count()
    return render(request, 'core/dashboard.html', ctx)


@login_required
def floor_list(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    buildings = Building.objects.prefetch_related('floors__rooms').all()
    return render(request, 'core/floor_list.html', {'buildings': buildings})


@login_required
def create_floor(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    if request.method == 'POST':
        building_id = request.POST.get('building')
        number = request.POST.get('number')
        name = request.POST.get('name', '')
        
        if not building_id or not number:
            messages.error(request, 'Заполните все обязательные поля')
            return redirect('create_floor')
        
        try:
            building = Building.objects.get(pk=building_id)
            floor, created = Floor.objects.get_or_create(
                building=building,
                number=int(number),
                defaults={'name': name}
            )
            if created:
                messages.success(request, f'Этаж {number} создан')
            else:
                messages.warning(request, f'Этаж {number} уже существует')
            return redirect('floor_list')
        except Building.DoesNotExist:
            messages.error(request, 'Здание не найдено')
        except ValueError:
            messages.error(request, 'Номер этажа должен быть числом')
    
    buildings = Building.objects.all()
    return render(request, 'core/create_floor.html', {'buildings': buildings})


@login_required
def create_room(request, floor_id):
    if not request.user.is_admin:
        return redirect('dashboard')
    floor = get_object_or_404(Floor, pk=floor_id)
    
    if request.method == 'POST':
        number = request.POST.get('number', '')
        name = request.POST.get('name', '')
        
        if not number or not name:
            messages.error(request, 'Заполните все обязательные поля')
            return redirect('create_room', floor_id=floor_id)
        
        room = Room.objects.create(
            floor=floor,
            number=number,
            name=name
        )
        messages.success(request, f'Кабинет {number} создан')
        return redirect('floor_list')
    
    return render(request, 'core/create_room.html', {'floor': floor})


@login_required
def floor_detail(request, pk):
    floor = get_object_or_404(Floor, pk=pk)
    rooms = floor.rooms.prefetch_related('equipment_items', 'keepers').all()
    return render(request, 'core/floor_detail.html', {'floor': floor, 'rooms': rooms})


@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.user.is_keeper and room not in request.user.rooms_kept.all():
        messages.error(request, 'У вас нет доступа к этому кабинету')
        return redirect('dashboard')
    equipment = room.equipment_items.select_related('equipment_type').all()

    # Apply filters
    condition = request.GET.get('condition')
    eq_type = request.GET.get('type')
    search = request.GET.get('search')
    if condition:
        equipment = equipment.filter(condition=condition)
    if eq_type:
        equipment = equipment.filter(equipment_type_id=eq_type)
    if search:
        equipment = equipment.filter(Q(brand__icontains=search) | Q(model__icontains=search) | Q(reg_number__icontains=search))

    from equipment.models import EquipmentType
    from requests_app.models import RepairRequest
    ctx = {
        'room': room,
        'equipment': equipment,
        'equipment_types': EquipmentType.objects.all(),
        'repair_requests': RepairRequest.objects.filter(room=room).order_by('-created_at')[:5],
        'stats': {
            'total': room.equipment_items.count(),
            'ok': room.equipment_items.filter(condition='ok').count(),
            'broken': room.equipment_items.filter(condition='broken').count(),
            'repair': room.equipment_items.filter(condition='repair').count(),
        }
    }
    return render(request, 'core/room_detail.html', ctx)


@login_required
def create_keeper(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    room = get_object_or_404(Room, pk=pk)
    if room.keepers.count() >= 2:
        messages.error(request, 'В кабинете уже 2 заведующих')
        return redirect('room_detail', pk=pk)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        password = get_random_string(10)
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=User.ROLE_KEEPER,
            password=password,
        )
        room.keepers.add(user)
        messages.success(request, f'Заведующий создан. Логин: {username}, Пароль: {password}')
        return render(request, 'accounts/user_created.html', {
            'new_user': user, 'password': password, 'room': room
        })
    return render(request, 'core/create_keeper.html', {'room': room})


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': notifs})


@login_required
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def changelog(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    logs = ChangeLog.objects.select_related('user').order_by('-created_at')[:100]
    return render(request, 'core/changelog.html', {'logs': logs})


@login_required
def notifications_count_api(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})
