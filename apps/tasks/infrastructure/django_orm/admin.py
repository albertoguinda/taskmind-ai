"""
Django Admin configuration for Task.

Provides admin interface for managing tasks.
"""

from django.contrib import admin
from .models import TaskModel


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for Task management.
    
    Provides filtering, searching, and bulk actions.
    """
    
    # List display
    list_display = (
        'title',
        'priority',
        'status',
        'urgency_score',
        'created_at',
        'updated_at',
    )
    
    # Filters
    list_filter = (
        'priority',
        'status',
        'created_at',
    )
    
    # Search
    search_fields = (
        'title',
        'description',
        'ai_keywords',
    )
    
    # Ordering
    ordering = ('-urgency_score', '-created_at')
    
    # Read-only fields
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'urgency_score',
        'ai_keywords',
    )
    
    # Fieldsets for organization
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description'),
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority'),
        }),
        ('AI Analysis', {
            'fields': ('urgency_score', 'ai_keywords'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions
    actions = ['mark_as_high_priority', 'mark_as_done']
    
    def mark_as_high_priority(self, request, queryset):
        """Bulk action: Mark tasks as HIGH priority."""
        updated = queryset.update(priority='HIGH')
        self.message_user(request, f'{updated} tasks marked as HIGH priority')
    mark_as_high_priority.short_description = 'Mark selected as HIGH priority'
    
    def mark_as_done(self, request, queryset):
        """Bulk action: Mark tasks as DONE."""
        updated = queryset.update(status='DONE')
        self.message_user(request, f'{updated} tasks marked as DONE')
    mark_as_done.short_description = 'Mark selected as DONE'