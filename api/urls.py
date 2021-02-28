from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='User')
router.register('users/me', views.UserViewSet, basename='me')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments'
)
router.register('titles', views.TitleViewSet)
router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenreViewSet)

urlpatterns = [
    # path('v1/users/me/', views.UserViewSet)  #DetailProfile.as_view()),
    path('v1/', include(router.urls))
]
