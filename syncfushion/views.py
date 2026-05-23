from django.shortcuts import render
# from django.db import connections
from rest_framework import status
# from django.http import JsonResponse
from rest_framework import viewsets
from .models import GridSetting,TrsMaildtls
from django.http import JsonResponse
from rest_framework import status
from rest_framework import viewsets
from .models import GridSetting,DiWasg,DiWasg_img,TrsMaildtls, SyncfushionKanban, SyncfusionGantt, BlockEditor
from .serializers import GridSettingSerializer,TrsMaildtlsSerializer
from rest_framework.permissions import IsAuthenticated  # optional
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .services.boldreports_service import (
    generate_auth_token,
    get_reports_list,
    export_report
)

class GridSettingViewSet(viewsets.ModelViewSet):
    queryset = GridSetting.objects.all()
    serializer_class = GridSettingSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .services.boldreports_service import (
    generate_auth_token,
    get_reports_list,
    export_report
)

@api_view(['GET'])
def token_api(request):
   
    try:
        reports = generate_auth_token()
        return Response({
            "success": True,
            "data": reports
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)

@api_view(['GET'])
def reports_list_api(request):
    try:
        reports = get_reports_list()
        return Response({
            "success": True,
            "data": reports
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)


@api_view(["POST"])
def export_report_api(request):
   
    try:
        data = request.data

        report_id = data.get("report_id")
        export_type = data.get("export_type", "PDF")
        server_path = data.get("server_path", "/")
        filter_parameters = data.get("filter_parameters", "")

        if not report_id:
            return Response(
                {"success": False, "error": "report_id is required"},
                status=400,
            )

        result = export_report(
            report_id=report_id,
            server_path=server_path,
            export_type=export_type,
            filter_parameters=filter_parameters,
        )

        return Response({
            "success": True,
            "data": result
        })

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
    


#############################################

@csrf_exempt
def diwasg_list(request):

    # ✅ GET ALL
    if request.method == "GET":
        data = [model_to_dict_all(obj) for obj in DiWasg_img.objects.using('main').all()]
        return JsonResponse(data, safe=False)

    # ✅ CREATE (ALL fields dynamic)
    if request.method == "POST":
        body = json.loads(request.body)
        obj = DiWasg_img()
        for field in DiWasg_img._meta.fields:
            field_name = field.name
            if field_name in body:
                setattr(obj, field_name, body[field_name])

        obj.save()
        return JsonResponse({"message": "Created", "id": obj.asgby_code})
def model_to_dict_all(obj):
    data = {}
    for field in obj._meta.fields:
        data[field.name] = getattr(obj, field.name)
    return data
@csrf_exempt
def diwasg_detail(request, id):

    try:
        obj = DiWasg.objects.using('main').get(asgby_code=id)
    except DiWasg.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    # ✅ GET ONE
    if request.method == "GET":
        return JsonResponse(model_to_dict_all(obj))

    # ✅ UPDATE (ALL fields dynamic)
    if request.method == "PUT":
        body = json.loads(request.body)
        for field in DiWasg._meta.fields:
            field_name = field.name
            if field_name in body:
                setattr(obj, field_name, body[field_name])
        obj.save()
        return JsonResponse({"message": "Updated"})

    # ✅ DELETE
    if request.method == "DELETE":
        obj.delete()
        return JsonResponse({"message": "Deleted"})
    
import os
from django.conf import settings
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_pdf(request):
    if request.method == "POST":
        file = request.FILES.get("file")

        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # ✅ Validate PDF
        if not file.name.lower().endswith(".pdf"):
            return JsonResponse({"error": "Only PDF allowed"}, status=400)

        base_path = settings.PDF_STORAGE_PATH

        # ✅ Ensure folder exists
        os.makedirs(base_path, exist_ok=True)

        file_path = os.path.join(base_path, file.name)

        # ✅ Replace if exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # ✅ Save file
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return JsonResponse({
            "message": "Uploaded successfully",
            "file_path": file_path
        })

    return JsonResponse({"error": "Invalid request"}, status=405)

def get_pdf(request, file_name):
    file_path = os.path.join(settings.PDF_STORAGE_PATH, file_name)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    return FileResponse(open(file_path, "rb"), content_type="application/pdf")

def list_pdfs(request):
    path = settings.PDF_STORAGE_PATH
    files = []
    for file in os.listdir(path):
        if file.lower().endswith(".pdf"):
            files.append({
                "name": file,
                "url": f"/get-pdf/{file}/"
            })

    return JsonResponse(files, safe=False)




#############################################

def get_mailss(request):
    if request.method == "GET":

        mails = list(
            TrsMaildtls.objects.values()
        )

        return JsonResponse(
            {
                "message": "Mail list fetched successfully",
                "data": mails
            },
            safe=False
        )
@api_view(['GET'])
def get_mails(request):
    mails = TrsMaildtls.objects.all()
    serializer = TrsMaildtlsSerializer(mails, many=True)
    return Response(serializer.data)


# ADD API
@api_view(['POST'])
def add_mail(request):
    serializer = TrsMaildtlsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Mail details added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE API
@api_view(['PUT'])
def update_mail(request, pk):
    try:
        mail = TrsMaildtls.objects.get(pk=pk)
    except TrsMaildtls.DoesNotExist:
        return Response(
            {"error": "Record not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TrsMaildtlsSerializer(mail, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Mail details updated successfully",
                "data": serializer.data
            }
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE API
@api_view(['DELETE'])
def delete_mail(request, pk):
    try:
        mail = TrsMaildtls.objects.get(pk=pk)
    except TrsMaildtls.DoesNotExist:
        return Response(
            {"error": "Record not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    mail.delete()

    return Response(
        {"message": "Mail details deleted successfully"},
        status=status.HTTP_200_OK
    )

#### syncfusion kanban
@csrf_exempt
def tasks_create(request):

    if request.method == "POST":
        body = json.loads(request.body)
        obj = SyncfushionKanban.objects.using('mssql1').create(

            Title=body.get("Title"),
            Status=body.get("Status"),
            Description=body.get("Description"),
            Type=body.get("Type"),
            Priority=body.get("Priority"),
            Tags=body.get("Tags"),
            Estimate=body.get("Estimate"),
            Assignee=body.get("Assignee"),
            Rankid=body.get("RankId"),
            Reporter=body.get("Reporter")
        )
        
        return JsonResponse({ "message": "Created", "Id": obj.Id })

# READ ALL
def tasks_list(request):

    data = list(SyncfushionKanban.objects.using('mssql1').values())
    return JsonResponse(data, safe=False)

# READ SINGLE
def tasks_single(request, id):

    data = SyncfushionKanban.objects.using('mssql1').filter(Id=id).values().first()
    return JsonResponse(data, safe=False)

# UPDATE
@csrf_exempt
def tasks_update(request, id):

    if request.method == "PUT":
        body = json.loads(request.body)
        SyncfushionKanban.objects.using('mssql1').filter(Id=id).update(

            Title=body.get("Title"),
            Status=body.get("Status"),
            Description=body.get("Description"),
            Type=body.get("Type"),
            Priority=body.get("Priority"),
            Tags=body.get("Tags"),
            Estimate=body.get("Estimate"),
            Assignee=body.get("Assignee"),
            RankId=body.get("RankId"),
            Reporter=body.get("Reporter")

        )

        return JsonResponse({ "message": "Updated" })

# DELETE
@csrf_exempt
def tasks_delete(request, id):

    if request.method == "DELETE":

        SyncfushionKanban.objects.using('mssql1').filter(Id=id).delete()
        return JsonResponse({ "message": "Deleted" })
    
from django.core.files.storage import FileSystemStorage   
@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        if not image:
            return JsonResponse({
                "status": False,
                "message": "No image uploaded"
            })
        upload_path = r"\\adminserver\File Sharing\AAAA Hero\Images"
        fs = FileSystemStorage(location=upload_path)
        filename = fs.save(image.name, image)
        saved_path = os.path.join(upload_path, filename)
        return JsonResponse({
            "status": True,
            "filename": filename,
            "saved_path": saved_path
        })

@csrf_exempt
def gantt_list(request):

    if request.method == "GET":
        data = list(
            SyncfusionGantt.objects.using('mssql1').values())
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        body = json.loads(request.body)
        obj = SyncfusionGantt.objects.using('mssql1').create(
            taskid=body.get("taskid"),
            taskname=body.get("taskname"),
            startdate=body.get("startdate"),
            enddate=body.get("enddate"),
            progress=body.get("progress"),
            status=body.get("status"),
            priority=body.get("priority"),
            assignee=body.get("assignee"),
            resourcesimage=body.get("resourcesimage"),
            department=body.get("department"),
            predecessor=body.get("predecessor"),
            parentid=body.get("parentid"),
        )
        return JsonResponse({
            "message": "Created Successfully",
            "taskid": obj.taskid
        })

@csrf_exempt
def gantt_detail(request, id):
    try:
        obj = SyncfusionGantt.objects.using('mssql1').get(taskid=id)
    except SyncfusionGantt.DoesNotExist:
        return JsonResponse({
            "error": "Data Not Found"
        }, status=404)

    if request.method == "GET":

        data = {
            "taskid": obj.taskid,
            "taskname": obj.taskname,
            "startdate": obj.startdate,
            "enddate": obj.enddate,
            "progress": obj.progress,
            "status": obj.status,
            "priority": obj.priority,
            "assignee": obj.assignee,
            "resourcesimage": obj.resourcesimage,
            "department": obj.department,
            "predecessor": obj.predecessor,
            "parentid": obj.parentid,
        }

        return JsonResponse(data)

    elif request.method == "PUT":
        body = json.loads(request.body)

        obj.taskname = body.get("taskname", obj.taskname)
        obj.startdate = body.get("startdate", obj.startdate)
        obj.enddate = body.get("enddate", obj.enddate)
        obj.progress = body.get("progress", obj.progress)
        obj.status = body.get("status", obj.status)
        obj.priority = body.get("priority", obj.priority)
        obj.assignee = body.get("assignee", obj.assignee)
        obj.resourcesimage = body.get("resourcesimage", obj.resourcesimage)
        obj.department = body.get("department", obj.department)
        obj.predecessor = body.get("predecessor", obj.predecessor)
        obj.parentid = body.get("parentid", obj.parentid)

        obj.save(using='mssql1')
        return JsonResponse({
            "message": "Updated Successfully"
        })

    elif request.method == "DELETE":

        obj.delete()
        return JsonResponse({
            "message": "Deleted Successfully"
        })
    

@csrf_exempt
def block_list(request):

    if request.method == "GET":
        data = list(
            BlockEditor.objects.using('mssql1').values())
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            obj = BlockEditor.objects.using('mssql1').create(
                blocks=body.get("blocks", [])
            )
            return JsonResponse({
                "message": "Created Successfully",
                "id": obj.id
            })

        except Exception as e:
            return JsonResponse({ "error": str(e) }, status=400)

@csrf_exempt
def block_detail(request, id):

    try:
        obj = BlockEditor.objects.using('mssql1').get(id=id)

    except BlockEditor.DoesNotExist:
        return JsonResponse({
            "error": "Data Not Found"
        }, status=404)

    if request.method == "GET":
        data = {
            "id": obj.id,
            "blocks": obj.blocks,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        }
        return JsonResponse(data)

    elif request.method == "PUT":
        try:
            body = json.loads(request.body)
            obj.blocks = body.get("blocks", obj.blocks)
            obj.save(using='mssql1')
            return JsonResponse({
                "message": "Updated Successfully"
            })

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)

    elif request.method == "DELETE":
        obj.delete()
        return JsonResponse({
            "message": "Deleted Successfully"
        })
