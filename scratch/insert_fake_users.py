import os
import sys
import django

# Setup Django environment
sys.path.append(r"c:\Users\SHYAM PRASATH S\Desktop\DESKTOP FOLDERS\Software Devleopment\hf-app\HF_API_Backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from herofashion.models import Role, User
from django.contrib.auth import get_user_model

def create_fake_data():
    print("Creating Roles...")
    roles = ["Admin", "Manager", "QC_Inspector", "Employee"]
    role_objs = {}
    for role_name in roles:
        role_obj, created = Role.objects.get_or_create(name=role_name)
        role_objs[role_name] = role_obj
        if created:
            print(f"- Created Role: {role_name}")
        else:
            print(f"- Role already exists: {role_name}")
            
    print("\nCreating Users...")
    users_to_create = [
        {"username": "admin", "email": "admin@herofashion.com", "password": "Password@01", "role": "Admin", "is_superuser": True, "is_staff": True},
        {"username": "shyam", "email": "shyam@herofashion.com", "password": "Password@01", "role": "Manager", "is_superuser": False, "is_staff": True},
        {"username": "qc_inspector", "email": "qc@herofashion.com", "password": "Password@01", "role": "QC_Inspector", "is_superuser": False, "is_staff": False},
        {"username": "employee1", "email": "emp1@herofashion.com", "password": "Password@01", "role": "Employee", "is_superuser": False, "is_staff": False},
        {"username": "employee2", "email": "emp2@herofashion.com", "password": "Password@01", "role": "Employee", "is_superuser": False, "is_staff": False},
    ]

    for user_info in users_to_create:
        username = user_info["username"]
        email = user_info["email"]
        password = user_info["password"]
        role_name = user_info["role"]
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"- User '{username}' already exists.")
            continue
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_superuser=user_info["is_superuser"],
            is_staff=user_info["is_staff"],
            role=role_objs[role_name]
        )
        print(f"- Created User: {username} (Role: {role_name})")

if __name__ == "__main__":
    create_fake_data()
