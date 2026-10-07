
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import VueAccPodetails, VueAccPodetails1

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