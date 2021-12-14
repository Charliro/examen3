from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from datetime import date
from .models import User, Appointment
import bcrypt
import datetime
import time 

# Create your views here.


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method =="POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            user_exist = User.objects.filter(email = request.POST.get('email'))
            if user_exist:
                messages.error(request,'Email ya registrado', extra_tags = 'mal_dato_login_e')
                return redirect("/")
            else:
                

                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                user = User.objects.create(
                    name = request.POST['name'],
                    email= request.POST['email'],
                    password = pw_hash,
                    )
                request.session['user_id'] = user.id
                return redirect('/')
    return redirect("/")

def login(request):

    if request.method =="POST":

        user_email = User.objects.filter(email = request.POST['email'])
        if user_email:
            user = user_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['id'] = user.id
                return redirect("/appoint")
        messages.error(request, "Email or Password are incorrect")
    return redirect("/")


def appoint(request):
    if 'id' not in request.session:
        return redirect ("/")
    
    
    appointments= Appointment.objects.filter(user__id=request.session['id'])
    user= User.objects.get(id=request.session['id'])
   
    
   
    context = {
        "user": user,
        "appointments": appointments,
        # "past_appoint":  Appointment.objects.filter(user__id = request.session['id']).filter(date = Previous_Date)
    }
    return render(request, 'appointment.html', context)

def toadd(request):
    return render(request, 'add.html')



def update(request, appoint_id):
    try:
        appointment= Appointment.objects.get(id=appoint_id)
    except Appointment.DoesNotExist:
        messages.info(request,"appointment Not Found")
        return redirect('/appoint')

    context={
        "appointment": appointment,
        # "others": User.objects.filter(joiner__id=appoint.id).exclude(id=appoint.creator.id),
    }
    return render(request, 'updatetime.html', context)

def edit_appoint(request, appoint_id):
    if 'id' not in request.session:
        return redirect ('/')
    if request.method != 'POST':
        messages.info(request, "Cannot edit like this!")
        return redirect('/update'+ appoint_id)

    try:
        print("/"*50)
        update_app = Appointment.objects.edit_appointment(request.POST, appoint_id)
        print("got to edit_appoint Try")
    except Appointment.DoesNotExist:
        messages.info(request,"appointment Not Found")
        return redirect('/update/'+appoint_id)
    if update_app[0]==False:
        messages.info(request, "Please fill in all the spaces and make sure it's valid!")
        return redirect('/update/'+appoint_id)
    else:
        messages.success(request, "successfuly updated information")
        return redirect('/appoint')

def add(request):
    if request.method != "POST":
        messages.error(request,"Can't add like that!")
        return redirect('/toadd')
    else:
        add_appoint= Appointment.objects.appointval(request.POST, request.session['id'])
        if add_appoint[0] == False:
            for each in add_appoint[1]:
                messages.error(request, each) #for each error in the list, make a message for each one.
            return redirect('/toadd')
        if add_appoint[0] == True:
            messages.success(request, 'Appointment Successfully Added')
            return redirect('/appoint')
#
def delete(request, appoint_id):
    try:
        target= Appointment.objects.get(id=appoint_id)
    except Appointment.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/appoint')
    target.delete()
    return redirect('/appoint')
# #

def logout(request):
    if 'id' not in request.session:
        return redirect('/')
    print("*******")
    print(request.session['id'])
    del request.session['id']
    return redirect('/')