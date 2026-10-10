from django.urls import path

from . import views


urlpatterns = [

    path("welcome/", views.welcome, name="welcome"),

    path("list/", views.list_students, name="list_students"),

    path("create/", views.create_student, name="create_student"),

    path("<int:pk>/", views.get_student, name="get_student"),

    path(
        "<int:pk>/update/",
        views.update_student,
        name="update_student"
    ),

    path(
        "<int:pk>/delete/",
        views.delete_student,
        name="delete_student"
    ),

    path(
        "with-courses/",
        views.students_with_courses,
        name="students_with_courses"
    ),

    path(
        "courses/",
        views.list_courses,
        name="list_courses"
    ),

    path(
        "courses/create/",
        views.create_course,
        name="create_course"
    ),

    path(
        "courses/<int:pk>/students/",
        views.course_detail_students,
        name="course_detail_students"
    ),

    path(
        "courses/<str:course_code>/students/",
        views.students_by_course_code,
        name="students_by_course_code"
    ),

]