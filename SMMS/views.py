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
from django.views.decorators.csrf import csrf_protect
# from phonepe.sdk.pg.payments.v2.standard_checkout_client import StandardCheckoutClient
# from phonepe.sdk.pg.env import Env
from uuid import uuid4
# from phonepe.sdk.pg.payments.v2.models.request.standard_checkout_pay_request import StandardCheckoutPayRequest

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

def assessment_view(request):
  #  assessments= Assessment.objects.create(user="krishna", quizzes=80, assignments=75, exams=90, overall=85)
    assessments = Assessment.objects.all()

    # Fetch all assessments from MySQL

    print(assessments)
    print("USING DATABASE:", settings.DATABASES['default'])
    return render(request, 'assessment.html', {'assessments': assessments})

def admin_dashboard(request):
    student = Student.get_all_students()
    tickets = support_ticketx.get_all_tickets()
    classes = Class.get_all_classes()
    no = Student.studntno()
    return render(request, 'admin-dashboard.html',{'student': student,'tickets': tickets, 'classes': classes , 'no': no})

def admin_class_add(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        class_title = request.POST.get('class_title', '')
        program = request.POST.get('program', '')
        batch = request.POST.get('batch', '')
        description = request.POST.get('description', '')
        class_date = request.POST.get('class_date', '')
        start_hour = request.POST.get('start_hour', '')
        start_minute = request.POST.get('start_minute', '')
        end_hour = request.POST.get('end_hour', '')
        end_minute = request.POST.get('end_minute', '')
        duration = int(request.POST.get('duration', 0))
        trainer = request.POST.get('trainer', '')
        platform = request.POST.get('platform', '')
        meeting_link = request.POST.get('meeting_link', '')
        meeting_password = request.POST.get('meeting_password', '')
        prerequisites = request.POST.get('prerequisites', '')
        materials = request.POST.get('materials', '')
        notes = request.POST.get('notes', '')
        start_time = f"{start_hour}:{start_minute}"
        end_time = f"{end_hour}:{end_minute}"

        if not all([class_title, program, batch, class_date, start_hour, start_minute, end_hour, end_minute, trainer, platform]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'class_title': class_title,
                    'program': program,
                    'batch': batch,
                    'description': description,
                    'class_date': class_date,
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': duration,
                    'trainer': trainer,
                    'platform': platform,
                    'meeting_link': meeting_link,
                    'meeting_password': meeting_password,
                    'prerequisites': prerequisites,
                    'materials': materials,
                    'notes': notes,
                }
                result = Class.add_class(form_data)
                if result:
                    messages.success(request, 'Class scheduled successfully!')
                    return redirect('admin_class_add')
                else:
                    messages.error(request, 'Failed to schedule class. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error scheduling class: {str(e)}')
    classes = Class.get_all_classes()
    return render(request, 'admin-class-add.html', {'classes': classes})


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
    print("POST data:", request.POST)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        message = request.POST.get('message', '')
        audience = request.POST.get('audience', '')
        program = request.POST.get('program', '')
        batch = request.POST.get('batch', '')
        expiry_date = request.POST.get('expiryDate', '')
        is_important = request.POST.get('isImportant') == 'on'
        created_date = datetime.now().strftime('%Y-%m-%d')
        created_by = "Admin"  # You can get this from the logged-in user

        if not all([title, message, audience]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'title': title,
                    'message': message,
                    'audience': audience,
                    'program': program if audience == 'program' else '',
                    'batch': batch if audience == 'batch' else '',
                    'expiry_date': expiry_date,
                    'is_important': is_important,
                    'created_date': created_date,
                    'created_by': created_by
                }
                print("form_data:", form_data)
                result = announcementx.add_announcement(form_data)
                if result:
                    messages.success(request, 'Announcement published successfully!')
                    return redirect('announcements')
                else:
                    messages.error(request, 'Failed to publish announcement. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error publishing announcement: {str(e)}')
    announcements_list = announcementx.get_all_announcements()
    return render(request, 'admin-announcements.html', {'announcements': announcements_list})


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
    if request.method == 'POST':
        # Extract form data
        print("POST data:", request.POST)
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        dob = request.POST.get('dob', '')
        gender = request.POST.get('gender', '')
        profile_picture_file = request.FILES.get('profile_picture')
        address_line1 = request.POST.get('address_line1', '')
        address_line2 = request.POST.get('address_line2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        postal_code = request.POST.get('postal_code', '')
        country = request.POST.get('country', '')
        designation = request.POST.get('designation', '')
        experience_years = int(request.POST.get('experience_years', ''))
        teaching_experience = int(request.POST.get('teaching_experience', ''))
        expertise_areas = request.POST.getlist('expertise_areas[]')
        certifications_raw = request.POST.get('certifications', '')
        bio = request.POST.get('bio', '')
        programs = request.POST.getlist('programs')
        specific_modules_raw = request.POST.get('specific_modules', '')
        hourly_rate = float(request.POST.get('hourly_rate', ''))
        max_hours_weekly = int(request.POST.get('max_hours_weekly', 20))
        create_account = request.POST.get('create_account') == 'on'
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        linkedin_profile = request.POST.get('linkedin_profile', '')            
        website = request.POST.get('website', '')
        notes = request.POST.get('notes', '')
        # Validate required fields
        if not all([first_name, last_name, email, phone, designation, bio, username]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'dob': dob,
                    'gender': gender,
                    'address_line1': address_line1,
                    'address_line2': address_line2,
                    'city': city,
                    'state': state,
                    'postal_code': postal_code,
                    'country': country,
                    'designation': designation,
                    'experience_years': experience_years,
                    'teaching_experience': teaching_experience,
                    'expertise_areas': expertise_areas,
                    'certifications': certifications_raw,
                    'bio': bio,
                    'programs': programs,
                    'specific_modules': specific_modules_raw,
                    'hourly_rate': hourly_rate,
                    'max_hours_weekly': max_hours_weekly,
                    'create_account': create_account,
                    'username': username,
                    'password': password,
                    'linkedin_profile': linkedin_profile,
                    'website': website,
                    'notes': notes,
                }
                print("form_data:", form_data)
                result = Trainer.add_trainer(form_data)
                if result:
                    messages.success(request, 'Trainer registered successfully!')
                    return redirect('admin_trainers')
                else:
                    messages.error(request, 'Failed to register trainer. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error registering trainer: {str(e)}')
        trainers = Trainer.get_all_trainers()
    return render(request, 'admin-trainer-add.html', {'trainers': trainers})
    
def admin_program_add(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        title = request.POST.get('program_title', '')
        duration_months = int(request.POST.get('duration_months', 0))
        num_classes = int(request.POST.get('num_classes', 0))
        students_enrolled = int(request.POST.get('students_enrolled', 0))
        price = float(request.POST.get('program_price', 0))
        revenue = request.POST.get('revenue', '')
        rating = float(request.POST.get('rating', 0))
        completion_percentage = int(request.POST.get('completion_percentage', 0))
        description = request.POST.get('program_description', '')
        status = request.POST.get('program_status', '')
        is_featured = request.POST.get('is_featured','')

        if not all([title, duration_months, num_classes, price, rating, completion_percentage, description, status]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'title': title,
                    'duration_months': duration_months,
                    'num_classes': num_classes,
                    'students_enrolled': students_enrolled,
                    'price': price,
                    'revenue': revenue,
                    'rating': rating,
                    'completion_percentage': completion_percentage,
                    'description': description,
                    'status': status,
                    'is_featured': is_featured,
                }
                print("form_data:", form_data)
                result = Program.add_program(form_data)
                if result:
                    messages.success(request, 'Program added successfully!')
                    return redirect('admin_program_add')
                else:
                    messages.error(request, 'Failed to add program. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error adding program: {str(e)}')
    programs = Program.get_all_programs()
    return render(request, 'admin-program-add.html', {'programs': programs})

def support_ticket(request):
    if request.method=="POST":
        print("POST data:", request.POST)
        subject = request.POST.get('ticket_subject', '')
        priority = request.POST.get('ticket_priority', '')
        category = request.POST.get('ticket_category', '')
        message = request.POST.get('ticket_message', '')
        attachment= request.POST.get('ticket_attachment', '')

        # Basic validation
        if not all([subject, priority, category, message]):
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
                result = support_ticketx.add_support_ticket(form_data)
                # Redirect to the same page after submission
                if result:
                    messages.success(request, 'ticket raised successfully!')
                    return redirect('support_ticket')
                else:
                    messages.error(request, 'Failed to save data. Check server logs for details.')
            except Exception as e:
                messages.error(request,f'Error saving data: {str(e)}')

    # Fetch existing tickets to display
    tickets = support_ticketx.get_all_tickets()

    return render(request, 'support-ticket.html', {'tickets': tickets})

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
    if request.method == 'POST':
        print("POST data:", request.POST)
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        dob = request.POST.get('dob', '')
        gender = request.POST.get('gender', '')
        address_line1 = request.POST.get('address_line1', '')
        address_line2 = request.POST.get('address_line2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')   
        postal_code = request.POST.get('postal_code', '')
        country = request.POST.get('country', '')
        program = request.POST.get('program', '')
        batch = request.POST.get('batch', '')
        referral_source = request.POST.get('referral_source', '')
        notes = request.POST.get('notes', '')
        payment_status = request.POST.get('payment_status', '')
        payment_method = request.POST.get('payment_method', '')
        amount_paid = float(request.POST.get('amount_paid', 0.0))
        transaction_id = request.POST.get('transaction_id', '')
        payment_date = request.POST.get('payment_date', '')
        invoice_number = request.POST.get('invoice_number', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not all([first_name, last_name, email, phone , dob ,]):
            messages.error(request, 'All fields are required')
        else:
            try:
                form_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'dob': dob,
                    'gender': gender,
                    'address_line1': address_line1,
                    'address_line2': address_line2,
                    'city': city,
                    'state': state,
                    'postal_code': postal_code,
                    'country': country,
                    'program': program,
                    'batch': batch,
                    'referral_source': referral_source,
                    'notes': notes,
                    'payment_status': payment_status,
                    'payment_method': payment_method,
                    'amount_paid': amount_paid,
                    'transaction_id': transaction_id,
                    'payment_date': payment_date,
                    'invoice_number': invoice_number,
                    'username': username,
                    'password': password,
                    }
                print("form_data:", form_data)
                result = Student.add_student(form_data)
                client_id = "<SU2505161610519785728289>"
                client_secret = "<1716f4d2-d67d-4e4f-a0d6-7625965e92d3>"
                client_version = 1  # Insert your client version here
                env = Env.PRODUCTION  # Change to Env.PRODUCTION when you go live   
                client = StandardCheckoutClient.get_instance(client_id=client_id,
                                                              client_secret=client_secret,
                                                              client_version=client_version,
                                                              env=env)         
                unique_order_id = str(uuid4())
                print("Unique Order ID:", unique_order_id)
                ui_redirect_url = "https://www.google.com/"
                amount = 100
                standard_pay_request = StandardCheckoutPayRequest.build_request(merchant_order_id=unique_order_id,
                                                                                    amount=amount,
                                                                                    redirect_url=ui_redirect_url)
                standard_pay_response = client.pay(standard_pay_request)
                checkout_page_url = standard_pay_response.redirect_url
                print("Checkout Page URL:", checkout_page_url)
                if result:
                    messages.success(request, 'Student added successfully')
                    # Redirect to the same page after submission   
                    # Redirect to the checkout page
                    return redirect('admin_student_add')
                else:
                    messages.error(request, 'Failed to add student. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error adding student: {str(e)}')
    # Fetch existing students to display
    students = Student.get_all_students()
    programs = Program.get_all_programs()
    invno = invoicex.get_invno()
    return render(request, 'admin-student-add.html' , {'students': students,'programs': programs, 'invno': invno})

def admin_resources(request):
    return render(request, 'admin-resourses.html')    

def admin_batch(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        batch_code = request.POST.get('batchCode', '')
        batch_name = request.POST.get('batchName', '')
        program = request.POST.get('program', '')
        start_date = request.POST.get('startDate', '')
        end_date = request.POST.get('endDate', '')
        capacity = request.POST.get('capacity', '')
        status = request.POST.get('status', '')
        trainerassignment = request.POST.get('trainerAssignment', '')
        description = request.POST.get('description', '')

        if not all([batch_code, batch_name, program, start_date, end_date, capacity, status, trainerassignment, description]):
            messages.error(request, 'Batch name, start date, and end date are required.')
        else:
            try:
                form_data = {
                    'batch_code': batch_code,
                    'batch_name': batch_name,
                    'program': program,
                    'start_date': start_date,
                    'end_date': end_date,
                    'capacity': capacity,
                    'status': status,
                    'trainer': trainerassignment,
                    'description': description,
                }
                result = Batch.add_batch(form_data)
                if result:
                    messages.success(request, 'Batch added successfully!')
                    return redirect('admin_batch')
                else:
                    messages.error(request, 'Failed to add batch. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error adding batch: {str(e)}')
    batches = Batch.get_all_batches()
    return render(request, 'admin-batch-management-add-form.html', {'batches': batches})

def admin_class_recordings(request):
    return render(request, 'admin-class-recordings-add.html')


def commissions(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        transaction_id = request.POST.get('transactionId', '')
        partner = request.POST.get('partner', '')
        referred_student = request.POST.get('referredStudent', '')
        program = request.POST.get('program', '')
        amount = float(request.POST.get('amount', 0))
        processing_fee = float(request.POST.get('processingFee', 0))
        date = request.POST.get('date', '')
        status = request.POST.get('status', '')
        notes = request.POST.get('notes', '')

        if not all([partner, referred_student, program, amount, date, status]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'transaction_id': transaction_id,
                    'partner': partner,
                    'referred_student': referred_student,
                    'program': program,
                    'amount': amount,
                    'processing_fee': processing_fee,
                    'date': date,
                    'status': status,
                    'notes': notes
                }
                result = commissionx.add_commission(form_data)
                if result:
                    messages.success(request, 'Commission added successfully!')
                    return redirect('commissions')
                else:
                    messages.error(request, 'Failed to add commission. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error adding commission: {str(e)}')

    commissions_list = commissionx.get_all_commissions()
    comno = commissionx.get_comno()
    return render(request, 'admin-commissions-add.html', {'commissions': commissions_list , 'comno': comno})

def exams(request):
    return render(request, 'admin-exams-add.html')

def invoices(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        invoice_number = request.POST.get('invoiceNumber', '')
        student = request.POST.get('student', '')
        program = request.POST.get('program', '')
        batch = request.POST.get('batch', '')
        issue_date = request.POST.get('issueDate', '')
        due_date = request.POST.get('dueDate', '')
        amount = float(request.POST.get('amount', 0))
        status = request.POST.get('status', '')
        notes = request.POST.get('notes', '')

        if not all([student, program, batch, issue_date, due_date, amount, status]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'invoice_number': invoice_number,
                    'student': student,
                    'program': program,
                    'batch': batch,
                    'issue_date': issue_date,
                    'due_date': due_date,
                    'amount': amount,
                    'status': status,
                    'notes': notes
                }
                result = invoicex.add_invoice(form_data)
                if result:
                    messages.success(request, 'Invoice added successfully!')
                    return redirect('invoices')
                else:
                    messages.error(request, 'Failed to add invoice. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error adding invoice: {str(e)}')
    invoices = invoicex.get_all_invoices()
    invno = invoicex.get_invno()
    print("invno:", invno)
    return render(request, 'admin-invoices-add.html', {'invoices': invoices,'invno': invno})

def prog_cat(request):
    return render(request, 'admin-program-categories-add.html')

def refunds(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        refund_number = request.POST.get('refundNumber', '')
        student = request.POST.get('student', '')
        program = request.POST.get('program', '')
        enrollment_id = request.POST.get('enrollmentId', '')
        request_date = request.POST.get('requestDate', '')
        amount = float(request.POST.get('amount', 0))
        reason = request.POST.get('reason', '')
        status = request.POST.get('status', '')
        notes = request.POST.get('notes', '')

        if not all([student, program, enrollment_id, request_date, amount, reason, status]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'refund_number': refund_number,
                    'student': student,
                    'program': program,
                    'enrollment_id': enrollment_id,
                    'request_date': request_date,
                    'amount': amount,
                    'reason': reason,
                    'status': status,
                    'notes': notes
                }
                result = refundx.add_refund(form_data)
                if result:
                    messages.success(request, 'Refund request added successfully!')
                    return redirect('refunds')
                else:
                    messages.error(request, 'Failed to add refund request. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error adding refund request: {str(e)}')
    refunds_list = refundx.get_all_refunds()
    refno = refundx.get_refno()
    print("refno:", refno)
    return render(request, 'admin-refunds.html', {'refunds': refunds_list , 'refno': refno})

def results(request):
    return render(request, 'admin-results.html') 

def revenue(request):
    return render(request, 'admin-revenue-report.html')

def admin_trainer_schedule(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        program = request.POST.get('program', '')
        batch = request.POST.get('batch', '')
        topic = request.POST.get('topic', '')
        description = request.POST.get('description', '')
        class_date = request.POST.get('classDate', '')
        trainer = request.POST.get('trainer', '')
        start_time = request.POST.get('startTime', '')
        end_time = request.POST.get('endTime', '')
        meeting_link = request.POST.get('meetingLink', '')
        meeting_password = request.POST.get('meetingPassword', '')

        if not all([program, batch, topic, class_date, trainer, start_time, end_time]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'program': program,
                    'batch': batch,
                    'topic': topic,
                    'description': description,
                    'class_date': class_date,
                    'trainer': trainer,
                    'start_time': start_time,
                    'end_time': end_time,
                    'meeting_link': meeting_link,
                    'meeting_password': meeting_password,
                }
                result = TrainerSchedule.add_schedule(form_data)
                if result:
                    messages.success(request, 'Class scheduled successfully!')
                    return redirect('admin_trainer_schedule')
                else:
                    messages.error(request, 'Failed to schedule class. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error scheduling class: {str(e)}')
    schedules = TrainerSchedule.get_all_schedules()
    return render(request, 'admin-trainer-schedule-add.html', {'schedules': schedules})


def admin_user( request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        first_name = request.POST.get('firstName', '')
        last_name = request.POST.get('lastName', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        role = request.POST.get('role', '') 
        password = request.POST.get('password', '')
        status = request.POST.get('status', '')
        confirm_password = request.POST.get('confirmPassword', '')
        bio = request.POST.get('bio', '')

        if not all([first_name, last_name, email, phone, username, status,password,bio, role]):
            messages.error(request, 'Please fill in all required fields.')
        else:       
            try:
                form_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username':username,
                    'email': email,
                    'phone': phone,
                    'role': role,
                    'password': password,
                    'status': status,
                    'confirm_password': confirm_password,
                    'bio': bio
                }
                print("form_data:", form_data)
                result = User.add_user(form_data)
                if result:
                    messages.success(request, 'User added successfully!')
                    return redirect('admin_user')
                else:
                    messages.error(request, 'Failed to add user. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error adding user: {str(e)}')
                # users = User.get_all_users()
    return render(request, 'admin-user-management.html')

def admin_program_categories(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        category_name = request.POST.get('categoryName', '')
        description = request.POST.get('description', '')
        icon = request.POST.get('selectedIcon', '')
        if not all([category_name, description]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                form_data = {
                    'category_name': category_name,
                    'description': description,
                    'icon': icon,
                }
                print("form_data:", form_data)
                result = ProgramCategory.add_program_category(form_data)
                if result:
                    messages.success(request, 'Program category added successfully!')
                    return redirect('admin_program_categories')
                else:
                    messages.error(request, 'Failed to add program category. Check server logs.')
            except Exception as e:
                messages.error(request, f'Error adding program category: {str(e)}')
    return render(request, 'admin-program-categories-add.html')

def admin_exams(request):
    return render(request, 'admin-exams-add.html')

def admin_results(request):
    return render(request, 'admin-results.html')

def admin_trnx(request):
    return render(request, 'admin-trainer-add.html')