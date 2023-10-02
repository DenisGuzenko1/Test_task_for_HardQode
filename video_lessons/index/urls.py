from django.urls import path, include
from rest_framework import routers

from . import views
from .views import *

router = routers.SimpleRouter()
router.register('lessons', AllLessonViewSET)

urlpatterns = [
    path('', views.index, name='index'),  # главная страница, где отображаются все уроки, продукты и просмотр уроков
    path('user_lessons/<int:user_id>/', UserLessons.as_view(), name='user-lessons'),
    # API который отображает уроки конкретного пользователя
    path('product_lessons/<int:user_id>/<int:product_id>/', ProductLessons.as_view(), name='product-lessons'),
    # API который отображает список уроков по конкретному продукту
    path('product_statistics/', ProductStatistics.as_view(), name='product-statistics'),
    # API который отображает статистику
    path('', include(router.urls))  # API который отображает все существующие уроки
]
