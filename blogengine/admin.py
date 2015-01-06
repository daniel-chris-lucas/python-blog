import blogengine.models
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", ), }

admin.site.register(blogengine.models.Post, PostAdmin)
