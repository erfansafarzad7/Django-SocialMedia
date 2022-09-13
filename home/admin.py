from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'created', 'updated')
    search_fields = ('slug', 'body')
    list_filter = ('created', 'updated')
    prepopulated_fields = {'slug': ('body',)}

# admin.site.register(Post, PostAdmin)
