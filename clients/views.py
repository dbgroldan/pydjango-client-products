from django.shortcuts import render
import json
import jwt
import datetime as dt

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password

from django.db import connection
from clients.models import Client
from clients.serializers import ClientSerializer

secret = 'developedbydbgroldan'

@api_view(['POST'])
def add_client(request):
    if request.method == 'POST':
        client_data = JSONParser().parse(request)
        client_serializer = ClientSerializer(data=client_data)
        if client_serializer.is_valid():
            # Generate query
            cursor = connection.cursor()
            query = 'INSERT INTO clients_client('
            data_spc_query = ''
            data_query = []
            attrbs_table = list(client_data.keys())
            for a in attrbs_table:
                if a != attrbs_table[-1]:
                    query += a + ', '
                    data_spc_query += '%s, '
                else:
                    query += a + ') VALUES('
                    data_spc_query += '%s);'
                if a != 'password':
                    data_query.append(client_data.get(a))
                else:
                    pwd = make_password(client_data.get(a))
                    data_query.append(pwd)
            query+= data_spc_query
            print(query)
            cursor.execute(query, tuple(data_query))
            connection.commit()
            return JsonResponse({"code":201, "message": "Client Added"}, status=status.HTTP_201_CREATED)
        return JsonResponse(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def login_client(request):
    response = HttpResponse('')
    if request.method == 'POST':
        client_data = JSONParser().parse(request)
        cursor = connection.cursor()
        query = "SELECT * FROM clients_client WHERE email = '" + client_data.get('email')+ "';"
        cursor.execute(query)
        clients = cursor.fetchall()
        columns = ("document", "first_name", "last_name", "email", "password")
        res = dict(zip(columns, clients[-1]))
        if check_password(client_data.get('password'), res.get('password')):
            exact_time = dt.datetime.now()
            info = {'name': res.get('first_name'), 'last_name': res.get('last_name'), 'actual_time': str(dt.date.today()) + str(exact_time.hour)}
            token = jwt.encode(info, secret, algorithm='HS256')
            response.set_cookie(key='token', value=str(token))
            return response
        return JsonResponse({"code":404, "message": "Client Not Found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def show_client(request, doc):
    cookies = request.COOKIES['token']
    if cookies:
        info_token = jwt.decode(token, secret, algorithms=['HS256'])
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
            return HttpResponse(json.dumps(res), content_type='application/json')
        return JsonResponse({"code":403, "message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse({"code":404, "message": "Client Not Found"}, status=status.HTTP_404_NOT_FOUND)
