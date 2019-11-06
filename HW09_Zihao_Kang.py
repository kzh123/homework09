"""
summarize student and instructor data
@author:10456094
"""

from HW08_Zihao_Kang import file_reading_gen
from collections import defaultdict
from prettytable import PrettyTable


class Repository:
    """hold the students, instructors and grades for a single University"""
    def __init__(self, dir_path, print_pt=False):
        """read all the things from all the place"""
        self.grade_course_cwid, self.grade_course_student = Grades(dir_path + 'grades.txt').cwid_course_student()
        self.instructor_dict = Instructor(dir_path + 'instructors.txt').instructor_dict_CW()
        self.student_dict = Student(dir_path + 'students.txt').student_dict_CW()
        self.student_id_course_dict = Grades(dir_path + 'grades.txt').student_id_course()
        if print_pt:
            print("Instructor Summary")
            self.print_instructor_pt()
            print("Student Summary")
            self.print_student_pt()

    def print_instructor_pt(self):
        """
        dict:
        Course(key):CWID-name-DEPT-student
        """
        instructor_dict_pt = dict()
        for key, value in self.grade_course_cwid.items():
            instructor_dict_pt.update(
                {key: {'CWID': value, 'name': self.instructor_dict[value][0], 'DEPT': self.instructor_dict[value][1],
                       'student': self.grade_course_student[key]}})

        pt_instructors = PrettyTable(field_names=['CWID', "Name", "Dept", "Course", "Students"])
        for key, value in instructor_dict_pt.items():
            pt_instructors.add_row([value['CWID'], value['name'], value['DEPT'], key, value['student']])
        print(pt_instructors)

    def print_student_pt(self):
        """
        dict:
        CWID(key):Name-completed course
        """
        student_dict_pt = dict()
        for key, value in self.student_id_course_dict.items():
            student_dict_pt.update(
                {key: {'name': self.student_dict[key][0], 'completed course': sorted(value)}}
            )

        pt_student = PrettyTable(field_names=["CWID", "Name", "Completed Courses"])
        for key, value in student_dict_pt.items():
            pt_student.add_row([key, value['name'], value['completed course']])
        print(pt_student)


class Student:
    """hold all of the details of a student"""
    def __init__(self, path):
        """read file"""
        try:
            self.student_list = file_reading_gen(path, 3, sep='\t', header=False)
        except ValueError:
            """can be changed in future homework"""
            raise ValueError
        self.student_dict = defaultdict(dict)

    def student_dict_CW(self):
        """CWID(key)-name-DEPT"""
        for item in self.student_list:
            self.student_dict.update({item[0]: [item[1], item[2]]})
        return self.student_dict


class Instructor:
    """hold all of the details of an instructor"""
    def __init__(self, path):
        """read file"""
        try:
            self.instructor_list = file_reading_gen(path, 3, sep='\t', header=False)
        except ValueError:
            """can be changed in future homework"""
            raise ValueError
        self.instructor_dict = defaultdict(dict)

    def instructor_dict_CW(self):
        """CWID(key)-name-DEPT"""
        for item in self.instructor_list:
            self.instructor_dict.update({item[0]: [item[1], item[2]]})
        return self.instructor_dict


class Grades:
    """info from grades.txt"""
    def __init__(self, path):
        try:
            self.grade_list = list(file_reading_gen(path, 4, sep='\t', header=False))
        except ValueError:
            """can be changed in future homework"""
            raise ValueError

    def cwid_course_student(self):
        """return ins_cwid-course and course-student(number) dict"""
        ins_cwid_course_dict = defaultdict(str)
        course_student_dict = defaultdict(int)

        for item in self.grade_list:
            ins_cwid_course_dict[item[1]] = (item[3])
            course_student_dict[item[1]] += 1

        # print(f"11{ins_cwid_course_dict}")
        # print(f"11{course_student_dict}")

        return ins_cwid_course_dict, course_student_dict

    def student_id_course(self):
        student_id_course_dict = defaultdict(list)
        for item in self.grade_list:
            student_id_course_dict[item[0]].append(item[1])

        return student_id_course_dict


if __name__ == '__main__':
    stevens = Repository('./', print_pt=True)
    # pt_instructors = PrettyTable(field_names=['CWID', "Name", "Dept", "Course", "Students"])
    # for key, value in Repository().instructor_summary().items():
    #     pt_instructors.add_row([value['CWID'], value['name'], value['DEPT'], key, value['student']])
    # print(pt_instructors)

    # pt_student = PrettyTable(field_names=["CWID", "Name", "Completed Courses"])
    # for key, value in Repository().student_summary().items():
    #     pt_student.add_row([key, value['name'], value['completed course']])
    # print(pt_student)


# a = Grades('grades.txt')
# a.student_id_course()
#
# b = Instructor('instructors.txt')
# # print(b.instructor_dict_CW())
# a = Grades('grades.txt')
# print(f"student id course{a.student_id_course()}")
# b = Student('students.txt')
# # print(f"course {b.student_dict_CW()}")
# c = Repository()
# print(c.student_summary())
# print(c.instructor_summary())