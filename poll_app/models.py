from django.db import models

# Create your models here.


class Person(models.Model):
    fio = models.CharField(max_length=250)
    age = models.IntegerField()
    bio = models.TextField()
    photo = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.fio


class Poll(models.Model):
    title = models.CharField(max_length=250)
    date_start = models.DateField()
    date_end = models.DateField()
    max_vote = models.IntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey('Person', blank=True, null=True, on_delete=models.SET_NULL, related_name='winner')
    persons = models.ManyToManyField(Person)

    def __str__(self):
        return self.title


class Votes(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)