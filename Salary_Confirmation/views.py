import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Machine_category_master, Operation_Category_master

# -------------------------------------------------------------
# Machine Category Views
# -------------------------------------------------------------

@csrf_exempt
def machine_category_api(request, id=None):
    # ------------------ SINGLE RECORD OPERATIONS (GET, PUT, DELETE) ------------------
    if id:
        try:
            machine = Machine_category_master.objects.get(id=id)
        except Machine_category_master.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Machine category not found'}, status=404)

        # GET: Retrieve a single machine category
        if request.method == 'GET':
            data = {
                'id': machine.id,
                'machine_name': machine.machine_name,
                'create_at': machine.create_at,
                'updated_at': machine.updated_at
            }
            return JsonResponse({'status': 'success', 'data': data}, status=200)

        # PUT: Update an existing machine category
        elif request.method == 'PUT':
            try:
                body = json.loads(request.body)
                machine_name = body.get('machine_name', '').strip()

                if not machine_name:
                    return JsonResponse({'status': 'error', 'message': 'machine_name is required'}, status=400)

                # Check for existing record (case-insensitive) excluding the current one
                if Machine_category_master.objects.filter(machine_name__iexact=machine_name).exclude(id=id).exists():
                    return JsonResponse(
                        {'status': 'error', 'message': f"Machine '{machine_name}' already exists."}, 
                        status=409
                    )

                machine.machine_name = machine_name
                machine.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Machine category updated successfully.',
                    'data': {'id': machine.id, 'machine_name': machine.machine_name}
                }, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

        # DELETE: Remove a machine category
        elif request.method == 'DELETE':
            machine.delete()
            return JsonResponse({'status': 'success', 'message': 'Machine category deleted successfully.'}, status=200)

    # ------------------ BULK/CREATION OPERATIONS (GET ALL, POST) ------------------
    else:
        # GET: Retrieve all machine categories
        if request.method == 'GET':
            categories = list(
                Machine_category_master.objects.values('id', 'machine_name', 'create_at', 'updated_at')
            )
            return JsonResponse({'status': 'success', 'data': categories}, status=200)

        # POST: Create a new machine category
        elif request.method == 'POST':
            try:
                body = json.loads(request.body)
                machine_name = body.get('machine_name', '').strip()

                if not machine_name:
                    return JsonResponse({'status': 'error', 'message': 'machine_name is required'}, status=400)

                if Machine_category_master.objects.filter(machine_name__iexact=machine_name).exists():
                    return JsonResponse(
                        {'status': 'error', 'message': f"Machine '{machine_name}' already exists."}, 
                        status=409
                    )

                instance = Machine_category_master.objects.create(machine_name=machine_name)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Machine category created successfully.',
                    'data': {'id': instance.id, 'machine_name': instance.machine_name}
                }, status=201)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


# -------------------------------------------------------------
# Operation Category Views
# -------------------------------------------------------------

@csrf_exempt
def operation_category_api(request, id=None):
    # ------------------ SINGLE RECORD OPERATIONS (GET, PUT, DELETE) ------------------
    if id:
        try:
            op = Operation_Category_master.objects.select_related('machine_cate_id').get(id=id)
        except Operation_Category_master.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Operation not found'}, status=404)

        # GET: Retrieve a single operation
        if request.method == 'GET':
            data = {
                'id': op.id,
                'machine_id': op.machine_cate_id.id,
                'machine_name': op.machine_cate_id.machine_name,
                'category_type': op.category_type,
                'operations': op.operations,
                'created_at': op.created_at,
                'updated_at': op.updated_at
            }
            return JsonResponse({'status': 'success', 'data': data}, status=200)

        # PUT: Update an existing operation
        elif request.method == 'PUT':
            try:
                body = json.loads(request.body)
                machine_id = body.get('machine_cate_id', op.machine_cate_id.id)
                category_type = body.get('category_type', op.category_type).strip()
                operations = body.get('operations', op.operations).strip()

                if not (machine_id and category_type and operations):
                    return JsonResponse(
                        {'status': 'error', 'message': 'machine_cate_id, category_type, and operations are required'},
                        status=400
                    )

                # Validate foreign key exists
                try:
                    machine = Machine_category_master.objects.get(id=machine_id)
                except Machine_category_master.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Machine category not found'}, status=404)

                # Check duplicate excluding current instance
                is_duplicate = Operation_Category_master.objects.filter(
                    machine_cate_id=machine,
                    category_type__iexact=category_type,
                    operations__iexact=operations
                ).exclude(id=id).exists()

                if is_duplicate:
                    return JsonResponse(
                        {'status': 'error', 'message': 'This operation already exists for this machine category.'},
                        status=409
                    )

                op.machine_cate_id = machine
                op.category_type = category_type
                op.operations = operations
                op.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Operation updated successfully.',
                    'data': {
                        'id': op.id,
                        'machine_id': op.machine_cate_id.id,
                        'category_type': op.category_type,
                        'operations': op.operations
                    }
                }, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

        # DELETE: Remove an operation
        elif request.method == 'DELETE':
            op.delete()
            return JsonResponse({'status': 'success', 'message': 'Operation deleted successfully.'}, status=200)

    # ------------------ BULK/CREATION OPERATIONS (GET ALL, POST) ------------------
    else:
        # GET: Retrieve all operations
        if request.method == 'GET':
            data = []
            for op in Operation_Category_master.objects.select_related('machine_cate_id'):
                data.append({
                    'id': op.id,
                    'machine_id': op.machine_cate_id.id,
                    'machine_name': op.machine_cate_id.machine_name,
                    'category_type': op.category_type,
                    'operations': op.operations,
                    'created_at': op.created_at,
                    'updated_at': op.updated_at
                })
            return JsonResponse({'status': 'success', 'data': data}, status=200)

        # POST: Create operation
        elif request.method == 'POST':
            try:
                body = json.loads(request.body)
                machine_id = body.get('machine_cate_id')
                category_type = body.get('category_type', '').strip()
                operations = body.get('operations', '').strip()

                if not (machine_id and category_type and operations):
                    return JsonResponse(
                        {'status': 'error', 'message': 'machine_cate_id, category_type, and operations are required'},
                        status=400
                    )

                try:
                    machine = Machine_category_master.objects.get(id=machine_id)
                except Machine_category_master.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Machine category not found'}, status=404)

                is_duplicate = Operation_Category_master.objects.filter(
                    machine_cate_id=machine,
                    category_type__iexact=category_type,
                    operations__iexact=operations
                ).exists()

                if is_duplicate:
                    return JsonResponse(
                        {'status': 'error', 'message': 'This operation already exists for this machine category.'},
                        status=409
                    )

                instance = Operation_Category_master.objects.create(
                    machine_cate_id=machine,
                    category_type=category_type,
                    operations=operations
                )

                return JsonResponse({
                    'status': 'success',
                    'message': 'Operation created successfully.',
                    'data': {
                        'id': instance.id,
                        'machine_id': instance.machine_cate_id.id,
                        'category_type': instance.category_type,
                        'operations': instance.operations
                    }
                }, status=201)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)