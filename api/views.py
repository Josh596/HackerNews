from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from hackernews.models import PostBase, Poll, PollOption, Comment, Job, Story
from hackernews.utils import available_models
from .serializers import PostBaseSerializer, PollOptionSerializer, PollSerializer, PostPolymorphicSerializer, StorySerializer, JobSerializer
# Create your views here.


@api_view(['GET'])
def getPost(request):
    post_type = request.GET.get('type', 'all')

    assert post_type in available_models
    model = available_models.get(post_type)

    posts = model.objects.all()
    serializer = PostPolymorphicSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addPost(request):
    print(request.data)
    serializer = PostPolymorphicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print('No match', serializer.error_messages, serializer.errors)
    return Response(serializer.data)

@api_view(['POST'])
def updatePost(request):
    data = request.data
    post = PostBase.objects.get(id=data['id'])
    if not post.hacker_id:
        for attr in data:
            if attr not in ['id', 'hacker_id', 'time', 'by']:
                if attr in dir(post):
                    setattr(post, attr, data[attr])
        post.save()
        
        serializer = PostPolymorphicSerializer(post)
        # if serializer.is_valid():
        #     serializer.update()
        # else:
        #     print('No match in update', serializer.error_messages, serializer.errors)
    else:
        print("Cannot edit this post")
        return Response({'error': 'Cannot update this item'})
    return Response(serializer.data)

@api_view(['POST'])
def deletePost(request):
    data = request.data
    post = PostBase.objects.get(id=data['id'])
    if not post.hacker_id:
        post.delete()
        # if serializer.is_valid():
        #     serializer.update()
        # else:
        #     print('No match in update', serializer.error_messages, serializer.errors)
    else:
        print("Cannot edit this post")
        return Response({'error': 'Cannot update this item'})
    return Response({'message': 'Post successfully deleted'})



