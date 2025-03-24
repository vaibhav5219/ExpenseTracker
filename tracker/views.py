from django.shortcuts import render, redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def registration(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        firstname = request.POST.get('Firstname')
        lastname = request.POST.get('Lastname')
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        if User.objects.filter( Q(username=username) | Q(email=email)).exists():
            messages.error(request,"Username or Password Already exists!")
            return redirect('/register')
        
        user_obj = User.objects.create(
            username = username,
            first_name = firstname,
            last_name = lastname,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.info(request,"Accoount is created!")
        return redirect('/register')

    return render(request, "register.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            messages.error(request,"Username doesn't exists!")
            return redirect('/login')
        user_obj = authenticate(username=username, password=password)
        print(password)
        if user_obj:
            messages.info(request,"You have logged In!") 
            login(request=request, user=user_obj)
            return redirect('/')
        else:
            messages.error(request,"Invalid Cradientals!") 
    return render(request, "login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")

@login_required(login_url="/login")
def index(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        print('description => ',description)
        print("amount =>", amount, isinstance(amount, int), type(amount), amount.isdigit())

        if not description:
            messages.info(request,"Please add description")
            return redirect("/")

        # if not amount.isdigit(): # not isinstance(amount, int):
        try:
            amount = float(amount)
        except exception as e: # type: ignore
            messages.info(request, "Please enter amount")
            return redirect("/")

        Transaction.objects.create(
            description = description,
            amount = amount,
            user = request.user
        )
        return redirect('/')

    context = { 
        'transactions' : Transaction.objects.filter(user=request.user),
        'balance': Transaction.objects.filter(user=request.user).aggregate(total_balance = Sum('amount'))['total_balance'] or 0,
        'income': Transaction.objects.filter(user=request.user, amount__gte = 0).aggregate(income = Sum('amount'))['income'] or 0,
        'expense': Transaction.objects.filter(user=request.user, amount__lte = 0).aggregate(expense = Sum('amount'))['expense'] or 0,
    }

    return render(request, "index.html", context=context)

@login_required(login_url="/login")
def deleteTransaction(request,uid):
    Transaction.objects.get(uuid = uid).delete()
    return redirect('/')