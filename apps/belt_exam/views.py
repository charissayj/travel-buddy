from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from django.db.models import Count
from .models import User, Travel
import bcrypt
# Create your views here.
def flashErrors(request, errors):
	for error in errors:
		messages.error(request, error)

def currentUser(request):
	id = request.session['user_id']

	return User.objects.get(id=id)

def index(request):

	return render(request, "belt_exam/index.html")

def travels(request):
	if 'user_id' in request.session:
		current_user = currentUser(request)
		travels = Travel.objects.all().order_by('-created_at')

		context = {
			'current_user': current_user,
			'travels': travels
		}

		return render(request, "belt_exam/travels.html", context)

	return redirect(reverse('index'))

def add_plan(request):

	return render(request, "belt_exam/add_plan.html")

def add_trip(request):
	if request.method == "POST":
		errors = Travel.objects.validateTravel(request.POST)
		current_user = currentUser(request)

		if not errors:
			travel = Travel.objects.createTravel(request.POST, current_user)
			
			request.session['travel_id'] = travel.id

			return redirect(reverse('travels'))

		flashErrors(request, errors)
	
	return redirect(reverse('add_plan'))

def destination(request, id):
	travel = Travel.objects.get(id=id)
	current_user = currentUser(request)
	travelers = Travel.objects.all()
	context = {
		'travel': travel,
		'travelers': travelers,
	}
	return render(request, "belt_exam/destination.html", context)

def travelers(request, id):
	if request.method == "POST":
		if 'user_id' in request.session:
			current_user = currentUser(request)

			joined_by = Travel.objects.get(id=id)

			current_user.travelers.add(joined_by)

			return redirect(reverse('travels'))

def register(request):
	if request.method == "POST":
		errors = User.objects.validatedRegistration(request.POST)

		if not errors:
			user = User.objects.createUser(request.POST)

			request.session['user_id'] = user.id

			return redirect(reverse('travels'))

		flashErrors(request, errors) 

	return redirect(reverse('index'))

def login(request):
		
	if request.method == "POST":
		errors = User.objects.validateLogin(request.POST)

		if not errors:
			user = User.objects.filter(email=request.POST['email']).first()

			if user:
				password = str(request.POST['password'])
				user_password = str(user.password)

				hashed_pw = bcrypt.hashpw(password, user_password)

				if hashed_pw == user.password:
					request.session['user_id'] = user.id 

					return redirect(reverse('travels'))

				errors.append("Invalid account information")

		flashErrors(request, errors)
		return redirect(reverse('index'))

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')

	return redirect(reverse('index'))