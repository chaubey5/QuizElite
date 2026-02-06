from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth_portal'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('auth/', views.auth_view, name='auth_portal'),
    
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/manage/', views.manage_exams, name='manage_exams'),
    path('dashboard/add-exam/', views.add_exam, name='add_exam'),
    path('dashboard/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('dashboard/add-question/<int:exam_id>/', views.add_question, name='add_question'),
    path('dashboard/results/', views.student_results, name='student_results'),

    path('quiz/<int:exam_id>/', views.quiz_view, name='quiz_page'),
    path('api/questions/<int:exam_id>/', views.get_questions, name='get_questions'),
    path('save-result/', views.save_result, name='save_result'),
    # urls.py mein ye line add karo
    path('result-page/<int:exam_id>/<int:score>/<int:total>/', views.result_page, name='result_page'),
    path('dashboard/edit-exam/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('edit-exam/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('manage-questions/<int:exam_id>/', views.manage_questions, name='manage_questions'),
    path('edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('exam/<int:exam_id>/import/', views.upload_questions_csv, name='upload_questions_csv'),
    

]
