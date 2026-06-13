import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
c = Client()
response = c.get('/static/css/index.css')
print("Status Code:", response.status_code)
print("Content-Type:", response.get('Content-Type'))
if response.status_code == 200:
    print("Content length:", len(response.content))
else:
    print("Content:", response.content)
