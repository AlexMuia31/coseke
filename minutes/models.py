from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Minutes(models.Model):
    title = models.CharField(max_length=256)
    content = RichTextField()
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:150]
