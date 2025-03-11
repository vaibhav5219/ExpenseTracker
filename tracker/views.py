from django.shortcuts import render, redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Sum

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
        except exception as e:
            messages.info(request, "Please enter amount")
            return redirect("/")

        Transaction.objects.create(
            description = description,
            amount = amount
        )
        return redirect('/')

    context = { 
        'transactions' : Transaction.objects.all(),
        'balance': Transaction.objects.all().aggregate(total_balance = Sum('amount'))['total_balance'] or 0,
        'income': Transaction.objects.filter(amount__gte = 0).aggregate(income = Sum('amount'))['income'] or 0,
        'expense': Transaction.objects.filter(amount__lte = 0).aggregate(expense = Sum('amount'))['expense'] or 0,
    }

    return render(request, "index.html", context=context)

def deleteTransaction(request,uid):
    Transaction.objects.get(uuid = uid).delete()
    return redirect('/')