from django.db import models
import django
from django.utils.text import slugify

# Create your models here.
# shorted link in DB
class Link(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)

    def click(self):
        self.clicks += 1
        self.save()

    def __str__(self) -> str:
        return f"{self.name} | {self.url}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
