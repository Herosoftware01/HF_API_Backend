
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import VueAccPodetails, VueAccPodetails1, TrsGatemoduleInward

def po_details(request):
    companyid = request.GET.get('companyid')
    year = request.GET.get('year')
    no = request.GET.get('no')

    purchase = VueAccPodetails.objects.using('test').all()
    taxdetails = VueAccPodetails1.objects.using('test').all()

    if companyid:
        purchase = purchase.filter(companyid=companyid)
        taxdetails = taxdetails.filter(companyid=companyid)

    if year:
        purchase = purchase.filter(year=year)
        taxdetails = taxdetails.filter(year=year)

    if no:
        purchase = purchase.filter(no=no)
        taxdetails = taxdetails.filter(no=no)

    data = {
        "podetails": list(purchase.values()),
        "taxdetails": list(taxdetails.values()),
    }

    return JsonResponse(data, safe=False)

@csrf_exempt
def GatemoduleInward(request):

    if request.method == 'GET':

        qr = request.GET.get('qr')
        queryset = TrsGatemoduleInward.objects.using('demo').all()

        if qr:
            queryset = queryset.filter(qr=qr)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)
        id = data.get('qr')

        exists = (
            TrsGatemoduleInward.objects.using('demo')
            .filter(qr=id).exists()
        )

        if exists:
            return JsonResponse(
                {'message': 'Record already exists.'},
                status=400
            )

        if not exists:

            TrsGatemoduleInward.objects.using('demo').create(
                module=data.get('module'),
                qr=id,
                companyid=data.get('companyid'),
                year=data.get('year'),
                no=data.get('no'),
                date=data.get('date'),
                jobno=data.get('jobno'),
                suppliername=data.get('suppliername'),
                descr=data.get('descr'),
                rls_bdls=data.get('rls_bdls'),
                kg=data.get('kg'),
                mtrs=data.get('mtrs'),
                verify=data.get('verify'),
                prepered=data.get('prepered'),
                fhero=data.get('fhero')
            )
            return JsonResponse(
                {'message': 'Record created successfully.'}, 
                status=201
            )

