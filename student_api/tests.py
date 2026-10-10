from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Student


class StudentApiTests(APITestCase):
	def setUp(self):
		self.course = Course.objects.create(
			course_name="Computer Science",
			course_code="CS101",
			description="Computer science fundamentals",
			duration_months=48,
		)

	def test_welcome_endpoint(self):
		response = self.client.get("/api/students/welcome/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			response.data["message"],
			"Welcome to the Student Management API",
		)

	def test_create_student_returns_nested_course(self):
		response = self.client.post(
			"/api/students/create/",
			{
				"name": "Rahul Kumar",
				"email": "rahul@college.edu",
				"age": 20,
				"course_id": self.course.id,
				"phone_number": "9876543210",
				"address": "Main Road",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["student"]["course"]["course_code"], "CS101")

	def test_invalid_age_is_rejected(self):
		response = self.client.post(
			"/api/students/create/",
			{
				"name": "Rahul Kumar",
				"email": "rahul@college.edu",
				"age": 17,
				"course_id": self.course.id,
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("age", response.data)

	def test_patch_updates_only_submitted_fields(self):
		student = Student.objects.create(
			name="Rahul Kumar",
			email="rahul@college.edu",
			age=20,
			course=self.course,
		)

		response = self.client.patch(
			f"/api/students/{student.id}/update/",
			{"address": "Updated Address"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		student.refresh_from_db()
		self.assertEqual(student.address, "Updated Address")
		self.assertEqual(student.name, "Rahul Kumar")

	def test_course_code_double_underscore_query_endpoint(self):
		Student.objects.create(
			name="Rahul Kumar",
			email="rahul@college.edu",
			age=20,
			course=self.course,
		)

		response = self.client.get("/api/students/courses/CS101/students/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)

	def test_delete_returns_no_content(self):
		student = Student.objects.create(
			name="Rahul Kumar",
			email="rahul@college.edu",
			age=20,
			course=self.course,
		)

		response = self.client.delete(f"/api/students/{student.id}/delete/")

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Student.objects.filter(id=student.id).exists())
