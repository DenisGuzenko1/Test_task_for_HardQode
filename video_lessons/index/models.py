from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.name} {self.description} {self.price} {self.owner}"


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    duration_seconds = models.IntegerField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.title} {self.video_url} {self.duration_seconds}"


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time_seconds = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20,
                              choices=[('Просмотрено', 'Просмотрено'), ('Не просмотрено', 'Не просмотрено')])
    last_viewed_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.user} {self.lesson} {self.view_time_seconds} {self.status}"
