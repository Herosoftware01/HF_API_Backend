from django.shortcuts import render
from .models import TxNotification,TmpPrdprn
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import json
import tempfile
import subprocess
import os
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
            "rowno": rec.rowno,
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
            "o_finaldelvdate": rec.o_finaldelvdate,
            "o_merch": rec.o_merch,
            "o_styledesc": rec.o_styledesc,
            "buyer": rec.buyer,
            "img": rec.img,
            "tbpic": (
                f"https://app.herofashion.com/order_image/"
                f"{str(rec.tbpic).replace(chr(92), '/').split('/')[-1]}"
                if rec.tbpic else ""
            )
        })
    return JsonResponse(response_data, safe=False)


@csrf_exempt
def html_to_image(request):

    # Only allow POST
    if request.method != "POST":
        return JsonResponse(
            {
                "status": False,
                "error": "Only POST method is allowed"
            },
            status=405
        )

    # Check request body
    if not request.body:
        return JsonResponse(
            {
                "status": False,
                "error": "Request body is empty"
            },
            status=400
        )

    # Parse JSON
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as e:
        return JsonResponse(
            {
                "status": False,
                "error": "Invalid JSON",
                "details": str(e)
            },
            status=400
        )

    # Get HTML
    html_content = data.get("html")

    if not html_content:
        return JsonResponse(
            {
                "status": False,
                "error": "html field is required"
            },
            status=400
        )

    # wkhtmltoimage path
    wkhtmltoimage = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe"

    if not os.path.exists(wkhtmltoimage):
        return JsonResponse(
            {
                "status": False,
                "error": "wkhtmltoimage.exe not found",
                "path": wkhtmltoimage
            },
            status=500
        )

    try:

        with tempfile.TemporaryDirectory() as temp_dir:

            html_file = os.path.join(temp_dir, "input.html")
            png_file = os.path.join(temp_dir, "output.png")

            # Write HTML file
            with open(
                html_file,
                "w",
                encoding="utf-8"
            ) as f:
                f.write(html_content)

            # Convert HTML -> PNG
            result = subprocess.run(
                [
                    wkhtmltoimage,
                    "--quality",
                    "100",
                    "--enable-local-file-access",
                    html_file,
                    png_file
                ],
                capture_output=True,
                text=True,
                check=False
            )

            # Check wkhtmltoimage error
            if result.returncode != 0:

                return JsonResponse(
                    {
                        "status": False,
                        "error": "HTML to image conversion failed",
                        "details": result.stderr.strip()
                    },
                    status=500
                )

            # Check generated PNG
            if not os.path.exists(png_file):

                return JsonResponse(
                    {
                        "status": False,
                        "error": "PNG file was not generated"
                    },
                    status=500
                )

            # Open image
            with Image.open(png_file) as img:

                output = io.BytesIO()

                img.save(
                    output,
                    format="PNG",
                    optimize=True,
                    compress_level=9
                )

                image_data = output.getvalue()

            # Image size
            size_mb = len(image_data) / (1024 * 1024)

            if size_mb > 5:

                return JsonResponse(
                    {
                        "status": False,
                        "error": "Image size exceeds 5 MB",
                        "size_mb": round(size_mb, 2)
                    },
                    status=400
                )

        # Return PNG
        response = HttpResponse(
            image_data,
            content_type="image/png"
        )

        response["Content-Disposition"] = 'inline; filename="output.png"'

        return response

    except Exception as e:

        return JsonResponse(
            {
                "status": False,
                "error": "Internal server error",
                "details": str(e)
            },
            status=500
        )
