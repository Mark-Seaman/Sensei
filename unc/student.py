# Import list of students
from unc.models import Student


def import_students():
    '''
    usage:   dj shell
         $ from unc.student import *
         $ import_students()
    '''

    print('import_students')
    print(open('data/students.csv').read())


def list_students():
    '''
    usage:   dj shell
         $ from unc.student import *
         $ list_students()
    '''

    print('list_students')
    print ('\n'.join(Student.objects.all()))
