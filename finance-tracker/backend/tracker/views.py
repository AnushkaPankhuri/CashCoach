from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Transaction, Budget, UserSettings
import pandas as pd
from datetime import datetime, timedelta
from django.db.models import Sum


def dashboard(request):
    transactions = Transaction.objects.all().order_by('-date')[:50]
    budget = Budget.objects.first() if Budget.objects.exists() else None
    
   
    spending_data = {}
    if transactions.exists():
        df = pd.DataFrame.from_records(transactions.values('category', 'amount'))
        spending_data = df.groupby('category')['amount'].sum().to_dict()
    
   
    insights = {
        'monthly_total': Transaction.objects.filter(
            date__month=datetime.now().month
        ).aggregate(Sum('amount'))['amount__sum'] or 0,
        'weekly_total': Transaction.objects.filter(
            date__gte=datetime.now() - timedelta(days=7)
        ).aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    
    return render(request, 'index.html', {
        'transactions': transactions,
        'budget': budget,
        'spending_data': spending_data,
        'insights': insights,
    })


class UploadCSVView(View):
    def post(self, request):
        if 'csv_file' not in request.FILES:
            messages.error(request, "No file selected!")
            return redirect('dashboard')
        
        try:
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)
            
          
            required_cols = {'date', 'amount', 'description', 'category'}
            if not required_cols.issubset(df.columns):
                missing = required_cols - set(df.columns)
                messages.error(request, f"Missing columns: {', '.join(missing)}")
                return redirect('dashboard')
            
           
            transactions_created = 0
            for _, row in df.iterrows():
                Transaction.objects.create(
                    date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                    amount=float(row['amount']),
                    description=row['description'],
                    category=row['category']
                )
                transactions_created += 1
            
            messages.success(request, f"Imported {transactions_created} transactions!")
            return redirect('dashboard')
        
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('dashboard')


class BudgetView(View):
    def post(self, request):
        amount = request.POST.get('budget_amount')
        if not amount:
            messages.error(request, "Budget amount is required!")
            return redirect('dashboard')
        
        try:
            budget, _ = Budget.objects.update_or_create(
                id=1, 
                defaults={'amount': float(amount)}
            )
            messages.success(request, "Budget updated!")
        except ValueError:
            messages.error(request, "Invalid amount format!")
        
        return redirect('dashboard')


def filter_transactions(request):
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    transactions = Transaction.objects.all()
    
    if category:
        transactions = transactions.filter(category=category)
    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])
    
    return render(request, 'partials/transactions_table.html', {
        'transactions': transactions
    })


def generate_insights(user):
    total_spent = Transaction.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    user_settings = UserSettings.objects.get(user=user)
    
    if total_spent > user_settings.budget_threshold:
        return f"⚠️ Exceeded budget by ₹{total_spent - user_settings.budget_threshold}"
    else:
        return f"✅ Within budget (₹{user_settings.budget_threshold - total_spent} remaining)"