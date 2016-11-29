from django.db import models

class CommonManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(active=True, deleted_at=None)

    def inactive(self):
        return self.get_queryset().filter(active=False)