from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    exclude = ("content_short", "author", "date", "display_full_content")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set author during the first save.
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
