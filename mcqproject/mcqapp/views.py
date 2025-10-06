
import os
import pdfplumber
import docx
import google.generativeai as genai
from django.conf import settings
import time
from collections import defaultdict
from fpdf import FPDF
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import  UploadedFile, QuizResult,QuestionAttempt
from math import ceil
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.db.models import Avg
from django.shortcuts import render
from .models import QuizResult
from django.db.models import Avg
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User

from google.api_core import retry
# mcqapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from .models import  QuizResult ,UserProfile
# from .forms import QuizForm
import random
import string


from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User


from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import QuizResult
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import QuizResult



from django.contrib.auth import login


from .models import UserProfile


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile
import random
import string
from datetime import timedelta
from .models import EmailVerification


# Forgot Password
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import CustomUserCreationForm  # Import the custom form
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from smtplib import SMTPException
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages
from django.shortcuts import render, redirect


from django.template.loader import render_to_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags



from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
import random
import string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone
from .models import EmailVerification
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model





def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Create user without strict password rules
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        messages.success(request, "Registration successful!")
        return redirect("home")  

    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")  
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# Admin Dashboard

def profile(request):
    # Dummy data for now
    user_data = {
        'username': 'learner123',
        'email': 'learner@eduquest.com',
        'quizzes_taken': 24,
        'documents_summarized': 12,
    }
    return render(request, 'profile.html', user_data)

def home(request):
    return render(request, 'home.html')
# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 # Redirect to 'next' parameter if it exists, otherwise to home
#                 next_url = request.GET.get('next', 'home')
#                 return redirect(next_url)
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        login_identifier = request.POST.get('login')
        password = request.POST.get('password')
        
        User = get_user_model()
        
        try:
            # First try to get user by email
            user = User.objects.get(email=login_identifier)
            username = user.username
        except User.DoesNotExist:
            # If not found by email, try username
            username = login_identifier
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username/email or password')
            return redirect('user_login')
    
    return render(request, 'login.html')

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            
            # Generate verification code
            verification_code = get_random_string(length=6, allowed_chars='0123456789')
            expiration_time = timezone.now() + timedelta(minutes=10)
            
            # Save to EmailVerification model
            EmailVerification.objects.update_or_create(
                user=user,
                defaults={
                    'verification_code': verification_code,
                    'expiration_time': expiration_time
                }
            )
            
            # Prepare email context
            context = {
                'user_name': user.username,
                'verification_code': verification_code,
                'time': expiration_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Render HTML email
            subject = 'Password Reset Verification Code'
            html_message = render_to_string('email_password_reset.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            msg = EmailMultiAlternatives(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            
            # Store user email in session for verification
            request.session['reset_email'] = email
            return redirect('password_reset_verify')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address')
            return redirect('user_login')
    
    return redirect('user_login')

def password_reset_verify(request):
    if 'reset_email' not in request.session:
        return redirect('user_login')
    
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'password_reset_verify.html')
        
        # Validate password strength
        try:
            validate_password(new_password)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return render(request, 'password_reset_verify.html')
        
        try:
            user = User.objects.get(email=request.session['reset_email'])
            verification = EmailVerification.objects.get(
                user=user,
                verification_code=verification_code,
                expiration_time__gte=timezone.now()
            )
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            # Clean up
            verification.delete()
            del request.session['reset_email']
            
            # Send confirmation email
            context = {
                'user_name': user.username,
                'reset_time': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            subject = 'Password Reset Successful'
            html_message = render_to_string('email_password_reset_success.html', context)
            plain_message = strip_tags(html_message)
            
            msg = EmailMultiAlternatives(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            
            messages.success(request, 'Password reset successfully. Please login with your new password.')
            return redirect('user_login')
            
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            messages.error(request, 'Invalid or expired verification code')
    
    return render(request, 'password_reset_verify.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


# Configure Google API with key from settings
genai.configure(api_key=getattr(settings, "GOOGLE_API_KEY", ""))
model = genai.GenerativeModel("models/gemini-1.5-pro")

def allowed_file(filename):
    allowed_extensions = {'pdf', 'txt', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def extract_text_from_file(file_path):
    try:
        if not os.path.exists(file_path):  # Check if file exists
            print(f"Error: File does not exist at {file_path}")
            return None

        ext = file_path.rsplit('.', 1)[1].lower()
        if ext == 'pdf':
            with pdfplumber.open(file_path) as pdf:
                text = '\n'.join([page.extract_text() or '' for page in pdf.pages])
            return text.strip() if text else None
        elif ext == 'docx':
            doc = docx.Document(file_path)
            text = ' '.join([para.text for para in doc.paragraphs])
            return text.strip() if text else None
        elif ext == 'txt':
            with open(file_path, 'r', encoding="utf-8") as file:
                return file.read().strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def Question_mcqs_generator(input_text, num_questions, difficulty):
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
    Please generate {num_questions} MCQs at a {difficulty} difficulty level. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """
    response = model.generate_content(prompt).text.strip()
    print("Generated MCQs:", response)  # Debugging
    return response

#  prompt = f"""
#     You are an expert MCQ generator. Create {num_questions} multiple-choice questions based on the following text:
#     '{input_text}'
    
#     Difficulty level: {difficulty}
    
#     Requirements for each question:
#     1. Must have exactly 4 options (A, B, C, D)
#     2. Must include one clearly correct answer
#     3. For hard difficulty:
#        - Include nuanced options that require deeper understanding
#        - Avoid obvious wrong answers
#        - Make distinctions between options subtle but meaningful
#     4. Format strictly as follows:
    
#     ## MCQ
#     Question: [question text]
#     A) [option A]
#     B) [option B]
#     C) [option C]
#     D) [option D]
#     Correct Answer: [letter of correct option]
    
#     Example for hard difficulty:
#     ## MCQ
#     Question: Which factor most significantly influenced Microsoft's shift toward open-source collaboration?
#     A) Declining market share in enterprise software
#     B) Fundamental changes in software development paradigms
#     C) Pressure from regulatory bodies
#     D) Strategic recognition of mutual benefits with the open-source community
#     Correct Answer: D
#     """
def save_mcqs_to_file(mcqs, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for i, mcq in enumerate(mcqs.split("## MCQ")[1:]):
            lines = mcq.strip().split("\n")
            if len(lines) < 6:
                continue

            # Extract question and options
            question = lines[1].replace("Question: ", "").strip()
            options = [line.strip() for line in lines[2:6]]
            correct_answer = lines[6].replace("Correct Answer: ", "").strip()

            # Write question
            f.write(f"Question {i + 1}: {question}\n")

            # Write options
            for option in options:
                f.write(f"{option}\n")

            # Write correct answer
            f.write(f"Correct Answer: {correct_answer}\n\n")


def create_pdf(mcqs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    try:
        pdf.add_font('DejaVu', '', r"C:\\Users\\HP\\OneDrive\\Documents\\minproject (4)\\dejavu-sans-ttf-2.37\\ttf\\DejaVuSans.ttf", uni=True)
        pdf.set_font('DejaVu', '', 10)
    except Exception as e:
        print(f"Error loading font: {e}")
        return

    mcq_blocks = mcqs.split("## MCQ")[1:]

    for i, mcq in enumerate(mcq_blocks):
        lines = mcq.strip().split("\n")
        if len(lines) < 6:
            continue

        question = lines[1].replace("Question: ", "").strip()
        options = [line.strip() for line in lines[2:6]]
        correct_answer = lines[6].replace("Correct Answer: ", "").strip()

        # Handle large text with proper wrapping
        pdf.multi_cell(180, 10, f"Question {i + 1}: {question}")

        # Display options
        for option in options:
            pdf.multi_cell(180, 10, option)

        # Add correct answer
        pdf.multi_cell(180, 10, f"Correct Answer: {correct_answer}")
        pdf.ln(10)

    try:
        pdf.output(filename)
        print(f"PDF successfully created at {filename}")
    except Exception as e:
        print(f"Error saving PDF: {e}")


def parse_mcqs(mcqs):
    mcq_list = []
    mcq_blocks = mcqs.split("## MCQ")[1:]  # Split into individual MCQs
    for block in mcq_blocks:
        lines = block.strip().split("\n")
        if len(lines) < 6:  # Ensure there are enough lines for a complete MCQ
            continue

        # Extract the question
        question = lines[1].replace("Question: ", "").strip()

        # Extract options (A, B, C, D)
        options = [line.strip() for line in lines[2:6]]

        # Extract the correct answer
        correct_answer = lines[6].replace("Correct Answer: ", "").strip()

        # Store the parsed MCQ in the list
        mcq_list.append({
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        })

    return mcq_list


@login_required
def quiz_generation(request):
    # Clear any existing data when loading the page
    if 'mcqs' in request.session:
        del request.session['mcqs']
    if 'file_name' in request.session:
        del request.session['file_name']
    
    if request.method == 'POST':
        try:
            file = request.FILES['file']
        except KeyError:
            return render(request, 'quiz_generation.html', {'error': 'No file uploaded. Please upload a file.'})

        num_questions = int(request.POST['num_questions'])
        difficulty = request.POST['difficulty']
        action = request.POST['action']

        file_path = default_storage.save(file.name, file)
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        file_name = os.path.splitext(file.name)[0]
        request.session['file_name'] = file_name

        text = extract_text_from_file(full_file_path)
        if not text:
            return render(request, 'quiz_generation.html', {'error': 'Could not extract text from the file.'})

        mcqs = Question_mcqs_generator(text, num_questions, difficulty)
        mcq_list = parse_mcqs(mcqs)

        if action == "generate_mcqs":
            uploaded_file = UploadedFile(
                file=file_path,
                num_questions=num_questions,
                difficulty=difficulty,
                generated_mcqs=mcqs
            )
            uploaded_file.save()

            txt_filename = f"generated_mcqs_{uploaded_file.id}.txt"
            pdf_filename = f"generated_mcqs_{uploaded_file.id}.pdf"
            txt_full_path = os.path.join(settings.MEDIA_ROOT, txt_filename)
            pdf_full_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
            save_mcqs_to_file(mcqs, txt_full_path)
            create_pdf(mcqs, pdf_full_path)

            response = render(request, 'result.html', {
                'mcqs': mcq_list,
                'txt_filename': os.path.join(settings.MEDIA_URL, txt_filename),
                'pdf_filename': os.path.join(settings.MEDIA_URL, pdf_filename)
            })
            
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        elif action == "start_quiz":
            request.session['mcqs'] = mcq_list
            return redirect('quiz')

    response = render(request, 'quiz_generation.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response



def start_new_chat(request):
    if request.method == 'POST':
        # Clear the session data
        if 'pdf_text' in request.session:
            del request.session['pdf_text']
        if 'file_name' in request.session:
            del request.session['file_name']
    return redirect('summarization')

def summarization(request):
    if request.method == 'POST':
        try:
            # Get the uploaded PDF file
            file = request.FILES['pdf_file']
        except KeyError:
            return render(request, 'summarization.html', {'error': 'No file uploaded. Please upload a PDF file.'})
        
        # Save the uploaded file
        file_path = default_storage.save(file.name, file)
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        print("File saved at:", full_file_path)  # Debugging
        
        # Extract text from the PDF
        text = extract_text_from_pdf(full_file_path)
        if not text:
            return render(request, 'summarization.html', {'error': 'Could not extract text from the PDF.'})
        
        # Store the extracted text in the session
        request.session['pdf_text'] = text
        return render(request, 'summarization.html', {'text': text})
    
    return render(request, 'summarization.html')





def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = '\n'.join([page.extract_text() or '' for page in pdf.pages])
        return text.strip() if text else None
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def ask_question(request):
    if request.method == 'POST':
        # Get the question from the form
        question = request.POST.get('question', '').strip()
        if not question:
            return render(request, 'summarization.html', {'error': 'Please enter a question.'})
        
        # Get the extracted text from the session
        text = request.session.get('pdf_text')
        if not text:
            return render(request, 'summarization.html', {'error': 'No PDF text found. Please upload a PDF first.'})
        
        # Generate a response using the language model
        prompt = f"""
        You are an AI assistant helping the user answer questions based on the following text:
        '{text}'
        Question: {question}
        Answer:
        """
        response = model.generate_content(prompt).text.strip()
        
        return render(request, 'summarization.html', {
            'text': text,
            'question': question,
            'response': response,
        })
    
    return redirect('summarization')




@login_required
def user_logout(request):
    logout(request)
    return redirect('home')







