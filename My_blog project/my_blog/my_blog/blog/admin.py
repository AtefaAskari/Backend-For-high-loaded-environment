from django.contrib import admin
from .models import Post

# Custom admin class for the Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Display title, author, and created_at in the list view
    search_fields = ('title',)  # Add search functionality to search by title

# Register the Post model with the custom admin class
admin.site.register(Post, PostAdmin)
