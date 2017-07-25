from __future__ import unicode_literals

from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def validatedRegistration(self, form_data):
		errors = []

		if len(form_data['first_name']) == 0:
			errors.append("First name is required")
		if len(form_data['last_name']) == 0:
			errors.append("Last name is required")
		if len(form_data['email']) == 0:
			errors.append("Email is required")
		if len(form_data['password']) < 8:
			errors.append("Password must be at least 8 characters")
		if form_data['password'] != form_data['password_confirm']:
			errors.append("Passwords do not match!")

		return errors

	def validateLogin(self, form_data):
		errors = []

		if len(form_data['email']) == 0:
			errors.append("Email is required")
		if len(form_data['password']) == 0:
			errors.append("Password is required")

		return errors

	def createUser(self, form_data):
		password = str(form_data['password'])
		hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
		user = User.objects.create(
				first_name = form_data['first_name'],
				last_name = form_data['last_name'],
				email = form_data['email'],
				password = hashed_pw
			)

		return user

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class TravelManager(models.Manager):
	def validateTravel(self, form_data):
		errors = []

		if len(form_data['destination']) == 0:
			errors.append("You must enter a destination")
		if len(form_data['plan']) == 0:
			errors.append("You must enter a plan")
		if len(form_data['start_date']) == 0:
			errors.append("Start date cannot be blank!")
		if len(form_data['end_date']) == 0:
			errors.append("End date cannot be blank")
		
		return errors

	def createTravel(self, form_data, user):
		travel = Travel.objects.create(
				destination = form_data['destination'],
				start_date = form_data['start_date'],
				end_date = form_data['end_date'],
				plan = form_data['plan'],
				user = user
			)
		
		return travel

class Travel(models.Model):
	destination = models.CharField(max_length=255)
	start_date = models.DateTimeField()
	end_date = models.CharField(max_length=255)
	plan = models.TextField()
	user = models.ForeignKey(User, related_name='trips')
	joined_by = models.ManyToManyField(User, related_name="travelers")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = TravelManager()