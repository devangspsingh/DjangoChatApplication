from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatMessage


# List of available users to chat with
@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(
        request,
        "chat/user_list.html",
        {"users": users},
    )


# Chat room for a specific user
@login_required
def chat_room(request, user_id):
    users = User.objects.exclude(id=request.user.id)
    other_user = get_object_or_404(User, id=user_id)
    messages = ChatMessage.objects.filter(
        sender=request.user, receiver=other_user
    ) | ChatMessage.objects.filter(sender=other_user, receiver=request.user)
    messages = messages.order_by("timestamp")
    return render(
        request,
        "chat/chat_room.html",
        {"messages": messages, "other_user": other_user, "users": users},
    )
