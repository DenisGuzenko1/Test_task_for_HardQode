from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Product, Lesson, LessonView


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class LessonViewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    lesson = LessonSerializer()
    last_viewed_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = LessonView
        fields = '__all__'


class ProductStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'lessons_viewed_count', 'total_time_watched', 'students_count',
                  'acquisition_percentage')

    lessons_viewed_count = serializers.IntegerField()
    total_time_watched = serializers.IntegerField()
    students_count = serializers.IntegerField()
    acquisition_percentage = serializers.FloatField()
