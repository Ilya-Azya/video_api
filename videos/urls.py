from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    VideoViewSet,
    VideoIDsView,
    VideoStatisticsSubqueryView,
    VideoStatisticsGroupByView
)

router = DefaultRouter()
router.register('videos', VideoViewSet, basename='video')

urlpatterns = [
    path('', include(router.urls)),
    path('videos/ids/', VideoIDsView.as_view()),
    path('videos/statistics-subquery/', VideoStatisticsSubqueryView.as_view()),
    path('videos/statistics-group-by/', VideoStatisticsGroupByView.as_view()),
]
