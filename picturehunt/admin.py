from django.contrib import admin

# Register your models here.
from picturehunt.models import User, Team, Segment, Clue, CompletedClue, SegmentOrder, Path


class UserAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    pass


class SegmentAdmin(admin.ModelAdmin):
    pass


class ClueAdmin(admin.ModelAdmin):
    exclude = ('img_content',)


class CompletedClueAdmin(admin.ModelAdmin):
    pass


class SegmentOrderAdmin(admin.ModelAdmin):
    pass


class PathAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(Clue, ClueAdmin)
admin.site.register(CompletedClue, CompletedClueAdmin)
admin.site.register(SegmentOrder, SegmentOrderAdmin)
admin.site.register(Path, PathAdmin)
