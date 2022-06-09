from django.contrib import admin
from . import models


@admin.register(models.LeadStage)
class LeadStageAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'stage_ordering')
    list_editable = ('stage_ordering', )
    ordering = ('-stage_ordering', )


class TaskInline(admin.StackedInline):
    model = models.Task


@admin.register(models.Lead)
class Lead(admin.ModelAdmin):
    inlines = (TaskInline, )


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LeadComment)
class LeadCommentAdmin(admin.ModelAdmin):
    pass