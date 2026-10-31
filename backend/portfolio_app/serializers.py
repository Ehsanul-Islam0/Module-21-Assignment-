from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import (
    Category,
    Comment,
    ContactMessage,
    Education,
    Experience,
    Post,
    PostLike,
    Profile,
    Project,
    Skill,
    Tag,
)

User = get_user_model()


def absolute_url(request, value):
    if not value:
        return value
    if request is None:
        return value
    return request.build_absolute_uri(value)


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'full_name', 'headline', 'bio', 'email', 'phone', 'location',
            'avatar', 'resume', 'github_url', 'linkedin_url', 'x_url', 'website_url',
            'years_of_experience', 'is_available_for_hire', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_avatar(self, obj):
        request = self.context.get('request')
        return absolute_url(request, obj.avatar.url) if obj.avatar else None

    def get_resume(self, obj):
        request = self.context.get('request')
        return absolute_url(request, obj.resume.url) if obj.resume else None


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    def validate_proficiency(self, value):
        if value < 1 or value > 100:
            raise serializers.ValidationError('Proficiency must be between 1 and 100.')
        return value


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

    def validate(self, attrs):
        start_date = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end_date = attrs.get('end_date', getattr(self.instance, 'end_date', None))
        is_current = attrs.get('is_current', getattr(self.instance, 'is_current', False))
        if start_date and start_date > timezone.now().date():
            raise serializers.ValidationError({'start_date': 'Start date cannot be in the future.'})
        if is_current:
            if end_date not in (None, ''):
                raise serializers.ValidationError({'end_date': 'End date must be empty when this is your current role.'})
        else:
            if not end_date:
                raise serializers.ValidationError({'end_date': 'End date is required unless the role is current.'})
            if start_date and end_date and end_date <= start_date:
                raise serializers.ValidationError({'end_date': 'End date must be after start date.'})
        return attrs


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    tech_stack = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())

    class Meta:
        model = Project
        fields = '__all__'

    def get_cover_image(self, obj):
        request = self.context.get('request')
        return absolute_url(request, obj.cover_image.url) if obj.cover_image else None

    def validate(self, attrs):
        live_url = attrs.get('live_url', getattr(self.instance, 'live_url', ''))
        github_url = attrs.get('github_url', getattr(self.instance, 'github_url', ''))
        if not live_url and not github_url:
            raise serializers.ValidationError('At least one of live_url or github_url must be provided.')
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.filter(status='PUBLISHED').count()


class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.filter(status='PUBLISHED').count()


class PostListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    cover_image = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'cover_image', 'category', 'tags',
            'author', 'status', 'published_at', 'views_count', 'reading_time', 'is_featured',
            'likes_count', 'comments_count', 'created_at', 'updated_at'
        ]

    def get_cover_image(self, obj):
        request = self.context.get('request')
        return absolute_url(request, obj.cover_image.url) if obj.cover_image else None

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover_image = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'cover_image', 'category', 'tags',
            'author', 'status', 'published_at', 'views_count', 'reading_time', 'is_featured',
            'likes_count', 'comments_count', 'is_liked', 'created_at', 'updated_at'
        ]

    def get_cover_image(self, obj):
        request = self.context.get('request')
        return absolute_url(request, obj.cover_image.url) if obj.cover_image else None

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        visitor_id = request.headers.get('X-Visitor-Id') if request else None
        if not visitor_id:
            return False
        return PostLike.objects.filter(post=obj, visitor_id=visitor_id).exists()


class PostWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'cover_image', 'category', 'tags',
            'status', 'is_featured'
        ]
        read_only_fields = ['id', 'slug']

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError('Post title must be at least 5 characters long.')
        return value

    def validate(self, attrs):
        status = attrs.get('status', getattr(self.instance, 'status', 'DRAFT'))
        content = attrs.get('content', getattr(self.instance, 'content', ''))
        category = attrs.get('category', getattr(self.instance, 'category', None))
        if status == 'PUBLISHED':
            if not category:
                raise serializers.ValidationError({'category': 'A post must have a category before it can be published.'})
            if len((content or '').strip()) < 100:
                raise serializers.ValidationError({'content': 'Published posts must have at least 100 characters of content.'})
        return attrs

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError('Name must be at least 2 characters long.')
        return value

    def validate_content(self, value):
        if len(value.strip()) < 5 or len(value.strip()) > 1000:
            raise serializers.ValidationError('Comment content must be between 5 and 1000 characters.')
        return value


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

    def validate_message(self, value):
        if len(value.strip()) < 10 or len(value.strip()) > 2000:
            raise serializers.ValidationError('Message must be between 10 and 2000 characters.')
        return value


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
