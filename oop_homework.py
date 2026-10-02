from functools import total_ordering


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (
            isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress
            and course in lecturer.courses_attached
        ):
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def average_grade(self):
        all_grades = [g for course_grades in self.grades.values() for g in course_grades]
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        in_progress = ', '.join(self.courses_in_progress)
        finished = ', '.join(self.finished_courses)
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self.average_grade():.1f}\n"
            f"Курсы в процессе изучения: {in_progress}\n"
            f"Завершенные курсы: {finished}"
        )

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() == other.average_grade()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        all_grades = [g for course_grades in self.grades.values() for g in course_grades]
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {self.average_grade():.1f}"
        )

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() == other.average_grade()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            student.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


def average_hw_grade(students, course):
    total = 0
    count = 0
    for student in students:
        for grade in student.grades.get(course, []):
            total += grade
            count += 1
    return total / count if count else 0


def average_lecture_grade(lecturers, course):
    total = 0
    count = 0
    for lecturer in lecturers:
        for grade in lecturer.grades.get(course, []):
            total += grade
            count += 1
    return total / count if count else 0


if __name__ == '__main__':
    # Задание 1 — проверка наследования
    lecturer = Lecturer('Some', 'Buddy')
    reviewer = Reviewer('Some', 'Buddy')
    print(isinstance(lecturer, Mentor))   # True
    print(isinstance(reviewer, Mentor))   # True
    print(lecturer.courses_attached)      # []
    print(reviewer.courses_attached)      # []

    # Задание 2 — атрибуты и взаимодействие классов
    student = Student('Ruoy', 'Eman', 'Ж')
    student.courses_in_progress += ['Python', 'Java']
    lecturer.courses_attached += ['Python', 'C++']
    reviewer.courses_attached += ['Python', 'C++']

    print(student.rate_lecture(lecturer, 'Python', 7))   # None
    print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
    print(student.rate_lecture(lecturer, 'С++', 8))      # Ошибка
    print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка
    print(lecturer.grades)                               # {'Python': [7]}

    # Задание 4 — полевые испытания
    lecturer_2 = Lecturer('Anna', 'Petrova')
    reviewer_2 = Reviewer('Ivan', 'Ivanov')
    student_2 = Student('Kate', 'Sidorova', 'Ж')

    student_2.courses_in_progress += ['Python']
    student_2.finished_courses += ['Введение в программирование']
    lecturer_2.courses_attached += ['Python']
    reviewer_2.courses_attached += ['Python']

    reviewer.rate_hw(student, 'Python', 10)
    reviewer.rate_hw(student, 'Python', 8)
    reviewer_2.rate_hw(student_2, 'Python', 9)
    reviewer_2.rate_hw(student_2, 'Python', 7)

    student.rate_lecture(lecturer, 'Python', 10)
    student_2.rate_lecture(lecturer_2, 'Python', 9)

    print('\n', lecturer, sep='')
    print('\n', lecturer_2, sep='')
    print('\n', reviewer, sep='')
    print('\n', reviewer_2, sep='')
    print('\n', student, sep='')
    print('\n', student_2, sep='')

    print('\nstudent > student_2:', student > student_2)
    print('lecturer > lecturer_2:', lecturer > lecturer_2)

    print('\nСредняя оценка за ДЗ по курсу Python:',
          average_hw_grade([student, student_2], 'Python'))
    print('Средняя оценка за лекции по курсу Python:',
          average_lecture_grade([lecturer, lecturer_2], 'Python'))
