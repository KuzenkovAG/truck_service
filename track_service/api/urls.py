from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'loads', views.LoadViewSet, basename='Load')

urlpatterns = [
    path('v1/trucks/<int:pk>/', views.TruckUpdateView.as_view()),
    path('v1/', include(router.urls)),
]
