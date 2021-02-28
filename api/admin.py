from django.contrib import admin

from .models import Category, ConfirmationCode, CustomUser, Genre, Title


class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'user', 'valid',)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'role', 'bio',)


class MembershipInline(admin.TabularInline):
    model = Title.genre.through


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'year') 
    search_fields = ('name',) 
    list_filter = ('category', 'genre', 'year') 
    empty_value_display = '-пусто-'
    inlines = [
        MembershipInline,
    ]
    exclude = ('genre',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug') 
    search_fields = ('name',)  
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug') 
    search_fields = ('name',) 
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(ConfirmationCode, ConfirmationCodeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
