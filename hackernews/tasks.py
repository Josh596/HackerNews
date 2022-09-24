from datetime import datetime
from celery import shared_task
from django.db.models import Max
from django.db.utils import IntegrityError
from django.apps import apps

from hackernews_api_wrapper.posts import Post
# from hackernews.utils import available_models
# from .models import Comment, Poll, PollOption, PostBase, Job, Story



def load_to_db(post):
    models = {
        'postbase': apps.get_model('hackernews', 'PostBase'),
        'job': apps.get_model('hackernews', 'Job'),
        'story': apps.get_model('hackernews', 'Story'),
        'poll': apps.get_model('hackernews', 'Poll'),
        'pollopt': apps.get_model('hackernews', 'PollOption'),
        'comment': apps.get_model('hackernews', 'Comment'),
    }

    print(post)
    if post['type'] == 'story':
        # Add to Story Table
        model = models['story']
        # ContentType = apps.get_model('contenttypes', 'ContentType')

        # new_ct = ContentType.objects.get_for_model(model)

        # model.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)

        try:
            model = model.objects.get_or_create(
                hacker_id=post['id'],
                by=post['by'],
                time=datetime.fromtimestamp(post['time']),
                title=post['title'],
                url=post.get('url'),
                score=post['score'])
        except IntegrityError:
            pass

        # model.save()
        pass

    elif post['type'] == 'job':
        # Add to Job Table
        model = models['job']
        # ContentType = apps.get_model('contenttypes', 'ContentType')

        # new_ct = ContentType.objects.get_for_model(model)

        # model.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)
        try:
            model = model.objects.get_or_create(
                hacker_id=post['id'],
                by=post['by'],
                time=datetime.fromtimestamp(post['time']),
                text=post['text'],
                title=post['title'],
                url=post.get('url'))
        except IntegrityError:
            pass

        # model.save()
        pass
    elif post['type'] == 'comment':
        # Add to Comment Table
        model = models['comment']
        # ContentType = apps.get_model('contenttypes', 'ContentType')

        # new_ct = ContentType.objects.get_for_model(model)

        # model.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)
        parent_model = models['postbase']
        try:
            parent = parent_model.objects.get(hacker_id=post['parent'])
        except parent_model.DoesNotExist:
            parent = None
        # print(parent)
        try:
            model = model.objects.get_or_create(
                hacker_id=post['id'],
                by=post['by'],
                time=datetime.fromtimestamp(post['time']),
                parent=parent,
                text=post.get('text'))
        except IntegrityError:
            pass

        # model.save()
        pass
    elif post['type'] == 'poll':
        # Add to poll table
        model = models['poll']
        # ContentType = apps.get_model('contenttypes', 'ContentType')

        # new_ct = ContentType.objects.get_for_model(model)

        # model.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)
        try:
            model = model.objects.get_or_create(
                hacker_id=post['id'],
                by=post['by'],
                time=datetime.fromtimestamp(post['time']),
                text=post['text'],
                title=post['title'],
                url=post.get('url'))
        except IntegrityError:
            pass

        # model.save()
        pass
    elif post['type'] == 'pollopt':
        model = models['pollopt']
        # ContentType = apps.get_model('contenttypes', 'ContentType')

        # new_ct = ContentType.objects.get_for_model(model)

        # model.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)
        poll_model = models['poll']
        parent = poll_model.objects.get(hacker_id=post['parent'])
        try:
            model = model.objects.get_or_create(
                hacker_id=post['id'],
                by=post['by'],
                time=datetime.fromtimestamp(post['time']),
                text=post['text'],
                score=post['score'],
                parent=parent)
        except IntegrityError:
            pass


@shared_task(name = "sync_db")
def sync_db():
    print('Executing task')
    model = apps.get_model('hackernews', 'PostBase')
    minimum_count = 100
    if model.objects.count() == 0:
        posts = Post.get_last_n_post(minimum_count)
    elif model.objects.count() < minimum_count:
        posts = Post.get_last_n_post(100 - model.objects.count())
    else:
        max_id_db = apps.get_model('hackernews', 'PostBase').objects.aggregate(
            Max('hacker_id')).get('hacker_id__max')

        print(max_id_db, 'Max ID')
        posts = Post.get_all_posts_from_id(max_id_db)

    for post in posts:
        load_to_db(post)
        pass    # do your thing here

    # max_id_db = apps.get_model('hackernews', 'PostBase').objects.aggregate(
    #     Max('hacker_id')).get('hacker_id__max')

    # print(max_id_db, 'Max ID')
    # posts = Post.get_all_posts_from_id(max_id_db)

    # for post in posts:
    #     load_to_db(post)
    #     pass    # do your thing here

def sync_db2():
    print('Executing task')
    model = apps.get_model('hackernews', 'PostBase')
    minimum_count = 100
    if model.objects.count() == 0:
        posts = Post.get_last_n_post(minimum_count)
    elif model.objects.count() < minimum_count:
        posts = Post.get_last_n_post(100 - model.objects.count())
    else:
        max_id_db = apps.get_model('hackernews', 'PostBase').objects.aggregate(
            Max('hacker_id')).get('hacker_id__max')

        print(max_id_db, 'Max ID')
        posts = Post.get_all_posts_from_id(max_id_db)

    for post in posts:
        load_to_db(post)
        pass    # do your thing here

# def cron_job():
#     # Step 1
#     # Get the max id from our db
#     # Get posts from range(max_id_api,max_id_db)
#     # Add posts to db
#     pass
