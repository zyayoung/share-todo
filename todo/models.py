from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Todo(models.Model):
    time_add = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    detail = models.TextField(blank=True)
    deadline = models.DateTimeField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def seconds_left(self):
        return (self.deadline - timezone.now()).total_seconds()

    def state(self):
        if self.done:
            return 'Done'
        elif self.seconds_left() > 0:
            return 'Todo'
        else:
            return 'Exceeded'

    class Meta:
        ordering = ['-deadline']
