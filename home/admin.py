from django.contrib import admin
from .models import Post, Comments


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'created', 'updated')
    search_fields = ('slug', 'body')
    list_filter = ('created', 'updated')
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug': ('body',)}

# admin.site.register(Post, PostAdmin)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_reply')
    search_fields = ('user', 'body')
    list_filter = ('user', 'created')
    raw_id_fields = ('user', 'reply', 'post')

