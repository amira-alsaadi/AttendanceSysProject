from django.forms import ModelForm
from .models import Lecturer, Attendance, Student, Contact


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'



