from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Max, OuterRef, Subquery, DateTimeField
from django.contrib.auth import get_user_model
from .models import Message
from .serializers import MessageSerializer

User = get_user_model()

# ────────────────────────────────────────────────────────
# 👥 பயனர் பட்டியல் (Last Message Time பேஸ் பண்ணி துல்லியமான டாப் சார்ட்டிங்)
# ────────────────────────────────────────────────────────
class ChatUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        
        # ⏳ சப்-குரி மூலம் மூர்த்திக்கும் ஒவ்வொரு யூசருக்கும் இடையே உள்ள கடைசி மெசேஜ் நேரத்தைக் கண்டுபிடித்தல்
        last_message_time_subquery = Message.objects.filter(
            (Q(sender=current_user) & Q(receiver=OuterRef('pk'))) |
            (Q(sender=OuterRef('pk')) & Q(receiver=current_user))
        ).order_by('-id').values('timestamp')[:1] # உங்க மாடலில் 'timestamp' அல்லது 'created_at' எதுவோ அதை போடுங்க

        # உங்களைத் தவிர மற்ற பயனர்களை எடுத்து, கடைசி மெசேஜ் நேரத்தின் அடிப்படையில் இறங்குவரிசையில் (Latest First) பிரிக்கிறோம்
        all_users = User.objects.exclude(id=current_user.id).annotate(
            last_interaction=Subquery(last_message_time_subquery, output_field=DateTimeField())
        ).order_by('-last_interaction') # 👈 இதுதான் லேட்டஸ்ட் சாட்டை டாப்-க்கு கொண்டு வரும் மேஜிக் வொர்க்

        user_list = []
        for user in all_users:
            # இவர்களுக்கிடையே கடைசியாக வந்த மெசேஜ் டெக்ஸ்ட்
            last_msg = Message.objects.filter(
                (Q(sender=current_user) & Q(receiver=user)) |
                (Q(sender=user) & Q(receiver=current_user))
            ).order_by('-id').first()
            
            # படிக்காத மெசேஜ் கவுண்ட்
            unread_cnt = Message.objects.filter(
                sender=user,
                receiver=current_user,
                is_read=False
            ).count() if hasattr(Message, 'is_read') else 0

            # ஆன்லைன் ஸ்டேட்டஸ்
            is_online = False
            if hasattr(user, 'userstatus'):
                is_online = user.userstatus.is_online

            # நேர ஃபார்மட்
            msg_time = ""
            if last_msg:
                # 'timestamp' அல்லது 'created_at' உங்க மாடலுக்கு ஏற்ப மாற்றவும்
                t = last_msg.timestamp if hasattr(last_msg, 'timestamp') else last_msg.created_at
                msg_time = t.strftime('%I:%M %p') if t else ""

            user_list.append({
                "id": user.id,
                "username": user.username,
                "is_online": is_online,
                "unread_count": unread_cnt,
                "last_message": last_msg.content if last_msg else "No messages yet",
                "last_msg_time": msg_time
            })
        
        return Response(user_list)


# ────────────────────────────────────────────────────────
# 2. 👁️ மெசேஜ்களைப் படித்ததாக மாற்றுதல் (Mark Read API)
# ────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_messages_as_read(request, user_id):
    current_user = request.user
    if hasattr(Message, 'is_read'):
        Message.objects.filter(
            sender_id=user_id,
            receiver=current_user,
            is_read=False
        ).update(is_read=True)
    return Response({"status": "Messages marked as read"}, status=200)


# ────────────────────────────────────────────────────────
# 3. 📜 சாட் ஹிஸ்டரி (Chat History API)
# ────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request, user_id):
    logged_in_user = request.user
    if not logged_in_user or logged_in_user.is_anonymous:
        return Response({"error": "Authentication credentials were not provided."}, status=401)
        
    order_field = 'timestamp' if hasattr(Message, 'timestamp') else 'id'
    messages = Message.objects.filter(
        (Q(sender=logged_in_user) & Q(receiver_id=user_id)) |
        (Q(sender_id=user_id) & Q(receiver=logged_in_user))
    ).order_by(order_field)
    
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=200)


# ────────────────────────────────────────────────────────
# 4. 📎 ஃபைல் அப்லோடு (File Upload API)
# ────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file_api(request):
    sender = request.user
    receiver_id = request.data.get('receiver_id')
    file = request.FILES.get('file')
    is_image = request.data.get('is_image', 'false') == 'true'

    if not file or not receiver_id:
        return Response({"error": "Invalid Data"}, status=400)

    receiver = User.objects.get(id=receiver_id)
    msg = Message.objects.create(
        sender=sender, 
        receiver=receiver, 
        file_upload=file, 
        is_image=is_image
    )
    serializer = MessageSerializer(msg)
    return Response(serializer.data)