from django.contrib import admin

from .models import Category, Comment, ContactMessage, Education, Experience, Post, PostLike, Profile, Project, Skill, Tag


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'headline', 'email', 'is_available_for_hire']
    search_fields = ['full_name', 'email', 'location']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_featured']
    search_fields = ['name']
    list_filter = ['category', 'is_featured']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'role', 'employment_type', 'start_date', 'is_current']
    search_fields = ['company', 'role']
    list_filter = ['employment_type', 'is_current']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'field_of_study', 'start_year', 'end_year']
    search_fields = ['institution', 'degree', 'field_of_study']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'completed_date']
    search_fields = ['title', 'summary']
    list_filter = ['category', 'is_featured']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category', 'author', 'published_at', 'views_count']
    search_fields = ['title', 'excerpt', 'content']
    list_filter = ['status', 'category', 'is_featured']


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'visitor_id', 'created_at']
    search_fields = ['visitor_id']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'email', 'is_approved', 'created_at']
    search_fields = ['name', 'content']
    list_filter = ['is_approved', 'post']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_filter = ['is_read']
