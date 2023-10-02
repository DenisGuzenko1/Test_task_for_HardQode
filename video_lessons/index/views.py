from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, LessonView, Lesson
from .serializers import LessonViewSerializer, ProductStatisticsSerializer


def index(request):
    products = Product.objects.all()
    lessons = Lesson.objects.all()
    lessons_view = LessonView.objects.all()
    context = {
        'products': products,
        'lessons': lessons,
        'lessons_view': lessons_view
    }
    return render(request, 'index.html', context)


class AllLessonViewSET(viewsets.ModelViewSet):
    serializer_class = LessonViewSerializer
    queryset = LessonView.objects.all()


class UserLessons(APIView):
    def get(self, request, user_id):
        user_lessons = LessonView.objects.filter(user=user_id)

        serializer = LessonViewSerializer(user_lessons, many=True)
        return Response(serializer.data)


class ProductLessons(APIView):
    def get(self, request, user_id, product_id):
        try:
            product = Product.objects.get(id=product_id, owner=user_id)

            lessons = product.lesson_set.all()

            lesson_views = LessonView.objects.filter(user=user_id, lesson__in=lessons)

            serializer = LessonViewSerializer(lesson_views, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"message": "У вас нет доступа к этому продукту"}, status=403)


class ProductStatistics(APIView):
    def get(self, request):
        products = Product.objects.all()

        statistics = []
        for product in products:
            product_stats = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'lessons_viewed_count': LessonView.objects.filter(lesson__products=product).count(),
                'total_time_watched': LessonView.objects.filter(lesson__products=product).aggregate(
                    total_time=Coalesce(Sum('view_time_seconds'), 0))['total_time'],
                'students_count': LessonView.objects.filter(lesson__products=product).values('user').distinct().count(),
                'acquisition_percentage': (LessonView.objects.filter(lesson__products=product).values(
                    'user').distinct().count() / User.objects.count()) * 100
            }
            statistics.append(product_stats)

        serializer = ProductStatisticsSerializer(statistics, many=True)
        return Response(serializer.data)
