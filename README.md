# QuizElite

A Django-based quiz application for creating, managing, and taking exams.
# live demo link - https://quiz-elite-ndttadf53-rishabhs-projects-1b507e30.vercel.app/ 
## Features

- User authentication (login/signup)
- Admin dashboard for managing exams and questions
- Student interface for taking quizzes
- Results tracking and display
- Responsive web interface

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd exam
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Open your browser and go to `http://127.0.0.1:8000/`

## Usage

- Access the admin dashboard at `/admin/` to manage exams and questions.
- Students can register/login and take quizzes.
- View results after completing exams.

## Requirements

- Python 3.8+
- Django 4.0+
- Other dependencies listed in `requirements.txt`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
