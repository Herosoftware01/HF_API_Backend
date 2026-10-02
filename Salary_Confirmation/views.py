import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MasProcess, Salcon_Operation_Category, Salcon_Employee_Details, Salcon_Approval, Salcon_Individual_Assessment

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
def Employee_Details(request):

    if request.method == 'GET':

        id = request.GET.get('slno')
        queryset = Salcon_Employee_Details.objects.all()

        if id:
            queryset = queryset.filter(slno=id)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        for key in data:

            exists = Salcon_Employee_Details.objects.filter(
                slno=key['slno']
            ).exists()

            if exists:
                return JsonResponse({
                    "message": f"Employee {key['slno']} already exists"
                }, status=400)

            if not exists:
                Salcon_Employee_Details.objects.create(
                    emp_id=key['emp_id'],
                    emp_name=key['emp_name'],
                    prev_salary=key['prev_salary'],
                    prev_company=key['prev_company'],
                    prev_category=key['prev_category'],
                    experience=key['experience'],
                    current_category=key['current_category'],
                    current_grade=key['current_grade'],
                    evaluation_date=key['evaluation_date'],
                    unit=key['unit'],
                    salary_recommendation=key['salary_recommendation'],
                    salary_type=key['salary_type']
                )

    elif request.method == 'PUT':

        data = json.loads(request.body)

        for key in data:

            Salcon_Employee_Details.objects.filter(
                slno=key['slno']
            ).update(
                emp_id=key['emp_id'],
                emp_name=key['emp_name'],
                prev_salary=key['prev_salary'],
                prev_company=key['prev_company'],
                prev_category=key['prev_category'],
                experience=key['experience'],
                current_category=key['current_category'],
                current_grade=key['current_grade'],
                evaluation_date=key['evaluation_date'],
                unit=key['unit'],
                salary_recommendation=key['salary_recommendation'],
                salary_type=key['salary_type']
            )

        return JsonResponse({
            "message": "Employee records updated"
        }, status=200)

    elif request.method == 'DELETE':

        data = json.loads(request.body)

        for key in data:

            Salcon_Employee_Details.objects.filter(
                slno=key['slno']
            ).delete()

        return JsonResponse({
            "message": "Employee records deleted"
        }, status=200)

@csrf_exempt
def Operation_Category(request):

    if request.method == 'GET':

        slno = request.GET.get('slno')
        process_id = request.GET.get('process_id')

        queryset = Salcon_Operation_Category.objects.all()

        if slno:
            queryset = queryset.filter(slno=slno)

        if process_id:
            queryset = queryset.filter(process_id=process_id)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        for key in data:

            # Check duplicate
            exists = Salcon_Operation_Category.objects.filter(
                process_id=key['process_id'],
                jobno=key['jobno'],
                oper_category=key['oper_category']
            ).exists()

            if exists:
                return JsonResponse({
                    "message": "Operation record already exists"
                }, status=400)

            if not exists:
                Salcon_Operation_Category.objects.create(
                    slno=key['slno'],
                    process_id=key['process_id'],
                    jobno=key['jobno'],
                    topbottom=key['topbottom'],
                    emp_id=key['emp_id'],
                    oper_category=key['oper_category'],
                    sam_time=key['sam_time'],
                    cycle_time1=key['cycle_time1'],
                    cycle_time2=key['cycle_time2'],
                    cycle_time3=key['cycle_time3'],
                    cycle_time4=key['cycle_time4'],
                    cycle_time5=key['cycle_time5'],
                    avg_with_alw=key['avg_with_alw'],
                    given=key['given'],
                    achved=key['achved'],
                    efficiency=key['efficiency']
                )

        return JsonResponse({
            "message": "Operation records created"
        }, status=201)

    elif request.method == 'PUT':

        data = json.loads(request.body)

        for key in data:

            Salcon_Operation_Category.objects.filter(
                id=key['id']
            ).update(
                slno=key['slno'],
                process_id=key['process_id'],
                jobno=key['jobno'],
                topbottom=key['topbottom'],
                emp_id=key['emp_id'],
                oper_category=key['oper_category'],
                sam_time=key['sam_time'],
                cycle_time1=key['cycle_time1'],
                cycle_time2=key['cycle_time2'],
                cycle_time3=key['cycle_time3'],
                cycle_time4=key['cycle_time4'],
                cycle_time5=key['cycle_time5'],
                avg_with_alw=key['avg_with_alw'],
                given=key['given'],
                achved=key['achved'],
                efficiency=key['efficiency']
            )

        return JsonResponse({
            "message": "Operation records updated"
        }, status=200)

    elif request.method == 'DELETE':

        data = json.loads(request.body)

        for key in data:

            Salcon_Operation_Category.objects.filter(
                id=key['id']
            ).delete()

        return JsonResponse({
            "message": "Operation records deleted"
        }, status=200)


@csrf_exempt
def Approval(request):

    if request.method == 'GET':

        slno = request.GET.get('slno')
        queryset = Salcon_Approval.objects.all()

        if slno:
            queryset = queryset.filter(slno=slno)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        for key in data:

            exists = Salcon_Approval.objects.filter(
                slno=key['slno']
            ).exists()

            if exists:
                return JsonResponse({
                    "message": "Approval record already exists"
                }, status=400)

            if not exists:
                Salcon_Approval.objects.create(
                    slno=key['slno'],
                    emp_id=key['emp_id'],
                    salary_approved=key['salary_approved'],
                    approve_fm=key['approve_fm'],
                    approve_fm_date=key['approve_fm_date'],
                    approve_hr=key['approve_hr'],
                    approve_hr_date=key['approve_hr_date'],
                    approve_md=key['approve_md'],
                    approve_md_date=key['approve_md_date']
                )

        return JsonResponse({
            "message": "Approval records created"
        }, status=201)

    elif request.method == 'PUT':

        data = json.loads(request.body)

        for key in data:

            Salcon_Approval.objects.filter(
                id=key['id']
            ).update(
                slno=key['slno'],
                emp_id=key['emp_id'],
                salary_approved=key['salary_approved'],
                approve_fm=key['approve_fm'],
                approve_fm_date=key['approve_fm_date'],
                approve_hr=key['approve_hr'],
                approve_hr_date=key['approve_hr_date'],
                approve_md=key['approve_md'],
                approve_md_date=key['approve_md_date']
            )

        return JsonResponse({
            "message": "Approval records updated"
        }, status=200)

    elif request.method == 'DELETE':

        data = json.loads(request.body)

        for key in data:
            Salcon_Approval.objects.filter(
                id=key['id']
            ).delete()

        return JsonResponse({
            "message": "Approval records deleted"
        }, status=200)

@csrf_exempt
def Individual_Assessment(request):

    if request.method == 'GET':

        slno = request.GET.get('slno')
        queryset = Salcon_Individual_Assessment.objects.all()

        if slno:
            queryset = queryset.filter(slno=slno)

        data = list(queryset.values())
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        
        data = json.loads(request.body)

        for key in data:

            exists = Salcon_Individual_Assessment.objects.filter(
                slno=key['slno']
            ).exists()

            if exists:
                return JsonResponse({
                    "message": "Assessment record already exists"
                }, status=400)

            if not exists:
                Salcon_Individual_Assessment.objects.create(
                    slno=key['slno'],
                    emp_id=key['emp_id'],
                    assessment_criteria=key['assessment_criteria'],
                    assessment_status=key['assessment_status'],
                    remarks=key['remarks'],
                    prepared_ie=key['prepared_ie'],
                    approved_pi=key['approved_pi']
                )

        return JsonResponse({
            "message": "Assessment records created"
        }, status=201)

    elif request.method == 'PUT':

        data = json.loads(request.body)

        for key in data:

            Salcon_Individual_Assessment.objects.filter(
                id=key['id']
            ).update(
                slno=key['slno'],
                emp_id=key['emp_id'],
                assessment_criteria=key['assessment_criteria'],
                assessment_status=key['assessment_status'],
                remarks=key['remarks'],
                prepared_ie=key['prepared_ie'],
                approved_pi=key['approved_pi']
            )

        return JsonResponse({
            "message": "Assessment records updated"
        }, status=200)

    elif request.method == 'DELETE':

        data = json.loads(request.body)

        for key in data:

            Salcon_Individual_Assessment.objects.filter(
                id=key['id']
            ).delete()

        return JsonResponse({
            "message": "Assessment records deleted"
        }, status=200)
