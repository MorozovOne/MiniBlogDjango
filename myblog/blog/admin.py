from django.contrib import admin
from .models import Post, Comments
from django_summernote.admin import SummernoteModelAdmin

#@admin.register(PostAdmin, Some)
class PostAdmin(SummernoteModelAdmin):
    #list_display = ('title', 'users')
    summernote_fields = ('description',)

#@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('users_comment', 'post_id')


admin.site.register(Post, PostAdmin)
admin.site.register(Comments)