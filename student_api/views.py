from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Student, Course
from .serializers import (
    StudentSerializer,
    CourseSerializer,
    CourseDetailSerializer
)


@api_view(["GET"])
def welcome(request):
    return Response(
        {"message": "Welcome to the Student Management API"},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def list_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
def create_student(request):
    serializer = StudentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message": "Student created successfully",
                "student": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
def get_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)

    except Student.DoesNotExist:
        return Response(
            {
                "error": "Student not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = StudentSerializer(student)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["PUT", "PATCH"])
def update_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)

    except Student.DoesNotExist:
        return Response(
            {
                "error": "Student not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = StudentSerializer(
        instance=student,
        data=request.data,
        partial=request.method == "PATCH",
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["DELETE"])
def delete_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)

    except Student.DoesNotExist:
        return Response(
            {
                "error": "Student not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    student.delete()

    return Response(
        {
            "message": "Student deleted successfully"
        },
        status=status.HTTP_204_NO_CONTENT
    )

@api_view(["POST"])
def create_course(request):

    serializer = CourseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            {
                "message": "Course created successfully",
                "course": serializer.data
            },
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )

@api_view(["GET"])
def students_with_courses(request):

    students = Student.objects.all()

    serializer = StudentSerializer(students, many=True)

    return Response(serializer.data, status=200)

@api_view(["GET"])
def list_courses(request):

    courses = Course.objects.all()

    serializer = CourseSerializer(courses, many=True)

    return Response(serializer.data, status=200)

@api_view(["GET"])
def course_detail_students(request, pk):

    course = get_object_or_404(Course, pk=pk)

    serializer = CourseDetailSerializer(course)

    return Response(serializer.data, status=200)

@api_view(["GET"])
def students_by_course_code(request, course_code):

    students = Student.objects.filter(
        course__course_code=course_code
    )

    serializer = StudentSerializer(students, many=True)

    return Response(serializer.data, status=200)