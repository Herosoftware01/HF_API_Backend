# test_wa.py
import requests

WHATSAPP_SEND_URL = 'https://ws.herofashion.com/send'
WHATSAPP_GROUP_ID = '120363427040771599@g.us'

file_path = r'D:\Qc Report Image\roving_1_2026-07-11_1.png'

with open(file_path, 'rb') as f:
    files = {'file': (file_path.split('\\')[-1], f, 'image/png')}
    data = {'groupId': WHATSAPP_GROUP_ID}

    resp = requests.post(WHATSAPP_SEND_URL, data=data, files=files, timeout=30)

print('status:', resp.status_code)
print('body:', resp.text)