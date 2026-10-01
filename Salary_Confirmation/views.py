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
        
        # If frontend sends a single dictionary object, wrap it in a list
        if isinstance(data, dict):
            data = [data]

        for item in data:
            exists = Master_Operation_Category.objects.filter(
                category_type=item['category_type'],
                operations=item['operations'],
                machine_name=item['machine_name']
            ).exists()

            if exists:
                return JsonResponse({"message": "Records already exist"}, status=400)

            Master_Operation_Category.objects.create(
                category_type=item['category_type'],
                operations=item['operations'],
                machine_name=item['machine_name']
            )

        return JsonResponse({"message": "Records created"}, status=201)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        
        if isinstance(data, dict):
            data = [data]

        for item in data:
            item_id = item.get('id')
            
            # If ID isn't in the payload, extract it from the URL (e.g., /operations/5/)
            if not item_id:
                path_parts = request.path.strip('/').split('/')
                if path_parts[-1].isdigit():
                    item_id = int(path_parts[-1])

            if item_id:
                Master_Operation_Category.objects.filter(id=item_id).update(
                    category_type=item.get('category_type'),
                    operations=item.get('operations'),
                    machine_name=item.get('machine_name')
                )

        return JsonResponse({"message": "Records updated"}, status=200)