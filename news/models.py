from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

# Maximum number of characters that will be displayed as news content on the main page.
SHORT_CONTENT_CHARACTERS = 400

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    content_short = models.CharField(blank=True, max_length=SHORT_CONTENT_CHARACTERS + 3)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    # If length of the full content is greater than SHORT_CONTENT's value, this will be set to True.
    display_full_content = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if len(self.content) > SHORT_CONTENT_CHARACTERS:
            self.display_full_content = True
            self.content_short = self.content[:SHORT_CONTENT_CHARACTERS] + "..."
        else:
            self.content_short = self.content

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


    class Meta:
        ordering = ["-date"]
