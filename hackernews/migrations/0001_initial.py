# Generated by Django 4.0.7 on 2022-09-24 14:29
from datetime import datetime
from django.db import migrations, models
from django.db.utils import IntegrityError
import django.db.models.deletion

from hackernews_api_wrapper.posts import Post


def load_initial_data(apps, schema_editor):
    models = {
        'postbase': apps.get_model('hackernews', 'PostBase'),
        'job': apps.get_model('hackernews', 'Job'),
        'story': apps.get_model('hackernews', 'Story'),
        'poll': apps.get_model('hackernews', 'Poll'),
        'pollopt': apps.get_model('hackernews', 'PollOption'),
        'comment': apps.get_model('hackernews', 'Comment')
    }

    def load_to_db(post):
        models = {
            'postbase': apps.get_model('hackernews', 'PostBase'),
            'job': apps.get_model('hackernews', 'Job'),
            'story': apps.get_model('hackernews', 'Story'),
            'poll': apps.get_model('hackernews', 'Poll'),
            'pollopt': apps.get_model('hackernews', 'PollOption'),
            'comment': apps.get_model('hackernews', 'Comment'),
        }

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
    data = Post.get_last_n_post(50)
    result = []
    for post in data:
        if post['type'] == 'comment':
            # Store comment referrence until top level parent is found, then from top level parent, create all comments.
            comment_train = []
            comment = post.copy()
            while comment.get('parent'):
                comment = Post.get_parent(comment['id'])
                comment_train.append(comment)
                # print('getting parent')
            else:
                # print('Done to parent')
                comment_train.append(comment)
            # reverse the comment_train and load to db.
            comment_train.reverse()
            for comment in comment_train:
                # pass
                load_to_db(comment)
            result.extend(comment_train)

        elif post['type'] == 'pollopt':
            parent = Post.get_parent(post['id'])

            load_to_db(parent)
            load_to_db(post)

            pass
        else:
            result.append(post)
            load_to_db(post)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hacker_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('by', models.CharField(max_length=100, verbose_name='Author')),
                ('time', models.DateTimeField()),
                ('hacker_url', models.URLField(blank=True, null=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hackernews.postbase')),
                ('text', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('hackernews.postbase',),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hackernews.postbase')),
                ('score', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('hackernews.postbase',),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hackernews.postbase')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('score', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('hackernews.postbase',),
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hackernews.postbase')),
                ('score', models.IntegerField()),
                ('text', models.TextField()),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', related_query_name='option', to='hackernews.poll')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('hackernews.postbase',),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('postbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hackernews.postbase')),
                ('text', models.TextField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kids', related_query_name='kid', to='hackernews.postbase')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('hackernews.postbase',),
        ),
        migrations.RunPython(load_initial_data),
    ]
