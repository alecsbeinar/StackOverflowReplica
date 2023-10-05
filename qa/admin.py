from django.contrib import admin
from .models import Question, Answer

admin.site.register(Answer)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'added_at', 'rating', 'author')
    fields = ('title', 'author', 'text', 'added_at', ('rating', 'likes'))
    readonly_fields = ('added_at',)
    search_fields = ('title',)
    ordering = ('added_at', )


class AnswerAdmin(admin.TabularInline):
    model = Answer
    fields = ('text', 'added_at')
    readonly_fields = ('added_at', )
    extra = 1
