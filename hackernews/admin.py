from django.contrib import admin
from .models import (Poll, PollOption, PostBase, Story, Job, Comment)

# Register your models here.
admin.site.register(PostBase)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(Story)
admin.site.register(Job)
admin.site.register(Comment)
