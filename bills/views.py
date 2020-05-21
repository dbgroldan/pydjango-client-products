from django.shortcuts import render
import json
import jwt
import csv
import datetime as dt

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from rest_framework.decorators import api_view
from django.db import connection
from bills.models import Bill
from bills.serializers import BillSerializer
from django.contrib.auth.hashers import make_password
secret = 'developedbydbgroldan'

@api_view(['GET'])
def generateReport(request, doc):
    cookies = request.COOKIES['token']
    if cookies:
        info_token = jwt.decode(cookies, secret, algorithms=['HS256'])
        name = info_token.get('first_name')
        lastname = info_token.get('last_name')
        time_token= info_token.get('actual_time')
        exact_time = dt.datetime.now()
        actual_time = str(dt.date.today()) + str(exact_time.hour)

        cursor = connection.cursor()
        query = "SELECT * FROM clients_client WHERE document = '" + doc + "';"
        cursor.execute(query)
        clients = cursor.fetchall()
        columns = ("document", "first_name", "last_name", "email", "password")
        res = dict(zip(columns, clients[-1]))
        if (res.get('first_name') == name and res.get('last_name') == last_name) and actual_time == time_token:
            # cursorbills = connection.cursor()
            # querybills = "SELECT * FROM bills_bill WHERE client_id_id = '" + doc + "';"
            # cursorbills.execute(querybills)
            # bills = cursorbills.fetchall()
            # count_b = 0
            # columns_b = ("id", "company_name", "nit", "code", "create_at", "client_id_id")
            # columns_pr = ("id", "name", "description", "avalible")
            # for b in bills:
            #     res_bills = dict(zip(columns_b, b))
            #
            #     query_prod = """ SELECT * FROM products_product prd WHERE prd.id =
            #                 (SELECT pb.product_id FROM products_product_bills as pb
            #                 WHERE pb.bill_id = '""" + res_bills.get('id') + "');"
            #     cursorprod = connection.cursor()
            #     cursorprod.execute(query_prod)
            #     prods = cursorprod.fetchall()
            #     count_pr = 0
            #     for pr in prods:
            #         res_prod = dict(zip(columns_pr, pr))
            #         res_bills['product_'+str(count_pr)] = res_prod
            #         count_pr += 1
            #
            #     res['bill_'+str(count_b)] = res_bills
            #     count_b +=1
            query_joins = "SELECT * FROM bills_bill LEFT JOIN clients_client cc on bills_bill.client_id_id = '"
            query_joins+= res.get(document) + """'
                            LEFT JOIN products_product_bills pb ON pb.bill_id = bills_bill.id
                            LEFT JOIN  products_product pp on pb.product_id = pp.id;"""
            cursorjoins = connection.cursor()
            cursorjoins.execute(query_joins)
            final_data = cursor.fetchall()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'
            writer = csv.writer(response)
            for data in final_data:
                writer.writerow(data)
            return response
    return JsonResponse({"code":403, "message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
