from rest_framework import serializers

from .models import Student, Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"

    def validate_course_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Course name must be at least 3 characters long."
            )

        return value


class StudentSerializer(serializers.ModelSerializer):

    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        source="course",
        queryset=Course.objects.all(),
        write_only=True,
        required=True,
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "email",
            "age",
            "course",
            "course_id",
            "enrollment_date",
            "phone_number",
            "address",
        ]

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Name must be at least 3 characters long."
            )

        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "Name should only contain letters and spaces."
            )

        return value

    def validate_age(self, value):
        if value < 18 or value > 60:
            raise serializers.ValidationError(
                "Age must be between 18 and 60 years."
            )

        return value

    def validate_email(self, value):
        if not (
            value.endswith(".edu")
            or value.endswith(".ac.in")
            or value.endswith(".edu.in")
        ):
            raise serializers.ValidationError(
                "Email must be an educational domain ending with .edu, .ac.in, or .edu.in."
            )

        return value

    def validate_phone_number(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError(
                    "Phone number should contain only digits."
                )

            if len(value) != 10:
                raise serializers.ValidationError(
                    "Phone number must be exactly 10 digits."
                )

        return value

    def validate(self, data):
        course = data.get("course")
        age = data.get("age")

        if course is not None and age is not None:
            if course.course_name == "Computer Science" and age < 20:
                raise serializers.ValidationError(
                    "Computer Science students must be at least 20 years old."
                )

            if course.course_name == "Data Science" and age < 22:
                raise serializers.ValidationError(
                    "Data Science students must be at least 22 years old."
                )

        return data


class CourseDetailSerializer(serializers.ModelSerializer):

    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "course_name",
            "course_code",
            "students"
        ]