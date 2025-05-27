
from django.db import models
import MySQLdb
from django.conf import settings
import json

class Student(models.Model):
    @classmethod
    def add_student(cls, data):
        print("Data to be inserted:")
        print(f"first_name: {data.get('first_name')}")
        """Save data directly to MySQL using raw SQL"""
        db_settings = settings.DATABASES['default']

        # Connect to MySQL database
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()

        # Create SQL query for insertion
        query = """
        INSERT INTO students 
        (first_name, last_name, email, phone, dob, gender, address_line1 , address_line2 , city , state , postal_code , country , program, batch, referral_source, notes, payment_status, payment_method, amount_paid, transaction_id , invoice_number, payment_date, username , password)  
        VALUES (%s, %s, %s, %s, %s, %s , %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s , %s) 
        """
        try:
        # Execute the query with data
            cursor.execute(query, (
                    data.get('first_name', ''),
                    data.get('last_name', ''),
                    data.get('email', ''),
                    data.get('phone', ''),
                    data.get('dob', ''),
                    data.get('gender', ''),
                    data.get('address_line1', ''),
                    data.get('address_line2', ''),
                    data.get('city', ''),
                    data.get('state', ''),
                    data.get('postal_code', ''),
                    data.get('country', ''),
                    data.get('program', ''),
                    data.get('batch', ''),
                    data.get('referral_source', ''),
                    data.get('notes', ''),
                    data.get('payment_status', ''),
                    data.get('payment_method', ''),
                    data.get('amount_paid', ''),
                    data.get('transaction_id', ''),
                    data.get('invoice_number', ''),
                    data.get('payment_date', ''),
                    data.get('username', ''),
                    data.get('password', '')
                ))
                # Commit the transaction
            db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()  # Rollback in case of error
        finally:
            if cursor:
                cursor.close()
            # Close the connection
        db.close()
        return True 

    @classmethod
    def get_all_students(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM students")
        # Fetch all results
        results = cursor.fetchall()
        db.close()
        return results
    
    @classmethod
    def studntno(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select count(*) as stdnts from students")
        results = cursor.fetchall()
        db.close()
        return results
    
class PersonalInformation(models.Model):
    @classmethod
    def save_to_mysql(cls, data):
        """Save data directly to MySQL using raw SQL"""
        db_settings = settings.DATABASES['default']

        # Connect to MySQL database
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )

        cursor = db.cursor()

        # Create SQL query for insertion
        query = """
        INSERT INTO tmpreg 
        (first_name, last_name, email, phone, address, state) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        print("Data to be inserted:")
        print(f"first_name: {data.get('first_name')}")
        print(f"last_name: {data.get('last_name')}")
        print(f"email: {data.get('email')}")
        print(f"phone: {data.get('phone')}")
        print(f"dob: {data.get('dob')}")
        print(f"gender: {data.get('gender')}")
        # Execute the query with data
        cursor.execute(query, (
            data.get('first_name', ''),
            data.get('last_name', ''),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('dob', ''),
            data.get('gender', '')
        ))

        # Commit the transaction
        db.commit()
        if cursor:
            cursor.close()
        # Close the connection
        db.close()

        return True

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200)

    class Meta:
        managed = False  # Django won't manage this table
        db_table = 'tmpreg'  # Exact name of your MySQL table

    def __str__(self):
        return f"{self.first_name} - {self.state}%"
    @classmethod
    def get_all(cls):
        db_settings = settings.DATABASES['default']

        # Connect to MySQL database
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )

        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        # Execute query to get all records
        cursor.execute("SELECT * FROM tmpreg")

        # Fetch all results
        results = cursor.fetchall()

        # Close the connection
        db.close()

        # Return the results
        return results
    """Get all records from the database"""

class Assessment(models.Model):
    user = models.CharField(max_length=100)
    quizzes = models.IntegerField()
    assignments = models.IntegerField()
    exams = models.IntegerField()
    overall = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.overall}%"

    class Meta:
        # This indicates Django to not create table for this model
        managed = False
        db_table = 'assessment'  # MySQL table name

    @classmethod
    def get_assessments(cls):
        try:
            # Get database settings from Django settings
            db_settings = settings.DATABASES['default']

            # Connect to MySQL database using settings
            db = MySQLdb.connect(
                host=db_settings['HOST'],
                user=db_settings['USER'],
                passwd=db_settings['PASSWORD'],
                db=db_settings['NAME'],
                port=int(db_settings['PORT']),
            )
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM assessment")
            results = cursor.fetchall()
            db.close()
            return results
        except Exception as e:
            print(f"Error retrieving assessments: {e}")
            return []

class reg(models.Model):
    @classmethod
    def add_student_class(cls, data):
        """Save data directly to MySQL using raw SQL"""

        # Connect to MySQL database
        db_settings = settings.DATABASES['default']

        # Connect to MySQL database
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )


        cursor = db.cursor()

        # Create SQL query for insertion
        query = """
        INSERT INTO live_classes 
        (description,meeting_link) 
        VALUES (%s, %s)
        """

        print("Data to be inserted:")
        print(f"topcs: {data.get('topic')}")
        print(f"mtngs: {data.get('meeting_link')}")
     
        # Execute the query with data
        cursor.execute(query, (
            data.get('topic', ''),
            data.get('meeting_link', '')
           
        ))

        # Commit the transaction
        db.commit()
        if cursor:
            cursor.close()
        # Close the connection
        db.close()

        return True

class support_ticketx(models.Model):
    @classmethod
    def add_support_ticket(cls, data):
        """Save data directly to MySQL using raw SQL"""

        # Connect to MySQL database
        db_settings = settings.DATABASES['default']

        # Connect to MySQL database
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )

        cursor = db.cursor()

        # Create SQL query for insertion

        print("Data to be inserted:")
        print(f"subject: {data.get('ticket_subject')}")
        print(f"priority: {data.get('ticket_priority')}")
        print(f"category: {data.get('ticket_category')}")
        print(f"message: {data.get('ticket_message')}")
        print(f"attachment: {data.get('ticket_attachment')}")

        query = """
        INSERT INTO support_tickets
        (subject, proirity, category, message, attachment)
        VALUES (%s, %s, %s, %s, %s)
        """

        # Execute the query with data
        cursor.execute(query, (
            data.get('ticket_subject', ''),
            data.get('ticket_priority', ''),
            data.get('ticket_category', ''),
            data.get('ticket_message', ''),
            data.get('ticket_attachment', '')
        ))
        # Commit the transaction
        db.commit()
        if cursor:
            cursor.close()
        # Close the connection
        db.close()
        return True

    @classmethod
    def get_all_tickets(cls):
        """Fetch all support tickets from the database"""

        db_settings = settings.DATABASES['default']

        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )

        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM support_tickets ORDER BY id DESC")
        results = cursor.fetchall()
        db.close()
        return results

class Batch(models.Model):
    @classmethod
    def add_batch(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('batch_code')}")
        print(f"priority: {data.get('batch_name')}")
        print(f"program: {data.get('program')}")
        print(f"start_date: {data.get('start_date')}")
        print(f"end_date: {data.get('end_date')}")
        print(f"capacity: {data.get('capacity')}")
        print(f"status: {data.get('status')}")
        print(f"trainer: {data.get('trainer')}")
        print(f"description: {data.get('description')}")
        """Save data directly to MySQL using raw SQL"""
        # Connect to MySQL database
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        query = """
        INSERT INTO batch_management
        (batch_code, batch_name, program, start_date, end_date, capacity, trainer, status, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('batch_code', ''),
            data.get('batch_name', ''),
            data.get('program', ''),
            data.get('start_date',''),
            data.get('end_date', ''),
            data.get('capacity', ''),
            data.get('status', ''),
            data.get('trainer', ''),
            data.get('description', '')
        ))
        db.commit()
        if cursor:
            cursor.close()
        db.close()
        return True

    @classmethod
    def get_all_batches(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM batch_management ORDER BY id DESC")
        results = cursor.fetchall()
        db.close()
        return results

class Trainer(models.Model):
    @classmethod
    def add_trainer(cls, data):
        print("Data to be inserted:")
        print(f"first_name: {data.get('first_name')}")
        print(f"last_name: {data.get('last_name')}")
        print(f"email: {data.get('email')}")
        print(f"phone: {data.get('phone')}")
        print(f"dob: {data.get('dob')}")
        print(f"gender: {data.get('gender')}")
        # Connect to MySQL database
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        # expertise_areas_json = json.dumps(data.get('expertise_areas', []))
        # certifications_json = json.dumps(data.get('certifications', []))
        # programs_json = json.dumps(data.get('programs', []))
        # specific_modules_json = json.dumps(data.get('specific_modules', []))
        #
        # # Handle profile_picture_file saving logic as needed (e.g., save to media folder)
        # For now, store filename or path as string
        # profile_picture_path = profile_picture_file.name if profile_picture_file else ''

        query = """
        INSERT INTO trainers
        (first_name, last_name, email, phone, dob, gender,
         address_line1, address_line2, city, state, postal_code, country,
         designation, experience_years, teaching_experience, bio, hourly_rate,
         max_hours_weekly, create_account, username, password, linkedin_profile, website, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (
                data.get('first_name', ''),
                data.get('last_name', ''),
                data.get('email', ''),
                data.get('phone', ''),
                data.get('dob', ''),
                data.get('gender', ''),
                data.get('address_line1', ''),
                data.get('address_line2', ''),
                data.get('city', ''),
                data.get('state', ''),
                data.get('postal_code', ''),
                data.get('country', ''),
                data.get('designation', ''),
                data.get('experience_years', 0),
                data.get('teaching_experience', 0),
                # data.get('expertise_areas_json', '')
                # data.get(certifications_json,''),
                data.get('bio', ''),
                # programs_json,
                # specific_modules_json,
                data.get('hourly_rate', 0),
                data.get('max_hours_weekly', 20),
                int(data.get('create_account', False)),
                data.get('username', ''),
                data.get('password', ''),
                data.get('linkedin_profile', ''),
                data.get('website', ''),
                data.get('notes', ''),
            ))
            db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()  # Rollback in case of error 
        finally:
            if cursor:
                cursor.close()
            db.close()
            return True

    @classmethod
    def get_all_trainers(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM trainers ORDER BY id DESC")
        results = cursor.fetchall()
        db.close()
        return results

class TrainerSchedule(models.Model):
    @classmethod
    def add_schedule(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('program')}")
        print(f"priority: {data.get('batch')}")
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        query = """
        INSERT INTO trainer_schedules
        (program, batch, topic, description, class_date, trainer, start_time, end_time, meeting_link, meeting_password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('program', ''),
            data.get('batch', ''),
            data.get('topic', ''),
            data.get('description', ''),
            data.get('class_date', ''),
            data.get('trainer', ''),
            data.get('start_time', ''),
            data.get('end_time', ''),
            data.get('meeting_link', ''),
            data.get('meeting_password', ''),
        ))
        db.commit()
        if cursor:
            cursor.close()
        db.close()
        return True

    @classmethod
    def get_all_schedules(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM trainer_schedules ORDER BY class_date DESC, start_time DESC")
        results = cursor.fetchall()
        db.close()
        return results

class Program(models.Model):
    @classmethod
    def add_program(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('title')}")
        print(f"priority: {data.get('duration_months')}")
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()

        # Handle program_image_file saving logic as needed (e.g., save to media folder)
        # For now, store filename or path as string
        # program_image_path = program_image_file.name if program_image_file else ''

        query = """
        INSERT INTO programs
        (title, duration_months, num_classes, students_enrolled, price, revenue, rating, completion_percentage,
        description, status, is_featured)  # Remove the trailing comma
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  # Use 11 placeholders to match 11 columns
        """

        cursor.execute(query, (
            data.get('title', ''),
            data.get('duration_months', 0),
            data.get('num_classes', 0),
            data.get('students_enrolled', 0),
            data.get('price', 0.0),
            data.get('revenue', ''),
            data.get('rating', 0.0),
            data.get('completion_percentage', 0),
            data.get('description', ''),
            data.get('status', ''),
            data.get('is_featured', ''),
        ))
        db.commit()
        if cursor:
            cursor.close()
        db.close()
        return True
            
    @classmethod
    def get_all_programs(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM programs")
        results = cursor.fetchall()
        db.close()
        return results
    @classmethod
    def prgno(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select count(*) as prg from programs")
        results = cursor.fetchall()
        db.close()
        return results

class Class(models.Model):
    @classmethod
    def add_class(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('class_title')}")
        print(f"priority: {data.get('class_title')}")
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        query = """
        INSERT INTO classes
        (class_title, program, batch, description, class_date, start_time, end_time, duration,
         trainer, platform, meeting_link, meeting_password, prerequisites, materials, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.get('class_title', ''),
            data.get('program', ''),
            data.get('batch', ''),
            data.get('description', ''),
            data.get('class_date', ''),
            data.get('start_time', ''),
            data.get('end_time', ''),
            data.get('duration', 0),
            data.get('trainer', ''),
            data.get('platform', ''),
            data.get('meeting_link', ''),
            data.get('meeting_password', ''),
            data.get('prerequisites', ''),
            data.get('materials', ''),
            data.get('notes', ''),
        ))
        db.commit()
        if cursor:
            cursor.close()
        db.close()
        return True

    @classmethod
    def get_all_classes(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM classes ORDER BY class_date DESC, start_time DESC")
        results = cursor.fetchall()
        db.close()
        return results
        
class commissionx(models.Model):
    @classmethod
    def add_commission(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('partner')}")
        print(f"priority: {data.get('transaction_id')}")
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        
        query = """
        INSERT INTO commissions
        (transaction_id, partner, referred_student, program, amount, processing_fee, date, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (
                data.get('transaction_id', ''),
                data.get('partner', ''),
                data.get('referred_student', ''),
                data.get('program', ''),
                data.get('amount', 0),
                data.get('processing_fee', 0),
                data.get('date', ''),
                data.get('status', 'pending'),
                data.get('notes', '')
            ))
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()  # Rollback in case of error
        finally:
            db.commit()
            cursor.close()
            db.close()
        return True

    @classmethod
    def get_all_commissions(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM commissions")
        results = cursor.fetchall()
        db.close()
        return results
    
    @classmethod
    def get_comno(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM msksomim_.next_commission_view")
        results = cursor.fetchall()
        db.close()
        return results

class invoicex(models.Model):
    @classmethod
    def add_invoice(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('invoice_number')}")
        print(f"priority: {data.get('student')}")
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        
        query = """
        INSERT INTO invoices
        (invoice_number, student, program, batch, issue_date, due_date, 
         amount, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            data.get('invoice_number', ''),
            data.get('student', ''),
            data.get('program', ''),
            data.get('batch', ''),
            data.get('issue_date', ''),
            data.get('due_date', ''),
            data.get('amount', 0),
            data.get('status', 'pending'),
            data.get('notes', '')
        ))
        
        db.commit()
        cursor.close()
        db.close()
        return True

    @classmethod
    def get_all_invoices(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM invoices ORDER BY issue_date DESC")
        results = cursor.fetchall()
        db.close()
        return results

    @classmethod
    def get_invno(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM msksomim_.next_invoice_code_view")
        results = cursor.fetchall()
        db.close()
        return results
    
class announcementx(models.Model):
    @classmethod
    def add_announcement(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('title')}")
        print(f"priority: {data.get('message')}")
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        
        query = """
        INSERT INTO announcements
        (title, message, audience, program, batch, expiry_date, is_important, created_date, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            data.get('title', ''),
            data.get('message', ''),
            data.get('audience', 'all'),
            data.get('program', ''),
            data.get('batch', ''),
            data.get('expiry_date', ''),
            data.get('is_important', False),
            data.get('created_date', datetime.now().strftime('%Y-%m-%d')),
            data.get('created_by', 'Admin')
        ))
        
        db.commit()
        cursor.close()
        db.close()
        return True

    @classmethod
    def get_all_announcements(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM announcements")
        results = cursor.fetchall()
        db.close()
        return results

class refundx(models.Model):
    @classmethod
    def add_refund(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('refund_number')}")
        print(f"priority: {data.get('student')}")
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        
        query = """
        INSERT INTO refunds
        (refund_number, student, program, enrollment_id, request_date, amount, reason, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data.get('refund_number', 0),
            data.get('student', ''),
            data.get('program', ''),
            data.get('enrollment_id', ''),
            data.get('request_date', ''),
            data.get('amount', 0),
            data.get('reason', ''),
            data.get('status', 'pending'),
            data.get('notes', '')
        ))
        db.commit()
        cursor.close()
        db.close()
        return True

    @classmethod
    def get_all_refunds(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM refunds")
        results = cursor.fetchall()
        db.close()
        return results
    
    @classmethod
    def get_refno(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM msksomim_.next_refund_code_view")
        results = cursor.fetchall()
        db.close()
        return results
    
class User(models.Model):
    @classmethod
    def add_user(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('username')}")
        print(f"priority: {data.get('password')}")
        print(data.get('role_id'))

        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        query = """
        INSERT INTO users
        (first_name,last_name,username, password, confirm_password,email, phone,role, status, bio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (
                data.get('first_name', ''),
                data.get('last_name', ''),
                data.get('username', ''),
                data.get('password', ''),
                data.get('confirm_password', ''),
                data.get('email', ''),
                data.get('phone', ''),
                data.get('role', ''),
                data.get('status', ''),
                data.get('bio', '')
            ))
            db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()  # Rollback in case of error
        finally:
            cursor.close()
            db.close()
        return True
    
    def get_all_users(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        db.close()
        return results
    
class ProgramCategory(models.Model):
    @classmethod
    def add_program_category(cls, data):
        print("Data to be inserted:")
        print(f"subject: {data.get('category_name')}")
        print(f"priority: {data.get('description')}")
        print(f"priority: {data.get('icon')}")  
        
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor()
        
        query = """
        INSERT INTO program_categories
        (category_name, description, icon)
        VALUES (%s, %s, %s)
        """
        
        try:
            cursor.execute(query, (
                data.get('category_name', ''),
                data.get('description', ''),
                data.get('icon', ''),
            ))
            db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()  # Rollback in case of error
        finally:
            cursor.close()
            db.close()
        return True


    @classmethod
    def get_all_program_categories(cls):
        db_settings = settings.DATABASES['default']
        db = MySQLdb.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            passwd=db_settings['PASSWORD'],
            db=db_settings['NAME'],
            port=int(db_settings['PORT']),
        )
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM program_categories")
        results = cursor.fetchall()
        db.close()
        return results