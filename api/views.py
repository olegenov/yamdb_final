from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import (Category, Comment, ConfirmationCode, CustomUser, Genre,
                     Review, Title)
from .permissions import (IsAdmin, IsAdminWithSafe, IsModerator,
                          IsOwnerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmationCodeSerializer, CustomUserSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializerRead, TitleSerializerWrite)


User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    search_fields = ['username', ]
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes = [IsAuthenticated],
        url_name='me',
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, id=request.user.id)
        if request.method == 'GET':
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
class DetailProfile(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(id=user.id)

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        obj = get_object_or_404(queryset, id=user.id)
        self.check_object_permissions(self.request, obj)
        return obj
'''


class ConfirmationCodeViewSet(ModelViewSet):
    http_method_names = 'post'
    serializer_class = ConfirmationCodeSerializer
    queryset = ConfirmationCode.objects.all()
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        if CustomUser.objects.filter(
                username=serializer.validated_data['email'].split('@')[0]
        ).exists():
            raise serializers.ValidationError({'errors': 'Email already used'})
        user = CustomUser.objects.create(
            username=serializer.validated_data['email'].split('@')[0]
        )
        serializer.save(user=user)


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def get_token(request):
    code = get_object_or_404(
        ConfirmationCode,
        email=request.POST['email'],
        code=request.POST['confirmation_code']
    )
    if code.valid is False:
        return Response({'error': 'Confirmation code already used'})
    code.valid = False
    code.save()
    refresh = RefreshToken.for_user(code.user)
    response = {
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }
    return Response(response)


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'post']
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = Review.objects.filter(title_id=title.pk)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return serializer.save(
            author=self.request.user,
            title_id=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(
            Review,
            title_id=title,
            id=self.kwargs['review_id']
        )
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(
            Review,
            title_id=title,
            id=self.kwargs['review_id']
        )
        return serializer.save(
            author=self.request.user,
            review_id=review.pk)


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminWithSafe, ]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerRead
        return TitleSerializerWrite


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminWithSafe,)
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsAdminWithSafe,)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
