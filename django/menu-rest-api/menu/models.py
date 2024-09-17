from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.name} | {self.price}"
