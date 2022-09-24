from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel

# Create your models here.
class PostBase(PolymorphicModel):
    hacker_id = models.IntegerField(unique=True, null=True, blank=True)
    by = models.CharField(max_length=100, verbose_name='Author')
    time = models.DateTimeField()
    hacker_url = models.URLField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('hackernews:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if self.hacker_id:
            self.hacker_url = f'https://news.ycombinator.com/item?id={self.hacker_id}'
        return super().save(*args, **kwargs)

    
class Job(PostBase):
    text = models.TextField()
    title = models.CharField(max_length=255)
    url =  models.URLField()


class Story(PostBase):
    title = models.CharField(max_length=255)
    url =  models.URLField(null=True, blank=True)
    score = models.IntegerField()
    # descendants = models.IntegerField()

class Comment(PostBase):
    parent = models.ForeignKey(PostBase, on_delete=models.CASCADE, related_name='kids', related_query_name='kid', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    
class Poll(PostBase):
    # parts
    score = models.IntegerField()
    title = models.CharField(max_length=255)
    text = models.TextField()
    # descendants = models.IntegerField()


class PollOption(PostBase):
    score = models.IntegerField()
    parent = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options', related_query_name='option')
    text = models.TextField()

