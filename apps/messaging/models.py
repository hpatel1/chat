from __future__ import unicode_literals

from django.db import models


class ChatRoom(models.Model):
    CHAT_TYPE = (
        ('individual', 'Individual'),
        ('group', 'Group'),
    )
    owner = models.ForeignKey('authentication.User',
                            null=True, related_name='own_rooms')

    users = models.ManyToManyField('authentication.User',
                            related_name='chat_rooms')
    name = models.CharField(max_length=100,
                            null=True, blank=True)
    type = models.CharField(choices=CHAT_TYPE,
                            default='individual', max_length=20)
    last_message = models.ForeignKey('messaging.Message',
                            null=True, blank=True, related_name='chat_room')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return '-'.join([self.type, self.name])


class MessageManager(models.Manager):
    def unread_messages(self):
        return self.get_queryset().filter(read=False)


class Message(models.Model):
    from_user =  models.ForeignKey('authentication.User',
                            related_name='sent_messages')

    room = models.ForeignKey('messaging.ChatRoom',
                            related_name='messages')

    message = models.TextField(null=False)

    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        self.room.last_message = self
        self.room.save()