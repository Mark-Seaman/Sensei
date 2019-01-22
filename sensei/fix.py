from sensei.models import *


def fix_reading_names():
    for s in Student.objects.all():
        if not s.zbooks:
            s.zbooks = s.name
            s.save()


def fix_email_names():
    for s in Student.objects.all():
        if s.email != s.email.lower():
            s.email = s.email.lower()
            s.save()


def stud(id):
    return Student.objects.get(pk=id)


def name(name):
    return Student.objects.filter(name__contains=name)


# Export all the students to a file
from sensei.student import *
export_students()


'''
Title:  UNC BACS 200 - Web Dev for Small Business

Description:
University of Northern Colorado
Monfort College of Business
Business Administration Computer Science
BACS 200
Web Design and Development for Small Business
'''

