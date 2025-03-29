from django.shortcuts import render

# Create your views here.

import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction, Insight, UserSettings
from .serializers import TransactionSerializer
from django.db import transaction as db_transaction


from rest_framework.decorators import api_view
from django.db.models import Sum
from datetime import datetime, timedelta


import pathway as pw
import pandas as pd

from django.shortcuts import render, redirect

from django.contrib.auth.models import User

# class UploadCSV(APIView):
#     def post(self, request, format=None):
#         csv_file = request.FILES.get('file')
#         if not csv_file.name.endswith('.csv'):
#             return Response({"error": "File must be a CSV."}, status=400)

#         data_set = csv_file.read().decode('UTF-8')
#         io_string = io.StringIO(data_set)

#         next(io_string) 
#         with db_transaction.atomic():
#             for row in csv.reader(io_string, delimiter=','):
#                 Transaction.objects.create(
#                     date=row[0],
#                     description=row[1],
#                     category=row[2],
#                     amount=float(row[3])
#                 )
#         return Response({"message": "CSV Uploaded Successfully."}, status=201)

def dashboard(request):
    transactions = Transaction.objects.all()
    return render(request, 'index.html', {'transactions': transactions})

 
class UploadCSV(APIView):
    def post(self, request, format=None):
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "File must be a CSV."}, status=400)

      
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        
        next(io_string)  
        with db_transaction.atomic():
            for row in csv.reader(io_string, delimiter=','):
                Transaction.objects.create(
                    date=row[0],
                    description=row[1],
                    category=row[2],
                    amount=float(row[3])
                )

        
        transactions = Transaction.objects.all()

       
        self.generate_insights_and_store(transactions, request.user)

        
        self.process_data_to_vector_store(transactions)

        return Response({"message": "CSV Uploaded and Processed Successfully."}, status=201)





@api_view(['GET'])
def all_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def filter_transactions(request):
    category = request.GET.get('category')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    transactions = Transaction.objects.all()

    if category:
        transactions = transactions.filter(category=category)
    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def summary(request):
    today = datetime.today()
    start_of_month = today.replace(day=1)
    last_7_days = today - timedelta(days=7)

    monthly_total = Transaction.objects.filter(date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    weekly_total = Transaction.objects.filter(date__gte=last_7_days).aggregate(Sum('amount'))['amount__sum'] or 0

    return Response({
        "monthly_total": monthly_total,
        "weekly_total": weekly_total
    })


def parse_csv(file):
    df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    return df

def save_transactions_from_csv(file):
    df = parse_csv(file)
    for _, row in df.iterrows():
        txn = Transaction(
            date=row['date'],
            description=row['description'],
            category=row['category'],
            amount=row['amount']
        )
        txn.save()

def process_data_to_vector_store(transactions):
    data = []
    for txn in transactions:
        data.append({
            "description": txn.description,
            "category": txn.category,
            "amount": txn.amount,
        })
    store = pw.vector_store('transactions')
    store.add(data)        




def generate_insights_and_store(transaction_data, user):
    total_spent = sum(txn.amount for txn in transaction_data)

    user_settings = UserSettings.objects.get(user=user)
    budget_threshold = user_settings.budget_threshold

   
    if total_spent > budget_threshold:
        spending_pattern = f"You have exceeded your budget by ₹{total_spent - budget_threshold}."
    else:
        spending_pattern = f"You are within your budget by ₹{budget_threshold - total_spent}."

    insight = Insight(
        total_spent=total_spent,
        spending_pattern=spending_pattern
    )
    insight.save()
    return insight


@api_view(['GET'])
def get_insights(request):
    insights = Insight.objects.last()  
    response_data = {
        "total_spent": insights.total_spent,
        "spending_pattern": insights.spending_pattern
    }
    return Response(response_data)



@api_view(['POST'])
def set_budget_threshold(request):
    user = request.user  
    threshold = request.data.get('threshold')
    
   
    user_settings, created = UserSettings.objects.get_or_create(user=user)
    user_settings.budget_threshold = threshold
    user_settings.save()

    return Response({"message": "Threshold saved successfully!"})
