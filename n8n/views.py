from django.shortcuts import render
from .models import TxNotification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os


def ws_attendance(request):
    if request.method == 'GET':
        data = TxNotification.objects.using('mssql1').all()

        return JsonResponse({
            'status': 'success',
            'data': list(data.values())
        })

    return JsonResponse({
        'status': 'error',
        'message': 'check views.py function ws_attandence'
    }, status=405)
