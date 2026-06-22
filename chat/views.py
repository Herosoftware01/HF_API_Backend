from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.db.models import Q, Max, Prefetch
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import get_user_model
User = get_user_model()
import json

from .models import Room, Message, Profile
from .forms import RegisterForm, ProfileUpdateForm, CreateGroupForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import json
import tempfile
import subprocess
import os
import io


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'chat/register.html', {'form': form})


@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            Profile.objects.filter(user=user).update(is_online=True)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        Profile.objects.filter(user=request.user).update(is_online=False, last_seen=timezone.now())
    logout(request)
    return redirect('login')


@login_required
def home(request):
    Profile.objects.get_or_create(user=request.user)
    rooms = request.user.rooms.all().prefetch_related('members', 'members__profile')
    rooms_data = []
    for room in rooms:
        last_msg = room.messages.last()
        unread = room.messages.filter(is_read=False).exclude(sender=request.user).count()
        rooms_data.append({
            'room': room,
            'last_msg': last_msg,
            'unread': unread,
            'display_name': room.get_display_name(request.user),
            'display_avatar': room.get_display_avatar(request.user),
        })
    all_users = User.objects.exclude(id=request.user.id).select_related('profile')
    return render(request, 'chat/home.html', {
        'rooms_data': rooms_data,
        'all_users': all_users,
        'user': request.user,
    })


@login_required
def room_view(request, room_id):
    Profile.objects.get_or_create(user=request.user)
    room = get_object_or_404(Room, id=room_id)
    if request.user not in room.members.all():
        return redirect('home')
    messages = room.messages.select_related('sender', 'sender__profile').order_by('timestamp')
    room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    rooms = request.user.rooms.all()
    rooms_data = []
    for r in rooms:
        last_msg = r.messages.last()
        unread = r.messages.filter(is_read=False).exclude(sender=request.user).count()
        rooms_data.append({
            'room': r,
            'last_msg': last_msg,
            'unread': unread,
            'display_name': r.get_display_name(request.user),
            'display_avatar': r.get_display_avatar(request.user),
        })
    all_users = User.objects.exclude(id=request.user.id).select_related('profile')
    other_user = None
    if room.room_type == 'direct':
        other_user = room.get_other_user(request.user)
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages,
        'rooms_data': rooms_data,
        'all_users': all_users,
        'other_user': other_user,
        'members': room.members.select_related('profile').all(),
    })


@login_required
def start_direct_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    existing = Room.objects.filter(room_type='direct', members=request.user).filter(members=other_user)
    if existing.exists():
        return redirect('room', room_id=existing.first().id)
    room = Room.objects.create(room_type='direct', name=f'{request.user.username}-{other_user.username}')
    room.members.add(request.user, other_user)
    return redirect('room', room_id=room.id)


@login_required
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            room = Room.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data.get('description', ''),
                room_type='group',
                admin=request.user,
            )
            if form.cleaned_data.get('avatar'):
                room.avatar = form.cleaned_data['avatar']
                room.save()
            room.members.add(request.user)
            for member in form.cleaned_data['members']:
                room.members.add(member)
            return redirect('room', room_id=room.id)
    else:
        form = CreateGroupForm(request.user)
    return render(request, 'chat/create_group.html', {'form': form})


@csrf_exempt
@login_required
@require_POST
def upload_file(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user not in room.members.all():
        return JsonResponse({'error': 'Not a member'}, status=403)
    f = request.FILES.get('file')
    if not f:
        return JsonResponse({'error': 'No file'}, status=400)
    msg = Message.objects.create(
        room=room, sender=request.user,
        content=request.POST.get('caption', ''),
        file=f, file_name=f.name,
        file_type=f.content_type,
    )
    profile = getattr(request.user, 'profile', None)
    return JsonResponse({
        'message_id': msg.id,
        'sender_id': request.user.id,
        'sender_name': request.user.username,
        'avatar': profile.avatar.url if profile and profile.avatar else None,
        'timestamp': msg.timestamp.strftime('%I:%M %p'),
        'file': msg.file.url,
        'file_name': msg.file_name,
        'file_type': msg.file_type,
        'content': msg.content,
    })


@login_required
def profile_view(request, username=None):
    if username:
        target_user = get_object_or_404(User, username=username)
    else:
        target_user = request.user
    Profile.objects.get_or_create(user=target_user)
    if request.method == 'POST' and target_user == request.user:
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=target_user.profile, initial={
            'first_name': target_user.first_name,
            'last_name': target_user.last_name,
            'email': target_user.email,
        })
    return render(request, 'chat/profile.html', {'target_user': target_user, 'form': form, 'is_own': target_user == request.user})


@login_required
def user_status_api(request):
    user_ids = request.GET.get('ids', '').split(',')
    profiles = Profile.objects.filter(user_id__in=user_ids).values('user_id', 'is_online', 'last_seen')
    return JsonResponse({str(p['user_id']): {'is_online': p['is_online']} for p in profiles})


@login_required
def messages_api(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.user not in room.members.all():
        return JsonResponse({'error': 'Not allowed'}, status=403)

    after_id = request.GET.get('after')
    messages = room.messages.select_related('sender', 'sender__profile').order_by('id')

    if after_id and after_id.isdigit():
        messages = messages.filter(id__gt=int(after_id))
    else:
        messages = messages.order_by('-id')[:50]
        messages = sorted(messages, key=lambda msg: msg.id)

    room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    data = []
    for msg in messages:
        profile = getattr(msg.sender, 'profile', None)
        data.append({
            'message_id': msg.id,
            'message': msg.content,
            'sender_id': msg.sender_id,
            'sender_name': msg.sender.username,
            'avatar': profile.avatar.url if profile and profile.avatar else None,
            'timestamp': msg.timestamp.strftime('%I:%M %p'),
            'file': msg.file.url if msg.file else None,
            'file_name': msg.file_name,
            'file_type': msg.file_type,
        })

    return JsonResponse({'messages': data})

@csrf_exempt
@login_required
@require_POST
def send_message(request, room_id):
    
    room = get_object_or_404(Room, id=room_id)

    if request.user not in room.members.all():
        return JsonResponse({'error': 'Not allowed'}, status=403)
   
    content = request.POST.get('content')

    if content:

        msg = Message.objects.create(
            room=room,
            sender=request.user,
            content=content
        )

        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return redirect('room', room_id=room.id)

        return JsonResponse({
            'id': msg.id,
            'message_id': msg.id,
            'sender': msg.sender.username,
            'sender_id': msg.sender_id,
            'sender_name': msg.sender.username,
            'content': msg.content,
            'message': msg.content,
            'time': msg.timestamp.strftime('%I:%M %p'),
            'timestamp': msg.timestamp.strftime('%I:%M %p'),
            'avatar': None,
            'file': None,
            'file_name': '',
            'file_type': '',
        })

    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return redirect('room', room_id=room.id)

    return JsonResponse({'error': 'Empty message'}, status=400)






@csrf_exempt
def html_to_image(request):
    try:
        data = json.loads(request.body)
        html_content = data.get("html")

        if not html_content:
            return JsonResponse(
                {"error": "html field is required"},
                status=400
            )

        with tempfile.TemporaryDirectory() as temp_dir:

            html_file = os.path.join(temp_dir, "input.html")
            png_file = os.path.join(temp_dir, "output.png")

            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            subprocess.run([
                r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe",
                "--quality", "100",
                "--enable-local-file-access",
                html_file,
                png_file
            ], check=True)

            img = Image.open(png_file)

            output = io.BytesIO()

            img.save(
                output,
                format="PNG",
                optimize=True,
                compress_level=9
            )

            image_data = output.getvalue()

            # Optional: reject if > 5 MB
            size_mb = len(image_data) / (1024 * 1024)

            if size_mb > 5:
                return JsonResponse({
                    "error": f"Image size is {size_mb:.2f} MB (> 5 MB)"
                }, status=400)

        return HttpResponse(
            image_data,
            content_type="image/png"
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
