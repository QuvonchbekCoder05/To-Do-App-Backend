from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task, CustomUser

class TaskAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='password', email='test@example.com')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(title="Test Task", description="Test Description", user=self.user)

    def test_get_tasks(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        data = {'title': 'New Task', 'description': 'Task description'}
        response = self.client.post(reverse('task-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
