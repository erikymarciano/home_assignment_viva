from django.db import models
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class Participant(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_no = models.CharField(max_length=15, unique=True)
    date_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Team(models.Model):
    name = models.CharField(max_length=150)
    representative_name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    member = models.ManyToManyField('Participant')
    
    def __str__(self):
        return self.name
        

class Instance(models.Model):
    INSTANCES = (
        ('Local', 'Local'),
        ('National', 'National'),
        ('Regional', 'Regional'),
        ('International', 'International')
    )
    name = models.CharField(max_length=13, choices=INSTANCES, blank=False, null=False)

    def __str__(self):
        return self.name


class Competition(models.Model):
    instance = models.ForeignKey("Instance", on_delete=models.CASCADE, blank=False, null=False)
    year = models.IntegerField(validators=[MinValueValidator(1900)])

    def __str__(self):
        return f'{str(self.year)} - {self.instance.name}'


class CompetitionLog(models.Model):
    competition =  models.ForeignKey("Competition", on_delete=models.PROTECT, blank=False, null=False)
    team = models.ForeignKey("Team", on_delete=models.PROTECT, blank=False, null=False)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'Competition Log: {self.competition} - {self.team}'
