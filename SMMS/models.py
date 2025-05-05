
from django.db import models
import MySQLdb
from django.conf import settings


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
        (ticket_subject, ticket_priority, ticket_category, ticket_message, ticket_attachment)
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

