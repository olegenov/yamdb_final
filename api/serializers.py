from api.models import ConfirmationCode, CustomUser
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Title, Review, Comment, Category, Genre


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'last_name', 'username', 'bio', 'email',
                  'role']
        model = CustomUser


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = ConfirmationCode

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError({
                'username': "You can't take this username"
            })


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.ReadOnlyField()

    class Meta:
        fields = ('id', 'text', 'score', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            review = Review.objects.filter(
                author=self.context['request'].user,
                title_id=self.context['view'].kwargs['title_id'])
            if review.exists():
                raise serializers.ValidationError('One author for one title')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    pub_date = serializers.ReadOnlyField()

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', )
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genre


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        allow_null=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        allow_null=True,
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title
