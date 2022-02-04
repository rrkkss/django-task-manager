from django.test import TestCase

# Create your tests here.

from .models import Task
from django.contrib.auth.models import User

class ClassNameTest(TestCase):
    @classmethod
    def setUpClass(self):
        Task.objects.create(user=User, name="ukol #1", description="popis #2", finished=False)
        Task.objects.create(user=User, name="ukol #2", description="", finished=True)
        Task.objects.create(user=User, name="", description="popis #3", finished=False)

    def test_add_task(self):
        task1 = Task.objects.get(name="ukol #1")
        task2 = Task.objects.get(name="ukol #2")
        task3 = Task.objects.get(name="")

        self.assertEqual(task1.speak(), 'úkol 1 prošel')
        self.assertEqual(task2.speak(), 'úkol 2 prošel')
        self.assertEqual(task3.speak(), 'úkol 3 prošel')