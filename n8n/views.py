from django.shortcuts import render
from .models import TxNotification,TmpPrdprn
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.http import HttpResponse, JsonResponse
from PIL import Image
import tempfile
import subprocess
import io

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





@csrf_exempt
def html_to_image(request):
    try:
        data = json.loads(request.body)
        html_content = data.get("html")

        if not html_content:
            return JsonResponse(
                {"error": "html field is required"},
                status=400
            )

        with tempfile.TemporaryDirectory() as temp_dir:

            html_file = os.path.join(temp_dir, "input.html")
            png_file = os.path.join(temp_dir, "output.png")

            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            subprocess.run([
                r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe",
                "--quality", "100",
                "--enable-local-file-access",
                html_file,
                png_file
            ], check=True)

            img = Image.open(png_file)

            output = io.BytesIO()

            img.save(
                output,
                format="PNG",
                optimize=True,
                compress_level=9
            )

            image_data = output.getvalue()

            # Optional: reject if > 5 MB
            size_mb = len(image_data) / (1024 * 1024)

            if size_mb > 5:
                return JsonResponse({
                    "error": f"Image size is {size_mb:.2f} MB (> 5 MB)"
                }, status=400)

        return HttpResponse(
            image_data,
            content_type="image/png"
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
