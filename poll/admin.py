from django.contrib import admin
from .models import Category, Document, Comment


@admin.register(Category)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Document)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    readonly_fields = ('total_vote',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'document', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('user', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)