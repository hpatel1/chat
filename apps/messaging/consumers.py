from channels import Channel, Group
from channels.sessions import channel_session
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Message

import json

@receiver(post_save, sender=Message)
def send_update(sender, instance, **kwargs):
    for user in instance.room.users.all():
        if user != instance.from_user:
            print("Sending update")
            unread = instance.room.messages.filter(read=False).count()            
            Group("chat-%s" % user.username).send({
                "text": json.dumps({
                    "room": {
                        "name": instance.room.name,
                        "type": instance.room.type,
                        "id": instance.room.id
                    },
                    "from_user": {
                        "name": instance.from_user.first_name,
                        "id": instance.from_user.id,
                    },
                    "message": instance.message,
                    "read": instance.read,
                    "unread_count": unread
                })
            })

# Connected to websocket.connect
@channel_session
def ws_connect(message):
    print("Connecting")
    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group(room).add(message.reply_channel)
    print("Successfully added")


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group(message.channel_session['room']).discard(message.reply_channel)