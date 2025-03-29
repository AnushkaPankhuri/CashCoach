from django.shortcuts import render

# Create your views here.

import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer
from django.db import transaction as db_transaction

class UploadCSV(APIView):
    def post(self, request, format=None):
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            return Response({"error": "File must be a CSV."}, status=400)

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)

        next(io_string)  # Skip header
        with db_transaction.atomic():
            for row in csv.reader(io_string, delimiter=','):
                Transaction.objects.create(
                    date=row[0],
                    description=row[1],
                    category=row[2],
                    amount=float(row[3])
                )
        return Response({"message": "CSV Uploaded Successfully."}, status=201)