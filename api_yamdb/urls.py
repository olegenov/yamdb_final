from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from api import views
from api.views import ConfirmationCodeViewSet

router = DefaultRouter()
router.register('email', ConfirmationCodeViewSet, basename='Token')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
    path('auth/token/', views.get_token, name='Token'),
    path('auth/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
