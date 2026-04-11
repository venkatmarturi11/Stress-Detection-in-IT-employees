from django.db import models

# Create your models here.
class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=1000, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=100)
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistrations'
class UserImagePredictionModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    loginid = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    emotions = models.CharField(max_length=10000)
    stress_level = models.CharField(max_length=50, default='Low')
    confidence = models.IntegerField(default=0)
    eye_strain = models.CharField(max_length=50, default='Normal')
    brow_tension = models.CharField(max_length=50, default='Normal')
    facial_fatigue = models.CharField(max_length=50, default='Normal')
    file = models.FileField(upload_to='files/', null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = "UserStressImageResults"


class UserSurveyPredictionModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.IntegerField()
    designation = models.IntegerField()
    company_type = models.IntegerField()
    wfh_setup = models.IntegerField()
    resource_allocation = models.FloatField()
    mental_fatigue = models.FloatField()
    stress_percentage = models.FloatField()
    risk_level = models.CharField(max_length=20)
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "UserSurveyPredictions"