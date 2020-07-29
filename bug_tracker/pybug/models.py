from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from datetime import datetime, timedelta


class Project(models.Model):

    name = models.CharField(max_length=100)
    key = models.CharField(max_length=5,
                                unique=True)
    description = models.TextField()
    lead = models.ForeignKey(User,
                                null=True,
                                on_delete=models.SET_NULL, 
                                related_name='projects')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pybug-projects')


class Priority(models.Model):

    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Ticket(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, 
                                blank=True)
    date_reported = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    reporter = models.ForeignKey(User, 
                                null=True, 
                                on_delete=models.SET_NULL, 
                                related_name='reported_tickets')
    assignee = models.ForeignKey(User, 
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL, 
                                related_name='assigned_tickets')
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='project_tickets')
    priority = models.ForeignKey(Priority,
                                null=True,
                                default=1,
                                on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'key': self.project.key, 'pk': self.pk})


class Comment(models.Model):

    ticket = models.ForeignKey(Ticket,
                            on_delete=models.CASCADE,
                            related_name='comments')
    user = models.ForeignKey(User,
                            null = True,
                            on_delete=models.SET_NULL)
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_human_time(self):
        time = timezone.now()
        minutes_diff = (time - self.timestamp).total_seconds() / 60.0 
        if minutes_diff < 60 :
            return str(int(minutes_diff)) + " minute(s) ago"
        elif self.timestamp.day == time.day:
            return str(time.hour - self.timestamp.hour) + " hour(s) ago"
        elif self.timestamp.month == time.month:
            return str(time.day - self.timestamp.day) + " day(s) ago"
        elif self.timestamp.year == time.year:
            return str(time.month - self.timestamp.month) + " month(s) ago"
        else:
            return self.timestamp

    def __str__(self):
        return f'Comment({self.id}, {self.user.username})'