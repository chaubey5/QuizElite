from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exam_quiz.urls')),  # Ye line check karo, empty quotes '' hone chahiye
]