import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Master_Operation_Category, MasProcess

def Process_Master(request):

    if request.method == 'GET':

        id = request.GET.get('process_id')
        des = request.GET.get('process_des')
        mc = request.GET.get('mc')
        
        queryset = MasProcess.objects.using('main').all()

        if id:
            queryset = queryset.filter(process_id=id)

        if des:
            queryset = queryset.filter(process_des__icontains=des)

        if mc:
            queryset = queryset.filter(mc__icontains=mc)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

@csrf_exempt
def Operation_Category(request):

    if request.method == 'GET':

        id = request.GET.get('id')
        queryset = Master_Operation_Category.objects.all()

        if id:
            queryset = queryset.filter(id=id)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        for key in data:

            exists = (
                Master_Operation_Category.objects
                .filter(
                    category_type = key['category_type'],
                    operations = key['operations'],
                    machine_name = key['machine_name']
                )
                .exists()
            )

            if exists:
                return JsonResponse({"message": "Records already exist"}, status=400)

            if not exists:
                Master_Operation_Category.objects.create(
                    category_type = key['category_type'],
                    operations = key['operations'],
                    machine_name = key['machine_name']
                )

        return JsonResponse({"message": "Records created"}, status=201)

    elif request.method == 'PUT':

        data = json.loads(request.body)

        for key in data:

            Master_Operation_Category.objects.filter(
                id=key['id']
                ).update(
                    category_type = key['category_type'],
                    operations = key['operations'],
                    machine_name = key['machine_name']
                )

        return JsonResponse({"message": "Records updated"}, status=200)