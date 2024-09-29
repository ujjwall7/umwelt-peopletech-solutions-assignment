from django.db import models


from django.db import models

class Enrollee(models.Model):
    ENROLLMENT_CHOICES = [
        ('no_enrollment', 'No Enrollment'),
        ('Full time course', 'Full Time Course'),
        ('Part time course', 'Part Time Course')
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('Graduate', 'Graduate'),
        ('Masters', 'Masters'),
        ('High School', 'High School')
    ]
    
    MAJOR_DISCIPLINE_CHOICES = [
        ('STEM', 'STEM'),
        ('Business Degree', 'Business Degree'),
        ('Humanities', 'Humanities'),
        ('Arts', 'Arts')
    ]
    
    COMPANY_SIZE_CHOICES = [
        ('<10', '<10'),
        ('10-49', '10-49'),
        ('50-99', '50-99'),
        ('100-500', '100-500'),
        ('500-999', '500-999'),
        ('1000-4999', '1000-4999'),
        ('5000-9999', '5000-9999'),
        ('10000+', '10000+'),
        ('Oct-49', 'Oct-49')
    ]
    
    COMPANY_TYPE_CHOICES = [
        ('Pvt Ltd', 'Private Limited'),
        ('Funded Startup', 'Funded Startup')
    ]
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    
    LAST_NEW_JOB_CHOICES = [
        ('never', 'Never'),
        ('1', '1 Year'),
        ('2', '2 Years'),
        ('3', '3 Years'),
        ('4', '4 Years'),
        ('>4', 'More than 4 Years')
    ]

    EXPERINCE_CHOICES = [
        ('Has relevent experience','Has relevent experience'),
         ('No relevent experience','No relevent experience')
    ]
    
    enrollee_id = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    city_development_index = models.FloatField(null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    relevent_experience = models.CharField(max_length=150, choices=EXPERINCE_CHOICES, null=True)
    enrolled_university = models.CharField(max_length=50, choices=ENROLLMENT_CHOICES, default='no_enrollment')
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    major_discipline = models.CharField(max_length=50, choices=MAJOR_DISCIPLINE_CHOICES, null=True, blank=True)
    experience = models.CharField(max_length=10, null=True)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES, null=True, blank=True)
    company_type = models.CharField(max_length=50, choices=COMPANY_TYPE_CHOICES, null=True, blank=True)
    last_new_job = models.CharField(max_length=10, choices=LAST_NEW_JOB_CHOICES, null=True, blank=True)
    training_hours = models.IntegerField()
    target = models.BooleanField(default=False)

    def __str__(self):
        return f"Enrollee {self.enrollee_id} - {self.city}"

class Company(models.Model):
    gmail_email = models.EmailField(verbose_name='Email (Send Mail)', null=True, blank=True)
    password=models.CharField(max_length=350,verbose_name='Password (Send Mail)', blank=True)
    


