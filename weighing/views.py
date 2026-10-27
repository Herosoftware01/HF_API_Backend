
import socket
from django.http import JsonResponse

SCALE_IP = "192.168.1.101"
SCALE_PORT = 8080


def scale_weight_api(request):
    try:
        with socket.create_connection(
            (SCALE_IP, SCALE_PORT),
            timeout=5
        ) as sock:
            sock.settimeout(1)

            chunks = []

            while True:
                try:
                    data = sock.recv(1024)

                    if not data:
                        break

                    chunks.append(data)

                    # Stop when a complete line is received.
                    if b"\n" in data or b"\r" in data:
                        break

                except socket.timeout:
                    # If data arrived, return the collected data.
                    if chunks:
                        break

                    return JsonResponse({
                        "success": False,
                        "message": "No data received from scale because weight cannot stable"
                    }, status=504)

        raw_data = b"".join(chunks).decode(
            "ascii", errors="replace"
        ).strip()

        return JsonResponse({
            "success": True,
            "weight": raw_data
        })

    except OSError as error:
        return JsonResponse({
            "success": False,
            "message": str(error)
        }, status=502)
