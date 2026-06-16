from django.shortcuts import render
from .models import TxNotification,TmpPrdprn
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os


def ws_attendance(request):
    if request.method == 'GET':
        data = TxNotification.objects.using('mssql1').exclude(wunit='Service')

        return JsonResponse({
            'status': 'success',
            'data': list(data.values())
        })

    return JsonResponse({
        'status': 'error',
        'message': 'check views.py function ws_attandence'
    }, status=405)


def liveprdn(request):

    data = TmpPrdprn.objects.using('demo').all()

    print("Total records in TmpPrdprn:", data.count())  # Debug: Check total records

    response_data = []

    for rec in data:    
        response_data.append({
            "unit": rec.unit,
            "jobno": rec.jobno,
            "tb": rec.tb,
            "color": rec.clr,
            "ordqty": rec.ordqty,
            "cutqtyqty": rec.cutqtyqty,
            "allotqty": rec.allotqty,
            "bc": rec.bc,
            "oth": rec.oth,
            "sew": rec.sew,
            "singer": rec.singer,
            "che": rec.che,
            "fc": rec.fc,
            "irn": rec.irn,
            "pack": rec.pack,
            "mist": rec.mist,
            "rejqty": rec.rejqty,
        })

    return JsonResponse(response_data, safe=False)
