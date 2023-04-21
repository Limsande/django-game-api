from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=200)
    studio = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.title} by {self.studio}'
