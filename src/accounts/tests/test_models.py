from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from accounts.models import CustomUser, Friends, Interests, UserProfile

"""
class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
"""

class Test_CustomUser_Creation(TestCase):

	def setUp(self):
		pass

	def test_user_is_created(self):
		user = CustomUser.objects.create_user(email='abc@email.com',password='Password123')
		user.save()
		try:
			data = CustomUser.objects.get(email='abc@email.com')
			flag=True
		except ObjectDoesNotExist:
			flag=False
		self.assertTrue(flag,msg='User was not created')

	def test_superuser_is_created(self):
		user = CustomUser.objects.create_superuser(email='abc@email.com',password='Password123')
		user.save()
		try:
			data = CustomUser.objects.get(email='abc@email.com')
			flag=True
		except ObjectDoesNotExist:
			flag=False
		self.assertTrue(flag,msg='Superuser was not created')

		try:
			user = CustomUser.objects.create_superuser(email='abc@email.com')
			user.save()
			flag = False
		except:
			flag= True
		self.assertTrue(flag,msg="Superuser created without password")

class Test_CustomUser_Data(TestCase):

	@classmethod
	def setUpTestData(cls):
		user = CustomUser.objects.create_user(email='abc@email.com',password='Password123',
										first_name = 'abc', middle_name = 'optional', last_name = 'last',
										username = 'abc123')
		user.save()

	def test_email_taken(self):
		try:
			user = CustomUser.objects.create_user(email='abc@email.com',password='Password123')
			user.save()
			flag=False
		except:
			flag=True
		self.assertTrue(flag,msg='Object created with duplicate email')

	def test_username_taken(self):
		try:
			user = CustomUser.objects.create_user(email='def@email.com',password='Password123',username='abc123')
			user.save()
			flag=False
		except:
			flag=True
		self.assertTrue(flag,msg='Object created with duplicate username')

	def test_get_absolute_url(self):
		user = CustomUser.objects.get(email='abc@email.com')
		field = user.get_absolute_url()
		self.assertEqual(field,'accounts/abc%40email.com/',msg='Incorrect absolute url')

	def test_full_name(self):
		user = CustomUser.objects.get(email='abc@email.com')
		field = user.get_full_name()
		self.assertEqual(field,'abc last',msg='Incorrect full name')

	def test_short_name(self):
		user = CustomUser.objects.get(email='abc@email.com')
		field = user.get_short_name()
		self.assertEqual(field,'abc',msg='Incorrect short name')