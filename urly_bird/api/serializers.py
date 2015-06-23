from bookmarks.models import Bookmark, Tag, Click
from django.contrib.auth.models import User
from rest_framework import serializers
from hashids import Hashids


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

class ClickSerializer(serializers.ModelSerializer):
    bookmark = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Click
        fields = ('user_id', 'bookmark', 'time',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    id = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')

    class Meta:
        model = User
        fields = ('id', 'email', 'username',)


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    click_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='click-detail')
    link_url = serializers.CharField(source='url')
    hash_id = serializers.SerializerMethodField()
    _url = serializers.HyperlinkedIdentityField(view_name='bookmark-detail')

    class Meta:
        model = Bookmark
        fields = ('id', '_url', 'title', 'desc', 'user', 'marked_at', 'hash_id', 'tags', 'link_url', 'click_set')

    def get_hash_id(self, obj):
        return obj.hash_id

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(**validated_data)
        hashids = Hashids('saltstring')
        hash = hashids.encode(bookmark.id)
        bookmark.hash_id = hash
        bookmark.save()
        return bookmark