from django.http import JsonResponse
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import TrsWorkentry,user_master,project_master,category_master,subcategory_master,task_master,project_task_mapping


@csrf_exempt
def user_master_api(request):

    if request.method == 'GET':
        data = user_master.objects.all()
        return JsonResponse(list(data.values()),
         safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            obj = user_master.objects.create(
                user_name=body.get('user_name'),
                code=body.get('code'),
                user_role=body.get('user_role'),
                cost_per_hour=body.get('cost_per_hour'),
                user_status=body.get('user_status'),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            return JsonResponse({
                "status": True,
                "message": "User created successfully",
                "id": obj.id
            })
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    elif request.method == 'PUT':
        try:
            body = json.loads(request.body)
            user_id = body.get('id')
            obj = user_master.objects.get(id=user_id)

            obj.user_name = body.get('user_name', obj.user_name)
            obj.user_role = body.get('user_role', obj.user_role)
            obj.cost_per_hour = body.get('cost_per_hour', obj.cost_per_hour)
            obj.user_status = body.get('user_status', obj.user_status)
            obj.updated_at = timezone.now()

            obj.save()

            return JsonResponse({
                "status": True,
                "message": "User updated successfully"
            })
        except user_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "User not found"
            }, status=404)
    elif request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            user_id = body.get('id')
            obj = user_master.objects.get(id=user_id)
            obj.delete()

            return JsonResponse({
                "status": True,
                "message": "User deleted successfully"
            })
        except user_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "User not found"
            }, status=404)

    return JsonResponse({
        "status": False,
        "message": "Invalid request"
    }, status=405)

@csrf_exempt
def project_master_api(request):

    if request.method == 'GET':
        data = project_master.objects.all()
        return JsonResponse(list(data.values()),
         safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            obj = project_master.objects.create(
                project_name=body.get('project_name'),
                project_description=body.get('project_description'),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            return JsonResponse({
                "status": True,
                "message": "Project created successfully",
                "id": obj.id
            })
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    elif request.method == 'PUT':
        try:
            body = json.loads(request.body)
            project_id = body.get('id')
            obj = project_master.objects.get(id=project_id)

            obj.project_name = body.get('project_name', obj.project_name)
            obj.project_description = body.get('project_description', obj.project_description)
            obj.updated_at = timezone.now()

            obj.save()

            return JsonResponse({
                "status": True,
                "message": "Project updated successfully"
            })
        except project_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Project not found"
            }, status=404)
    elif request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            project_id = body.get('id')
            obj = project_master.objects.get(id=project_id)
            obj.delete()

            return JsonResponse({
                "status": True,
                "message": "Project deleted successfully"
            })
        except project_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Project not found"
            }, status=404)

    return JsonResponse({
        "status": False,
        "message": "Invalid request"
    }, status=405)


@csrf_exempt
def category_master_api(request):
    if request.method == 'GET':
        data = category_master.objects.all()
        return JsonResponse(list(data.values()), safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            obj = category_master.objects.create(
                category_name=body.get('category_name'),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            return JsonResponse({
                "status": True,
                "message": "Category created successfully",
                "id": obj.id
            })
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    elif request.method == 'PUT':
        try:
            body = json.loads(request.body)
            category_id = body.get('id')
            obj = category_master.objects.get(id=category_id)

            obj.category_name = body.get('category_name', obj.category_name)
            obj.updated_at = timezone.now()

            obj.save()

            return JsonResponse({
                "status": True,
                "message": "Category updated successfully"
            })
        except category_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Category not found"
            }, status=404)
    elif request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            category_id = body.get('id')
            obj = category_master.objects.get(id=category_id)
            obj.delete()

            return JsonResponse({
                "status": True,
                "message": "Category deleted successfully"
            })
        except category_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Category not found"
            }, status=404)

    return JsonResponse({
        "status": False,
        "message": "Invalid request"
    }, status=405)

@csrf_exempt
def subcategory_master_api(request):
    if request.method == 'GET':
        data = subcategory_master.objects.all()
        return JsonResponse(list(data.values()), safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            category_id = body.get('category_id')
            category = category_master.objects.get(id=category_id)

            obj = subcategory_master.objects.create(
                category=category,
                subcategory_name=body.get('subcategory_name'),
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            return JsonResponse({
                "status": True,
                "message": "Subcategory created successfully",
                "id": obj.id
            })
        except category_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Category not found"
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    elif request.method == 'PUT':
        try:
            body = json.loads(request.body)
            subcategory_id = body.get('id')
            obj = subcategory_master.objects.get(id=subcategory_id)

            category_id = body.get('category_id')
            if category_id:
                category = category_master.objects.get(id=category_id)
                obj.category = category

            obj.subcategory_name = body.get('subcategory_name', obj.subcategory_name)
            obj.updated_at = timezone.now()

            obj.save()

            return JsonResponse({
                "status": True,
                "message": "Subcategory updated successfully"
            })
        except subcategory_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Subcategory not found"
            }, status=404)
        except category_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Category not found"
            }, status=404)
    elif request.method == 'DELETE':
        try:
            body = json.loads(request.body)
            subcategory_id = body.get('id')
            obj = subcategory_master.objects.get(id=subcategory_id)
            obj.delete()

            return JsonResponse({
                "status": True,
                "message": "Subcategory deleted successfully"
            })
        except subcategory_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Subcategory not found"
            }, status=404)
@csrf_exempt
def task_master_api(request):
    if request.method == 'GET':
        data = task_master.objects.all()

        return JsonResponse(
            list(data.values(
                'id',
                'project_id',
                'code_id',
                'task_name',
                'task_description',
                'task_status',
                'created_at',
                'updated_at'
            )),
            safe=False
        )

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)

            # Get IDs from frontend
            proj_id = body.get('project_id')
            user_id = body.get('user_id')

            # Convert empty values to None
            if proj_id == "":
                proj_id = None

            if user_id == "":
                user_id = None

            # Create task
            obj = task_master.objects.create(
                project_id=proj_id,
                code_id=user_id,   # Save user_master ID here
                task_name=body.get('task_name'),
                task_description=body.get('task_description', ''),
                task_status=body.get('task_status', 'Pending')
            )

            return JsonResponse({
                "status": True,
                "message": "Task created successfully",
                "id": obj.id,
                "project_id": obj.project_id,
                "user_id": obj.code_id
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    return JsonResponse({
        "status": False,
        "message": "Method not allowed"
    }, status=405)


@csrf_exempt
def project_task_mapping_api(request):
    if request.method == 'GET':
        data = project_task_mapping.objects.all()
        return JsonResponse(list(data.values()), safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            project_id = body.get('project_id')
            task_id = body.get('task_id')

            project = project_master.objects.get(id=project_id)
            task = task_master.objects.get(id=task_id)

            obj = project_task_mapping.objects.create(
                project=project,
                task=task,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            return JsonResponse({
                "status": True,
                "message": "Project-Task mapping created successfully",
                "id": obj.id
            })
        except project_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Project not found"
            }, status=404)
        except task_master.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Task not found"
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

@csrf_exempt
def trs_workentry(request, id=None):

    # GET ALL OR SINGLE RECORD
    if request.method == 'GET':
        if id:
            try:
                data = TrsWorkentry.objects.get(id=id)
                return JsonResponse(model_to_dict(data), safe=False)
            except TrsWorkentry.DoesNotExist:
                return JsonResponse(
                    {"status": False, "message": "Record not found"},
                    status=404
                )

        else:
            data = TrsWorkentry.objects.using('default').all()

            # Filters from query params
            name = request.GET.get('name')
            project = request.GET.get('project')
            entry_date = request.GET.get('date')

            if name:
                data = data.filter(username__icontains=name)

            if project:
                data = data.filter(projectname__icontains=project)

            if entry_date:
                data = data.filter(entrydate=entry_date)

            return JsonResponse(
                list(data.values()),
                safe=False
            )

    # INSERT
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)

            obj = TrsWorkentry.objects.create(
                username=body.get('username'),
                entrydate=body.get('entrydate'),
                project=body.get('project'),
                category=body.get('category'),
                subcat=body.get('subcat'),
                startdatetime=body.get('startdatetime'),
                startstatus=body.get('startstatus'),
                description=body.get('description'),
                enddatetime=body.get('enddatetime'),
                endstatus=body.get('endstatus'),
                duration=body.get('duration'),
                durationminutes=body.get('durationminutes'),
                createddate=timezone.now(),
                modifieddate=timezone.now()
            )

            return JsonResponse({
                "status": True,
                "message": "Record created successfully",
                "id": obj.id
            })

        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=400)

    # UPDATE
    elif request.method == 'PUT':
        try:
            if not id:
                return JsonResponse({
                    "status": False,
                    "message": "ID is required"
                }, status=400)

            body = json.loads(request.body)

            obj = TrsWorkentry.objects.get(id=id)

            obj.username = body.get('username', obj.username)
            obj.entrydate = body.get('entrydate', obj.entrydate)
            obj.project = body.get('project', obj.project)
            obj.category = body.get('category', obj.category)
            obj.subcat = body.get('subcat', obj.subcat)
            obj.startdatetime = body.get('startdatetime', obj.startdatetime)
            obj.startstatus = body.get('startstatus', obj.startstatus)
            obj.description = body.get('description', obj.description)
            obj.enddatetime = body.get('enddatetime', obj.enddatetime)
            obj.endstatus = body.get('endstatus', obj.endstatus)
            obj.duration = body.get('duration', obj.duration)
            obj.durationminutes = body.get(
                'durationminutes',
                obj.durationminutes
            )
            obj.modifieddate = timezone.now()

            obj.save()

            return JsonResponse({
                "status": True,
                "message": "Record updated successfully"
            })

        except TrsWorkentry.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Record not found"
            }, status=404)

    # DELETE
    elif request.method == 'DELETE':
        try:
            if not id:
                return JsonResponse({
                    "status": False,
                    "message": "ID is required"
                }, status=400)

            obj = TrsWorkentry.objects.get(id=id)
            obj.delete()

            return JsonResponse({
                "status": True,
                "message": "Record deleted successfully"
            })

        except TrsWorkentry.DoesNotExist:
            return JsonResponse({
                "status": False,
                "message": "Record not found"
            }, status=404)

    return JsonResponse({
        "status": False,
        "message": "Invalid request"
    }, status=405)
