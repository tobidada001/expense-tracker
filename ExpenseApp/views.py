from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.contrib import messages
from django.db.models import Sum
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.

categories = ["Miscellaneous", "Food", "Shoes", "Wears", "Tax", 'Bills']

@login_required(login_url = '/login')
def index(request):
    expense = None

    if request.GET.get('edit_id'):
        expense= get_object_or_404(Expense, id = int(request.GET['edit_id']), owner = request.user)

    if request.method == 'POST':
        name = request.POST['expense_name']
        amount = request.POST['expense_amount']
        category = request.POST['expense_category']


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


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        auth = authenticate(request, username= request.POST['username'], password = request.POST['password1'])
        if auth:
            login(request, auth)
            return redirect('/')
        else:
            messages.error(request, 'Could not login.')
            return redirect('/new-user')
        
    return render(request, 'signin.html')



def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        if not request.POST['password1'] == request.POST['password2']:
            messages.error(request, 'Your passwords don\t match')
            return redirect('new-user')
        
        user = User.objects.create(first_name = request.POST['firstname'], last_name = request.POST['lastname'], username= request.POST['username'])
        user.set_password(request.POST['password1'])
        user.save()
        messages.success(request, 'Your account has been created successfully.')

        auth = authenticate(request=request, username= request.POST['username'], password = request.POST['password1'])

        if auth:
            login(request, auth)
            return redirect(to='/')
        else:
            messages.error(request, 'Could not login you in.')
            return redirect(request.path)
        
    return render(request, 'signup.html')


def logoutuser(request):
    logout(request)
    return redirect('loginuser')
