from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Exam, Question

# 1. Exam Model registration
# Isko normal rakhte hain taaki sirf Exams manage ho sakein
admin.site.register(Exam)

# 2. Question Model registration with Bulk Import/Export
# @admin.register(Question) decorator use karne se AlreadyRegistered error nahi aayega
@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    # Admin list view mein ye columns dikhenge
    list_display = ('id', 'question_text', 'exam', 'correct_option')
    
    # Sawaal search karne ke liye search bar (question text aur exam name par)
    search_fields = ('question_text', 'exam__title')
    
    # Side mein filter lagane ke liye
    list_filter = ('exam',)
    
    # Ek page par kitne questions dikhane hain
    list_per_page = 20