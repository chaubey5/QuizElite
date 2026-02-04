from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User 
from .models import Exam, Question, Result
import json
from django.contrib import messages
import csv

# --- Authentication (Login + Register) ---
def auth_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    login_form = AuthenticationForm()
    signup_form = UserCreationForm()
    
    if request.method == 'POST':
        if 'signup_submit' in request.POST:
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('index')
        
        elif 'login_submit' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('admin_dashboard' if user.is_staff else 'index')
                
    return render(request, 'auth.html', {'login_form': login_form, 'signup_form': signup_form})

# --- Admin Dashboard & Sections ---

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    context = {
        'total_exams': Exam.objects.count(),
        'total_students': User.objects.filter(is_staff=False).count(),
        'results_count': Result.objects.count(), # Kitne exams attempt hue
        'recent_results': Result.objects.all().order_by('-date_attempted')[:5], # Sirf top 5 results
        'active_tab': 'dashboard'
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def manage_exams(request):
    exams = Exam.objects.all()
    return render(request, 'manage_exams.html', {'exams': exams, 'active_tab': 'manage'})

@user_passes_test(lambda u: u.is_staff)
def student_results(request):
    # Ab yahan actual results dikhenge ordering ke saath
    results = Result.objects.all().order_by('-date_attempted')
    return render(request, 'student_results.html', {'results': results, 'active_tab': 'results'})

# --- CRUD Operations (Add/Delete) ---

@user_passes_test(lambda u: u.is_staff)
def add_exam(request):
    if request.method == "POST":
        Exam.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            total_marks=request.POST.get('marks')
        )
        return redirect('manage_exams')
    return render(request, 'add_exam.html')

@user_passes_test(lambda u: u.is_staff)
def delete_exam(request, exam_id):
    get_object_or_404(Exam, id=exam_id).delete()
    return redirect('manage_exams')

@user_passes_test(lambda u: u.is_staff)
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == "POST":
        Question.objects.create(
            exam=exam,
            question_text=request.POST.get('q_text'),
            option1=request.POST.get('opt1'),
            option2=request.POST.get('opt2'),
            option3=request.POST.get('opt3'),
            option4=request.POST.get('opt4'),
            correct_option=int(request.POST.get('correct'))
        )
        return redirect('add_question', exam_id=exam.id) 
    return render(request, 'add_question.html', {'exam': exam})

# --- Student & API Views ---

def index(request):
    exams = Exam.objects.all()
    # Hum chahein toh student ke pichle results bhi yahan se bhej sakte hain
    return render(request, 'index.html', {'exams': exams})

@login_required
def quiz_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, 'quiz.html', {'exam': exam})

# Quiz ke questions fetch karne ke liye API
def get_questions(request, exam_id):
    questions = list(Question.objects.filter(exam_id=exam_id).values(
        'id', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option'
    ))
    return JsonResponse(questions, safe=False)

# Result save karne ke liye AJAX view
@login_required
def save_result(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Result.objects.create(
            user=request.user,
            exam_id=data['exam_id'],
            score=data['score'],
            total_questions=data['total_questions']
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
# views.py mein ye function add karo
def result_page(request, exam_id, score, total):
    exam = get_object_or_404(Exam, id=exam_id)
    context = {
        'exam_title': exam.title,
        'score': score,
        'total': total,
    }
    return render(request, 'result_page.html', context)



@user_passes_test(lambda u: u.is_staff)
def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == "POST":
        exam.title = request.POST.get('title')
        exam.description = request.POST.get('description')
        exam.total_marks = request.POST.get('marks')
        exam.save()
        return redirect('manage_exams')
    return render(request, 'edit_exam.html', {'exam': exam})


# Views.py mein ye add karo
@user_passes_test(lambda u: u.is_staff)
def manage_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)
    return render(request, 'manage_questions.html', {'exam': exam, 'questions': questions})


@user_passes_test(lambda u: u.is_staff)
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    exam_id = question.exam.id # Wapas jane ke liye exam id save kar li
    
    if request.method == "POST":
        question.question_text = request.POST.get('question_text')
        question.option1 = request.POST.get('option1')
        question.option2 = request.POST.get('option2')
        question.option3 = request.POST.get('option3')
        question.option4 = request.POST.get('option4')
        question.correct_option = request.POST.get('correct_option')
        question.save()
        return redirect('manage_questions', exam_id=exam_id)
        
    return render(request, 'edit_question.html', {'question': question})



def upload_questions_csv(request, exam_id):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            exam = Exam.objects.get(id=exam_id)
            csv_file = request.FILES['csv_file']
            
            # UTF-8-SIG use karne se Excel ke hidden characters (BOM) hat jaate hain
            decoded_file = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file)
            
            # Ek baar check kar lo ki headers sahi aa rahe hain ya nahi
            # print(reader.fieldnames) 

            for row in reader:
                # .strip() use karne se extra spaces hat jayengi
                Question.objects.create(
                    exam=exam,
                    question_text=row.get('question_text', '').strip(),
                    option1=row.get('option1', '').strip(),
                    option2=row.get('option2', '').strip(),
                    option3=row.get('option3', '').strip(),
                    option4=row.get('option4', '').strip(),
                    correct_option=row.get('correct_option', '1').strip()
                )
            messages.success(request, "Bhai, saare sawaal load ho gaye!")
        except Exception as e:
            messages.error(request, f"Lafda: {e}")
            
    return redirect('manage_questions', exam_id=exam_id)