from unicodedata import category
from django.contrib.auth.decorators import login_required
from .models import Assessment
import MySQLdb
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from datetime import datetime
import json
from django.http import JsonResponse


def personal_info_view(request):
    print(f"Method: {request.method}")
    if request.method == 'POST':
        print("POST data:", request.POST)
        # Get form data directly from POST request
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        dob = request.POST.get('dob', '')
        gender = request.POST.get('gender', '')
        # Basic validation
        if not all([first_name, last_name, email, phone, dob, gender]):
            messages.error(request, 'All fields are required')
        else:
            try:
                # Convert date string to proper format for MySQL
                try:
                    # Parse date (assuming input format is YYYY-MM-DD from HTML5 date input)
                    dob_date = datetime.strptime(dob, '%Y-%m-%d').strftime('%Y-%m-%d')
                except ValueError:
                    messages.error(request, 'Invalid date format')
                    return render(request, 'studentfrom.html')
                # Prepare data dictionary
                form_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'dob': dob_date,
                    'gender': gender
                }
                # Use the model's class method to save to MySQL
                result = PersonalInformation.save_to_mysql(form_data)
                if result:
                    messages.success(request, 'Personal information saved successfully!')
                    return redirect('studentfrom.html')
                else:
                    messages.error(request, 'Failed to save data. Check server logs for details.')
               # Redirect to the same page after submission
            except Exception as e:
                messages.error(request, f'Error saving data: {str(e)}')
    # For GET requests, get existing records to display
    try:
        personal_infos = PersonalInformation.get_all()
    except:
        personal_infos = []

    # Render the form and show existing records
    return render(request, 'admin-students.html', {'personal_infos': personal_infos})

def assessment_list_view(request):
    # Get assessments using the class method
    assessments = Assessment.get_assessments()

    # Pass the assessments to the template
    context = {
        'assessments': assessments
    }

    return render(request, 'assessment.html', {'assessments': assessments})

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def programs(request):
    return render(request, 'programs.html')

def success_stories(request):
    return render(request, 'success-stories.html')

def studentdtls(request):
    try:
        # Use custom method since we're not using Django ORM
        personal_infos = PersonalInformation.get_all()
    except Exception as e:
        print(f"Error fetching records: {str(e)}")  # Log the actual error
        personal_infos = []
    return render(request, 'admin-students.html', {'personal_infos': personal_infos})

def assessment(request):
    return render(request, 'assessment.html')
def studentfrom(request):
    return render(request, 'studentfrom.html')

def login_view(request):
    return render(request, 'login.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def refund(request):
    return render(request, 'refund.html')

def assessment_view(request):
  #  assessments= Assessment.objects.create(user="krishna", quizzes=80, assignments=75, exams=90, overall=85)
    assessments = Assessment.objects.all()

    # Fetch all assessments from MySQL

    print(assessments)
    print("USING DATABASE:", settings.DATABASES['default'])
    return render(request, 'assessment.html', {'assessments': assessments})

def admin_dashboard(request):
    return render(request, 'admin-dashboard.html')

def admin_class_add(request):
    return render(request, 'admin-class-add.html')

def admin_classes(request):
    return render(request, 'admin-classes.html')

def admin_program(request):
    return render(request, 'admin-programs.html')

def admin_trainers(request):
    return render(request, 'admin-trainers.html')

def amp_enrollment(request):
    return render(request, 'amp-enrollment.html')

def contactfrom(request):
    return render(request, 'contactfrom.html')

def coursefeedback(request):
    return render(request, 'coursefeedback.html')

def library(request):
    return render(request, 'library.html')

def my_programs(request):
    return render(request, 'my-programs.html')

def partner_registeration(request):
    return render(request, 'partner-registration.html')

def refer_earn(request):
    return render(request, 'refer-earn.html')

def student_form(request):
    return render(request, 'studentfrom.html')

def reg(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        # Get form data directly from POST request
        topic = request.POST.get('description', '')
        meeting_link = request.POST.get('meeting_link', '')
        # Basic validation
        if not all([ topic, meeting_link]):
            messages.error(request, 'All fields are required')
        else:
            try:
                # Convert date string to proper format for MySQL

                # Prepare data dictionary
                form_data = {
                    'topic': topic,
                    'meeting_link': meeting_link,
                }
                # Use the model's class method to save to MySQL
                result = reg.add_student_class(form_data)
                if result:
                    messages.success(request, 'classes scheduled successfully!')
                    return redirect('studentfrom.html')
                else:
                    messages.error(request, 'Failed to save data. Check server logs for details.')
               # Redirect to the same page after submission
            except Exception as e:
                messages.error(request, f'Error saving data: {str(e)}')
    # For GET requests, get existing records to display
    try:
        personal_infos = PersonalInformation.get_all()
    except:
        personal_infos = []
    return render(request, 'reg.html')

def admin_announcements(request):
    return render(request, 'admin-announcements.html')

def success_stories(request):
    return render(request, 'success-stories.html')

def admin_quiz(request):
    return render(request,'admin-quizzes.html')

def add_quiz(request):
    if request.method == 'POST':
       # print("POST data:", request.POST)
       questions_json_raw = request.POST.get('questions_json', '')

       try:
           questions_data = json.loads(questions_json_raw)
           for idx, question in enumerate(questions_data, start=1):

               print(f"Question {idx}: {question.get('question_text', 'No Question Text Provided')}")

               options = question.get('options', [])
               for opt_idx, option in enumerate(options, start=1):
                   option_text = option.get('option_text', 'No Option Text')
                   is_correct = option.get('is_correct', False)
                   print(f"  Option {opt_idx}: {option_text} (Correct: {is_correct})")

               print("-" * 50)
       except json.JSONDecodeError:
           messages.error(request, 'Invalid questions data format!')
         #  return render(request, 'your_template.html')  # or wherever your form is

      # print("QUESTIONS DATA:", questions_data)


        # Get form data directly from POST request
        # first_name = request.POST.get('first_name', '')
        # last_name = request.POST.get('last_name', '')
        # email = request.POST.get('email', '')
        # phone = request.POST.get('phone', '')
        # dob = request.POST.get('dob', '')
        # gender = request.POST.get('gender', '')
        # Basic validation
        # if not all([first_name, last_name, email, phone, dob, gender]):
        #     messages.error(request, 'All fields are required')
        # else:
        #     try:
        #         # Convert date string to proper format for MySQL
        #         try:
        #             # Parse date (assuming input format is YYYY-MM-DD from HTML5 date input)
        #             dob_date = datetime.strptime(dob, '%Y-%m-%d').strftime('%Y-%m-%d')
        #         except ValueError:
        #             messages.error(request, 'Invalid date format')
        #             return render(request, 'studentfrom.html')
        #         # Prepare data dictionary
        #         form_data = {
        #             'first_name': first_name,
        #             'last_name': last_name,
        #             'email': email,
        #             'phone': phone,
        #             'dob': dob_date,
        #             'gender': gender
        #         }
        #         # Use the model's class method to save to MySQL
        #         result = PersonalInformation.save_to_mysql(form_data)
        #         if result:
        #             messages.success(request, 'Personal information saved successfully!')
        #             return redirect('studentfrom.html')
        #         else:
        #             messages.error(request, 'Failed to save data. Check server logs for details.')
        #        # Redirect to the same page after submission
        #     except Exception as e:
        #         messages.error(request, f'Error saving data: {str(e)}')
    # For GET requests, get existing records to display
    try:
        personal_infos = []
    except:
        personal_infos = []
    # Render the form and show existing records
    return render(request, 'admin-quizzes.html', {'personal_infos': personal_infos})

def admin_trainer_add(request):
    return render(request, 'admin-trainer-add.html')

def admin_program_add(request):
    return render(request, 'admin-program-add.html')

def support_ticket(request):
    if request.method=="POST":
        print("POST data:", request.POST)
        subject = request.POST.get('ticket_subject', '')
        priority = request.POST.get('ticket_priority', '')
        category = request.POST.get('ticket_category', '')
        message = request.POST.get('ticket_message', '')
        attachment= request.POST.get('ticket_attachment', '')

        # Basic validation
        if not all([subject, priority, category, message, attachment]):
            messages.error(request, 'All fields are required')
        else:
            try:
                # Prepare data dictionary
                form_data = {
                    'ticket_subject': subject,
                    'ticket_priority': priority,
                    'ticket_category': category,
                    'ticket_message': message,
                    'ticket_attachment': attachment,
                }
                print("form_data:", form_data)
                # Use the model's class method to save to MySQL
                result = support_ticket.add_support_ticket(form_data)
                # Redirect to the same page after submission
                if result:
                    messages.success(request, 'ticket raised successfully!')
                    return redirect('support_ticket.html')
                else:
                    messages.error(request, 'Failed to save data. Check server logs for details.')
            except Exception as e:
                messages.error(request,f'Error saving data: {str(e)}')
    return render(request, 'support-ticket.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def admin_partners(request):
    return render(request, 'admin-partners.html')

def terms_and_condition(request):
    return render(request, 'terms-and-condition.html')

def blog(request):
    return render(request, 'blog.html')

def community(request):
    return render(request, 'community.html')

def admin_partners(request):
    return render(request, 'admin-partners.html')

def admin_payments (request):
    return render(request, 'admin-payments.html')

def admin_student_add(request):
    return render(request, 'admin-student-add.html')

def admin_resources(request):
    return render(request, 'admin-resourses.html')    

def admin_batch(request):
    return render(request, 'admin-batch-management-add-form.html')

def admin_class_recordings(request):
    return render(request, 'admin-class-recordings-add.html')

def commissions(request):
    return render(request, 'admin-commissions-add.html')

def exams(request):
    return render(request, 'admin-exams-add.html')

def invoices(request):
    return render(request, 'admin-invoices-add.html')

def prog_cat(request):
    return render(request, 'admin-program-categories-add.html')

def refunds(request):
    return render(request, 'admin-refunds.html')

def results(request):
    return render(request, 'admin-results.html') 

def revenue(request):
    return render(request, 'admin-revenue-report.html')

def admin_trainer_schedule(request):
    return render(request, 'admin-trainer-schedule-add.html')

def admin_user( request):
    return render(request, 'admin-user-management.html')

def admin_program_categories(request):
    return render(request, 'admin-program-categories-add.html')

def admin_exams(request):
    return render(request, 'admin-exams-add.html')

def admin_results(request):
    return render(request, 'admin-results.html')