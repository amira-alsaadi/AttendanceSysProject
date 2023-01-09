from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import StudentForm, ContactForm
from .filters import StudentFilter, AttendanceFilter
from .models import Course, Student, Attendance, Lecturer
from django.views.decorators.csrf import csrf_exempt  # to disable Cross-Site Request Forgary
from django.contrib import messages
import cv2, os, face_recognition
import numpy as np
from django.http import HttpResponse
import csv
import pandas as pd
from plotly.offline import plot
import plotly.express as px


# Create your views here.
def homePage(request):
    return render(request, 'LogInApp/LogInPage.html')


@csrf_exempt
def logInPage(request):
    # print("test")
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        # print(username)
        # print(password1)
        lecturer = authenticate(request, username=username, password=password1)
        #login(request, lecturer)
        if lecturer is not None:
            login(request, lecturer)
            messages.success(request, 'You are Logged In Successfuly!!')
            return redirect('viewCourse')

        else:
            messages.error(request, 'Incorrect entries try again')
            return redirect('logIn')
            # return HttpResponse('Incorrect entries try again')

    context = {}
    return render(request, 'LogInApp/LogInPage.html', context)

# home page
def viewCourse(request):
    use = User.objects.all()
    #print(use)
    courses = Course.objects.all()
    # print(courses)
    context = {'courses': courses, 'use': use}
    return render(request, 'LogInApp/ViewCourse.html', context)


# after selecting course
def mainPage(request):
    return render(request, 'LogInApp/mainPage.html')


def logOutPage(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")

    return render(request, 'LogInApp/LogInPage.html')


def cameraCap(object):
    path = "LogInApp/resources/resources"
    images = []
    Names = []
    # lists the images names in the path file
    myList = os.listdir(path)
    # print(myList)
    # for loop to import the images from myList to the empty list (Names)
    for cl in myList:
        curImg = cv2.imread(f"{path}/{cl}")
        images.append(curImg)
        # image name withouth the extention .jpeg
        Names.append(os.path.splitext(cl)[0])
    print(Names)

    # function to compute the encooding of each image in the list
    def findEncodings(images):
        encodeList = []  # empty list that will hv all the encodings
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print("Encoding Complete")

    def markattendance(name):
        if name in Names:
            # fitches the information related to the detected name
            attend = Student.objects.filter(student_id=name).values('student_id', 'fk_course_id_id')
            # filter returns a queryset. A queryset isn't a single object, it's a group of objects so it doesn't make sense
            # to call save() on a queryset. Instead you save each individual object IN the queryset:
            student_with_name = attend[0]
            #print(student_with_name)

            if Attendance.objects.filter(student_id=name).exists():
                print("student exist")
            else:
                # INSERT SQL statement behind the scenes. Django doesn’t hit the database until you explicitly call save().
                reg = Attendance(student_id=student_with_name.get('student_id'),
                                 course_id=student_with_name.get('fk_course_id_id'),
                                 attendanceState='Present')

                print("student added")
                reg.save()

    cap = cv2.VideoCapture(0)  # compare the webcam image with the stored image
    while True:  # while loop to get each frame
        success, img = cap.read()
        # reduce the size of the image to speed up the process in real time
        imgSm = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # one fourth of the size
        imgSm = cv2.cvtColor(imgSm, cv2.COLOR_BGR2RGB)  # convert to rgb
        findCurrentFrame = face_recognition.face_locations(
            imgSm)  # find the faces locations incase two or more faces appear in webcam
        encodeCurrentFrame = face_recognition.face_encodings(imgSm,
                                                             findCurrentFrame)  # find the encoding of the webcam image + the locations

        # finding the matches of the founded webcam images with the ones  encoded in the list
        # one by one grab each one face location detected from current farme and grab the encoding of it from encode current frame
        for encodeFace, faceLoc in zip(encodeCurrentFrame,
                                       findCurrentFrame):  # we use zip because we want them in the same loop
            matches = face_recognition.compare_faces(encodeListKnown,
                                                     encodeFace)  # compare lists of known faces with the encodes
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # face_distance returns a list calculating the distance,the lowest distance value is the best match
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = Names[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markattendance(name)
            else:
                name = "Unknown"
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # because we resized the actual captured pictures to speed the process
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

        # cv2.imshow("Webcam", img)
        # cv2.waitKey(1)
    return render(object, 'LogInApp/mainPage.html')


def viewStudents(request):
    students = Student.objects.all()
    # print(students)
    stufilter = StudentFilter(request.GET, queryset=students)
    students = stufilter.qs
    context = {'students': students, 'stufilter': stufilter}
    return render(request, 'LogInApp/ViewStudent.html', context)


@csrf_exempt
def registerStudents(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student has been added successfully')
            return redirect('viewStudents')

    context = {'form': form}
    return render(request, 'LogInApp/RegisterStudent.html', context)


def viewAttendance(request):
    attendance = Attendance.objects.all()
    context = {'attendance': attendance}

    return render(request, 'LogInApp/ViewAttendance.html', context)

def saveAttendance(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= Attendance.csv'
    # create a csv writer
    writer = csv.writer(response)
    # display whatever stored in the model to the text sheet
    attendance = Attendance.objects.all()
    # add column heading
    writer.writerow(['StudentID', 'Course ID', 'Date', 'Time'])
    # loop thu students
    for stuattendance in attendance:
        writer.writerow([stuattendance.student_id,
                         stuattendance.course_id, stuattendance.date, stuattendance.time])
    return response


def viewReport(request):
    attendance = Attendance.objects.all()
    graph_data = [
        {
            'Student': x.student_id,
            'Start': x.start_date,
            'Finish': x.end_date,
            'Course': x.course_id
        } for x in attendance
    ]
    graph_frame = pd.DataFrame(graph_data)
    figure = px.timeline(
        graph_frame, x_start="Start", x_end="Finish", y="Course", color="Student"
    )
    figure.update_yaxes(autorange="reversed")
    gantt_plot = plot(figure, output_type="div")

    # print(attendance)
    attendfilter = AttendanceFilter(request.GET, queryset=attendance)
    attendance = attendfilter.qs
    context = {'attendance': attendance, 'attendfilter': attendfilter, 'gantt_plot': gantt_plot}
    return render(request, 'LogInApp/ViewReport.html', context)


def aboutUs(request):
    return render(request, 'LogInApp/AboutUs.html')


def contactUs(request):
    form = ContactForm
    if request.method == 'POST':
        form = ContactForm(request.POST)
        #print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully')
            return redirect('contactUs')

    context = {'form': form}
    return render(request, 'LogInApp/ContactUs.html', context)
