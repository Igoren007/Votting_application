from django.contrib import admin
from poll_app.models import Poll, Person, Votes
from django.utils.safestring import mark_safe

# Register your models here.

@admin.register(Poll)
class  PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'max_vote', 'date_start', 'date_end')
    list_filter = ('title', 'is_active',)
    fields = ['title', 'persons', 'max_vote', ('date_start', 'date_end'), 'is_active',]

    def button(self, obj):
        return mark_safe(f'<a class="button" >Кнопка</a>')



@admin.register(Person)
class  PersonAdmin(admin.ModelAdmin):
    list_display = ('fio', 'age', 'bio')
    list_filter = ('fio',)
