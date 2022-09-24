from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from hackernews.models import PostBase, Poll, PollOption, Comment, Job, Story


class PostBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostBase
        fields = '__all__'
        exclude = ('polymorphic_ctype', )
        kwargs = {
            'id': {'read_only': True},
            'hacker_id': {'read_only': True},
            'time': {'read_only': True}
        }

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('polymorphic_ctype', )
        kwargs = {
            'id': {'read_only': True},
            'hacker_id': {'read_only': True},
            'time': {'read_only': True}
        }

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        exclude = ('polymorphic_ctype', )
        kwargs = {
            'id': {'read_only': True},
            'hacker_id': {'read_only': True},
            'time': {'read_only': True}
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('polymorphic_ctype', )
        kwargs = {
            'id': {'read_only': True},
            'hacker_id': {'read_only': True},
            'time': {'read_only': True}
        }

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        exclude = ('polymorphic_ctype', )
        kwargs = {
            'id': {'read_only': True},
            'hacker_id': {'read_only': True},
            'time': {'read_only': True}
        }

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        exclude = ('polymorphic_ctype', )
        kwargs = {
            'id': {'read_only': True},
            'hacker_id': {'read_only': True},
            'time': {'read_only': True}
        }

class PostPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = 'item_type'
    model_serializer_mapping = {
        PostBase: PostBaseSerializer,
        Job: JobSerializer,
        Story: StorySerializer,
        Comment: CommentSerializer,
        Poll: PollSerializer,
        PollOption: PollOptionSerializer
    }

