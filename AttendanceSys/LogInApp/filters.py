import django_filters
from .models import *


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['fk_course_id' ,'mobile_number', 'email' ,'image_name' ]


class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = ['student_id']

