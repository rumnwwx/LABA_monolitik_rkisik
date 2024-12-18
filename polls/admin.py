from django.contrib import admin
from .models import Question, Choice, User


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'is_active')
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'avatar' )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'avatar')


admin.site.register(User, UserAdmin)