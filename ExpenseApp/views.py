from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
import datetime
# Create your views here.

categories = [{'miscellaneous': 'Miscellaneous', 'food': 'Food', 'shoes': 'Shoes', 'wears': 'Wears'}]



def index(request):

    expense = None

    if request.GET.get('edit_id'):
        expense= get_object_or_404(Expense, id = int(request.GET['edit_id']))

    if request.method == 'POST':
        name = request.POST['expense_name']
        amount = request.POST['expense_amount']
        category = request.POST['expense_category']

        if request.GET.get('edit_id'):
            expense= get_object_or_404(Expense, id = int(request.GET['edit_id']))
            expense.amount = request.POST.get('expense_amount')
            expense.category = request.POST.get('expense_category')
            expense.name = request.POST.get('expense_name')

            expense.save()
            messages.success(request, 'Expense record updated successfully.')
            return redirect('/')
        
        Expense.objects.create(name = name, amount= amount, category = category)
        messages.success(request, 'New Expense Record Added.')
        return redirect('/')
    
    expenses = Expense.objects.all()
    expense_total = Expense.objects.all().aggregate(expense_total= Sum('amount'))
    
    daays = datetime.datetime.today()

    last_7_days = Expense.objects.filter(created_date__gte = str(daays - datetime.timedelta(days= 7))).all().aggregate(total_7_days = Sum('amount'))
    last_30_days = Expense.objects.filter(created_date__gte = str(daays - datetime.timedelta(days= 30))).all().aggregate(total_30_days = Sum('amount'))
    last_52_weeks = Expense.objects.filter(created_date__gte = str(daays - datetime.timedelta(weeks= 52))).all().aggregate(total_52_weeks = Sum('amount'))
    context = {'expenses': expenses, 'total': expense_total, 'last_7_days': last_7_days, 'last_30_days': last_30_days, 
               'last_52_weeks': last_52_weeks, 'categories': categories, 'expense': expense}

    return render(request, 'index.html', context)


def delete(request, id):

    expense = get_object_or_404(Expense, id = id)
    expense.delete()
    messages.success(request, 'Expense record deleted successfully.')
    return redirect('/')

