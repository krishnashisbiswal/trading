"""
URL configuration for SMMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from SMMS import views
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('success_stories/', views.success_stories, name='success_stories'),
    path('assmnt/', views.assessment, name='assent'),
    path('login/', views.login_view, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('terms/', views.terms, name='terms'),
    # path('privacy/', views.privacy, name='privacy'),
    # path('refund/', views.refund, name='refund'),
    path('student_dtails/', views.studentdtls, name='studentdtls'),
    path('assessment/', assessment_list_view, name='assessment'),
    path('registration/', views.personal_info_view, name='personal_info_view'),
    path('student_reg/', studentfrom, name='studentfrom'),
    path("admin_partners/", views.admin_partners, name="admin_partners"),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_class_add/', views.admin_class_add, name='admin_class_add'),
    path('admin_classes/', views.admin_classes, name='admin_classes'),
    path('admin_program/', views.admin_program, name='admin_program'),
    path('admin_trainers/', views.admin_trainers, name='admin_trainers'),
    path('amp_enrollment/', views.amp_enrollment, name='amp_enrollment'),
    path('contactfrom/', views.contactfrom, name='contactfrom'),
    path("coursefeedback/", views.coursefeedback, name="coursefeedback"),
    path("library/", views.library, name="library"),
    path("my_programs/", views.my_programs, name="my_programs"),
    path("partner_registeration/", views.partner_registeration, name="partner_registeration"),
    path("refer_earn/", views.refer_earn, name="refer_earn"),
    path("student_form/", views.student_form, name="student_form"),
    path('reg/', views.reg, name='reg'),
    path('admin_announcements/',views.admin_announcements, name ="admin_announcements"),
    path('success_stories/',views.success_stories, name ="success_stories"),
    path("admin_quiz/",views.admin_quiz, name="admin_quiz"),
    path('add_quiz/',views.add_quiz, name="add_quiz"),
    path('admin_trainer_add/',views.admin_trainer_add, name='admin_trainer_add'),
    path('admin_program_add',views.admin_program_add, name='admin_program_add'),
    path('support_ticket/',views.support_ticket,name="support_ticket"),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('terms_and_condition/',views.terms_and_condition, name='terms_and_condition'),
    path('community/',views.community, name='community'),
    path('blog/',views.blog, name='blog'),
    path("admin_partners/", views.admin_partners, name="admin_partners"),
    path("admin_payments/",views.admin_payments,name="admin_payments"),
    path("admin_student_add/",views.admin_student_add,name="admin_student_add"),
    path("admin_resources/", views.admin_resources, name="admin_resources"),
    path("admin_batch/", views.admin_batch, name="admin_batch"),
    path("admin_class_recordings/", views.admin_class_recordings, name="admin_class_recordings"),   
    path("commissions/", views.commissions, name="commissions"),
    path("exams/", views.exams, name="exams"),
    path("invoices/", views.invoices, name="invoices"),
    path("prog_cat/", views.prog_cat, name="prog_cat"),
    path("refunds/", views.refunds, name="refunds"),
    path("results/", views.results, name="results"),
    path("revenue/", views.revenue, name="revenue"),
    path("admin_trainer_schedule/", views.admin_trainer_schedule, name="admin_trainer_schedule"),
    path("admin_user/", views.admin_user, name="admin_user"),
    path("admin_program_categories/", views.admin_program_categories, name="admin_program_categories"),
    path("admin_exams/", views.admin_exams, name="admin_exams"),
    path("admin_results/", views.admin_results, name="admin_results"),
    path("admin_trnx/", views.admin_trnx, name="admin_trnx"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
