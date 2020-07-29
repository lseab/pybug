from django.contrib import admin
from .models import Ticket, Project, Comment, Priority

admin.site.register(Ticket)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Priority)