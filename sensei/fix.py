

#########################
# Fix student records

from sensei.models import *
from sensei.student import *

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



#########################
# Export all the students to a file

from sensei.student import *

export_students()


#########################
# Design review logic

from sensei.models import *
from sensei.review import *


def list_reviews():
    for r in Review.objects.all():
        print(r.designer.name, r.page, r.due)


def clear_reviews():
    Review.objects.all().delete()


def test_reviews():
    student = Student.objects.get(name='Test Student')
    assert(student.name == 'Test Student')
    clear_reviews()
    r  = create_review(student, student, 'bacs200/index.html', '2019-01-22')
    assert(r.designer == student)
    assert(len(Review.objects.all()) == 1)
    create_review(student, student, '', '2019-01-20')
    create_review(student, student, 'bacs200/inspire.html', '2019-01-21')
    list_reviews()
    test_groups()

test_reviews()


def test_groups():
    pairs = review_pairs(review_groups())
    for p in pairs:
       print(p[0].name, p[1].name)
    print(len(pairs))

test_groups()


def list_groups():
    for g in review_groups():
        print(',  '.join([x.name for x in g]))

list_groups()


# Create review assignment

from sensei.review import *
clear_reviews()
print('Assign %d' % assign_reviews('bacs200/inspire.html', '2019-01-23'))
print("%s reviews assigned" % len(Review.objects.all()))


#########################
# Create Course

'''
Title:  UNC BACS 200 - Web Dev for Small Business

Description:
University of Northern Colorado
Monfort College of Business
Business Administration Computer Science
BACS 200
Web Design and Development for Small Business
'''

