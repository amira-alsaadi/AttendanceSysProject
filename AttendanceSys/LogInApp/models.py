from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Lecturer(models.Model):
    lecturer_id = models.AutoField(primary_key=True)
    lecturer_fname = models.CharField(max_length=100, null=True)
    lecturer_lname = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    password1 = models.CharField(max_length=50, null=True)
    password2 = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.lecturer_id, self.lecturer_fname, self.lecturer_lname)


class Course(models.Model):
    COURSES = (
        ('Data Structure','Data Structure'),
        ('Computer Network','Computer Network'),
        ('Web Design','Web Design'),
        ('Internet of Things','Internet of Things'),
        ('Artificial Intelligence','Artificial Intelligence'),
        ('Artificial Intelligence-Tut', 'Artificial Intelligence-Tut'),
    )
    course_id = models.AutoField(primary_key=True)
    fk_lecturer_id = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=100, null=True, choices=COURSES)
    date = models.DateField(max_length=20, null=True)
    start_time = models.TimeField(max_length=20, null=True)
    finish_time = models.TimeField(max_length=20, null=True)

    def __str__(self):
        return '{} {}'.format(self.course_id, self.course_name)


class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=100)
    student_fname = models.CharField(max_length=100, null=True)
    student_lname = models.CharField(max_length=100, null=True)
    fk_course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True) # foreign key
    mobile_number = models.IntegerField(null=True)
    email = models.EmailField(max_length=100, null=True)
    image_name = models.ImageField(upload_to='resources', blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.student_id, self.student_fname, self.student_lname)

    @property
    def course_id(self):
        return self.fk_course_id.course_id


class Attendance(models.Model):
    ATTENDANCE = (
        ('absent', 'Absent'),
        ('present', 'Present')
    )
    student_id = models.CharField(max_length=100, null=True)
    course_id = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    attendanceState = models.CharField(max_length=20, null=True,choices=ATTENDANCE)
    start_date = models.DateField(default='2022-02-27')
    #week_num = models.CharField(max_length=2, blank=True)
    end_date = models.DateField(default='2022-06-27')

    def __str__(self):
        return '{}'.format(self.student_id)

    #def save(self, *args, **kwargs):
        #print(self.start_date.isocalendar()[1])
        #if self.week_num == "":
            #self.week_num = self.start_date.isocalendar()[1]
        #super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(max_length=100, null=True)
    message = models.TextField(max_length=200, null=True)

    def __str__(self):
        return '{}'.format(self.name)


