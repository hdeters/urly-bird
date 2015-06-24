from bookmarks.models import Bookmark, Tag, Click
from django.contrib.auth.models import User
from rest_framework import serializers
from hashids import Hashids


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name')


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
        fields = ('id', 'username', 'email', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        return user


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    tags = TagSerializer(many=True, read_only=True)
    click_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='click-detail')
    link_url = serializers.CharField(source='url')
    hash_id = serializers.SerializerMethodField()
    _url = serializers.HyperlinkedIdentityField(view_name='bookmark-detail')
    click_this = serializers.HyperlinkedIdentityField(view_name='create_click')

    class Meta:
        model = Bookmark
        fields = (
        'id', '_url', 'title', 'desc', 'user', 'marked_at', 'hash_id', 'tags', 'link_url', 'click_set', 'click_this')

    def get_hash_id(self, obj):
        return obj.hash_id

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(**validated_data)
        hashids = Hashids('saltstring')
        hash = hashids.encode(bookmark.id)
        bookmark.hash_id = hash
        bookmark.save()
        return bookmark
