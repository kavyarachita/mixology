from django.utils import timezone
from django.db import models
from mixology.models import UserProfile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Action(models.Model):
    class Types(models.TextChoices):
        POST = 'PO', 'Post'
        EDIT = 'ED', 'Edit'
        COMMENT = 'CO', 'Comment'
        FOLLOW = 'FO', 'Follow'
        SAVE = 'SA', 'Save'
        
        @classmethod
        def get_verb(cls, action_type):
            return {
                cls.POST: 'posted',
                cls.EDIT: 'edited',
                cls.COMMENT: 'commented',
                cls.FOLLOW: 'followed',
                cls.SAVE: 'saved'
            }.get(action_type, '')
    
    actor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='actions', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=2, choices=Types.choices)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_ct', 'target_id')
    
    def get_human_readable_time(self):
        now = timezone.now()
        diff = now - self.timestamp
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds // 3600 > 0:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds // 60 > 0:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "Just now"  
    
    def __str__(self):
        return f"{self.actor.user.username} {self.action_type} at {self.timestamp}"
    
    def getJSON(self):
        return {
            'id': self.pk,
            'actor': self.actor.user.username,
            'timestamp': self.timestamp,
            'action_type': self.action_type,
            'target': self.target.getJSON(),
            'human_readable_time': self.get_human_readable_time(),
        }
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'