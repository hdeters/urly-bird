from bookmarks.models import Bookmark, Tag, Click
from users.models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers
from hashids import Hashids
from rest_framework.reverse import reverse


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    class Meta:
        model = Profile
        fields = ('location', 'age', 'interests', 'user')


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
    profile = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile_detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
    tags = TagSerializer(many=True, read_only=True)
    link_url = serializers.CharField(source='url')
    hash_id = serializers.SerializerMethodField()
    _url = serializers.HyperlinkedIdentityField(view_name='bookmark-detail')
    click_count = serializers.IntegerField(read_only=True, source='click_set.count')
    clicks = serializers.HyperlinkedIdentityField(view_name='create_click')
    #_links = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ('id', '_url', 'title', 'desc', 'user', 'marked_at', 'hash_id', 'tags', 'link_url', 'clicks', 'click_count')

    def get_hash_id(self, obj):
        return obj.hash_id

    # def get__links(self, obj):
    #     links = {
    #         "clicks": reverse('create_click', kwargs=dict(pk=obj.id), request=self.context.get('request'))
    #     }
    #     return links

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(**validated_data)
        hashids = Hashids('saltstring')
        hash = hashids.encode(bookmark.id)
        bookmark.hash_id = hash
        bookmark.save()
        return bookmark
