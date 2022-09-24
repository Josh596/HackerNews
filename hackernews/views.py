import bleach
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Poll, PostBase, Story, Comment, PollOption, Job
from .utils import get_model_from_type, available_models
# Create your views here.


def post_list(request, item_type='all'):
    if (item_type not in available_models.keys()):
        raise Http404('Page not found')


    if item_type:
        model = get_model_from_type(item_type)
        posts = model.objects.not_instance_of(Comment, PollOption)
    else:
        posts = PostBase.objects.not_instance_of(Comment, PollOption)

    posts = posts.order_by('time')
    posts_per_page = 30

    paginator = Paginator(posts, posts_per_page)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'hackernews/post/list.html', {'posts': posts, 'types':available_models.keys(), 'active_type': item_type})


def post_detail(request, id):
    post = get_object_or_404(PostBase, id=id)
    # Traverse the comment tree
    # comments = post.kids

    return render(request, 'hackernews/post/detail.html', {'post':post, })

def post_search(request, item_type='all'):
    if (item_type not in available_models.keys()):
        raise Http404('Page not found')

    query = request.GET.get('query', '')
    posts = []
    post_per_page = 30
    # if item_type:
    #     model = get_model_from_type(item_type)
    #     posts = model.objects.all()

    query = bleach.clean(query)

    model = get_model_from_type(item_type)

    model_name = model._meta.object_name
    if model_name in  (Poll._meta.object_name, Job._meta.object_name, Story._meta.object_name): # Search by title
        posts = model.objects.filter(title__icontains=query)
    elif model_name in (PollOption._meta.object_name, Comment._meta.object_name): # Search by text
        posts = model.objects.filter(text__icontains=query)
    elif model_name in PostBase._meta.object_name: # Search by all
        posts = model.objects.filter(
            Q(Story___title__icontains = query) | 
            Q(Job___text__icontains= query) |
            Q(Poll___title__icontains=query)
        )
    # posts = model.objects.filter(
    #     Q(Story___title__lower__trigram_similar = query) | 
    #     Q(Job___text__lower__trigram_similar = query) )
    posts = posts.order_by('time') if posts else posts

    paginator = Paginator(posts, post_per_page)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(
        request, 
        'hackernews/post/list.html', 
        {
            'posts': posts, 
            'types':available_models.keys(), 
            'active_type': item_type,
            'query': query
        }
            )
