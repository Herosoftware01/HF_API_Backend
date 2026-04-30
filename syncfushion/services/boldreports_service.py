from django.conf import settings
import requests
import uuid
import hmac
import hashlib
import base64
import time

BOLD_REPORTS_URL = settings.BOLD_REPORTS["URL"]
SITE_IDENTIFIER = settings.BOLD_REPORTS["SITE_IDENTIFIER"]
USER_EMAIL = settings.BOLD_REPORTS["USER_EMAIL"]
EMBED_SECRET_KEY = settings.BOLD_REPORTS["EMBED_SECRET_KEY"]


def generate_auth_token():
    nonce = str(uuid.uuid4())
    timestamp = str(int(time.time()))

    embed_message = (
        f"embed_nonce={nonce}&user_email={USER_EMAIL}&timestamp={timestamp}"
    )

    signature = base64.b64encode(
        hmac.new(
            EMBED_SECRET_KEY.encode("utf-8"),
            embed_message.lower().encode("utf-8"),
            hashlib.sha256,
        ).digest()
    ).decode("utf-8")

    token_url = (
        f"{BOLD_REPORTS_URL.rstrip('/')}/reporting/api/site/{SITE_IDENTIFIER}/token"
    )

    payload = {
        "grant_type": "embed_secret",
        "username": USER_EMAIL,
        "embed_nonce": nonce,
        "embed_signature": signature,
        "timestamp": timestamp,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=payload, headers=headers, timeout=(5, 60))
    response.raise_for_status()

    data = response.json()

    if "access_token" not in data:
        raise RuntimeError(f"Token generation failed: {data}")
    return data

def get_reports_list():
    token_data = generate_auth_token()

    url = (
        f"{BOLD_REPORTS_URL.rstrip('/')}/reporting/api/site/{SITE_IDENTIFIER}/v5.0/items"
    )

    params = {"itemType": "Report"}
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    response = requests.get(url, headers=headers, params=params, timeout=(5, 60))
    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "Items" in data:
        return data
    else:
        raise RuntimeError(f"Unexpected response: {data}")

def export_report(
    report_id: str,
    server_path: str = "",
    export_type: str = "PDF",
    filter_parameters: str | None = None,
):
    """
    Calls Bold Reports v5.0 export API (Items_ExportReportV3)
    """

    token_data = generate_auth_token()

    url = (
        f"{BOLD_REPORTS_URL.rstrip('/')}"
        f"/reporting/api/site/{SITE_IDENTIFIER}/v5.0/reports/export"
    )

    payload = {
        "ReportId": report_id,
        "ServerPath": server_path,
        "ExportType": export_type,
        "FilterParameters": filter_parameters or "",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data['access_token']}",
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=(5, 120)
    )

    response.raise_for_status()
    result = response.json()

    if not isinstance(result, dict) or "FileContent" not in result:
        raise RuntimeError(f"Export failed: {result}")

    return result
