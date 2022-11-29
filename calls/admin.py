from django.contrib import admin

from .models import AppliedSolution, Called, ImpressoraDeth, Priority, Sector


@admin.register(Called)
class CalledAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_resolved', 'author']
    list_display_links = ['title', 'created_at']
    search_fields = ['id', 'title', 'description']
    list_filter = ['category', 'author', 'is_resolved']
    list_per_page = 10
    list_editable = ['is_resolved']
    ordering: '-id'
    prepopulated_fields = {
        "slug": ('title',)
    }


admin.site.register(Sector)
admin.site.register(Priority)
admin.site.register(AppliedSolution)
admin.site.register(ImpressoraDeth)
