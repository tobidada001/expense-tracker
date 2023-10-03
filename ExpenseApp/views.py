from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
import datetime
import json
# Create your views here.

categories = ["Miscellaneous", "Food", "Shoes", "Wears", "Tax", 'Bills']


def index(request):
    expense = None

    if request.GET.get('edit_id'):
        expense= get_object_or_404(Expense, id = int(request.GET['edit_id']), owner = request.user)

    if request.method == 'POST':
        name = request.POST['expense_name']
        amount = request.POST['expense_amount']
        category = request.POST['expense_category']

        if not request.user.is_authenticated:
            messages.error(request, 'You are not logged in!')
            return redirect('/')

        if category == "":
            messages.warning(request, 'No category selected')
            return redirect('/')

        if request.GET.get('edit_id'):
            expense= get_object_or_404(Expense, id = int(request.GET['edit_id']))
            expense.amount = request.POST.get('expense_amount')
            expense.category = request.POST.get('expense_category')
            expense.name = request.POST.get('expense_name')
            expense.owner = request.user

            expense.save()
            messages.success(request, 'Expense record updated successfully.')
            return redirect('/')
        
        Expense.objects.create(name = name, amount= amount, category = category, owner= request.user)
        messages.success(request, 'New Expense Record Added.')
        return redirect('/')
    
    expenses = Expense.objects.filter(owner = request.user)
    expense_total = expenses.aggregate(expense_total= Sum('amount'))
    
    daays = datetime.datetime.today()
    past_30_days_sum_expenses = expenses.values('created_date').annotate(sum= Sum('amount'))
    categorical_expenses = expenses.values('category').annotate(sum= Sum('amount'))
    
    last_7_days = expenses.filter(created_date__gte = str(daays - datetime.timedelta(days= 7))).aggregate(total_7_days = Sum('amount'))
    last_30_days = expenses.filter(created_date__gte = str(daays - datetime.timedelta(days= 30))).aggregate(total_30_days = Sum('amount'))
    last_52_weeks = expenses.filter(created_date__gte = str(daays - datetime.timedelta(weeks= 52))).aggregate(total_52_weeks = Sum('amount'))
    context = {'expenses': expenses, 'total': expense_total, 'last_7_days': last_7_days, 'last_30_days': last_30_days, 
    'last_52_weeks': last_52_weeks, 'categories': categories, 'expense': expense, 'past_30_days_sum_expenses': past_30_days_sum_expenses,  'categorical_expenses': categorical_expenses}
    
    return render(request, 'index.html', context)


def delete(request, id):

    expense = get_object_or_404(Expense, id = id, owner= request.user)
    expense.delete()
    messages.success(request, 'Expense record deleted successfully.')
    return redirect('/')

