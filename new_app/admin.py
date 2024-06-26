from django.contrib import admin
from .models import News, Category, Contact, Comment

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish_time', 'status', 'category']
    list_filter = ['status', 'created_time', 'publish_time']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Contact)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comment', 'active_comment']

    def disable_comment(self, request, queryset):
        queryset.update(active=False)

    def active_comment(self, request, queryset):
        queryset.update(active=True)

# admin.site.register(Comment, CommentAdmin)
