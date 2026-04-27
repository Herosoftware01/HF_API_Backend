from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import RoleSubMenuPermission,User,Role,RoleMenuPermission,Menu, SubMenu
from .serializers import MyTokenSerializer,RoleSerializer,SubMenuSerializer,MenuSerializer,UserSerializer, RoleMenuPermissionSerializer, RoleSubMenuPermissionSerializer
from collections import defaultdict
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenSerializer

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ blacklist refresh token
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        user_data = []

        for u in users:
            user_data.append({
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": {
                    "id": u.role.id if u.role else None,
                    "name": u.role.name if u.role else None
                },
            })

        return Response(user_data)


class SidebarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.user.role

        if not role:
            return Response({"menus": []})

        # ✅ STEP 1: MENUS (ORDERED)
        allowed_menus = RoleMenuPermission.objects.filter(
            role=role,
            can_view=True
        ).select_related("menu").order_by("menu__order")

        if not allowed_menus.exists():
            return Response({"menus": []})

        menu_dict = {}

        for rm in allowed_menus:
            menu = rm.menu
            menu_dict[menu.id] = {
                "id": menu.id,
                "name": menu.name,
                "icon": request.build_absolute_uri(menu.icon.url) if menu.icon else None,
                "submenus": []
            }

        # ✅ STEP 2: SUBMENU PERMISSIONS
        allowed_submenus = RoleSubMenuPermission.objects.filter(
            role=role,
            can_view=True
        ).select_related("submenu__parent", "submenu__menu")

        # ✅ STEP 3: INCLUDE PARENTS
        def get_all_with_parents(perms):
            result = {}

            for perm in perms:
                s = perm.submenu
                result[s.id] = s

                parent = s.parent
                while parent:
                    result[parent.id] = parent
                    parent = parent.parent

            return list(result.values())

        submenu_objects = get_all_with_parents(allowed_submenus)

        # ✅ STEP 4: BUILD TREE WITH ORDER
        def build_tree(submenus):
            tree = []
            mapping = {}

            # 🔥 SORT FIRST
            submenus = sorted(submenus, key=lambda x: x.order)

            for s in submenus:
                mapping[s.id] = {
                    "id": s.id,
                    "name": s.name,
                    "path": s.path,
                    "order": s.order,
                    "children": [],
                    "menu_id": s.menu.id
                }

            for s in submenus:
                if s.parent_id and s.parent_id in mapping:
                    mapping[s.parent_id]["children"].append(mapping[s.id])
                else:
                    tree.append(mapping[s.id])

            # 🔥 SORT CHILDREN ALSO
            for item in mapping.values():
                item["children"] = sorted(item["children"], key=lambda x: x["order"])

            return tree

        submenu_tree = build_tree(submenu_objects)

        # ✅ STEP 5: ATTACH TO MENUS
        for menu in menu_dict.values():
            menu["submenus"] = [
                s for s in submenu_tree if s["menu_id"] == menu["id"]
            ]

        return Response({
            "menus": list(menu_dict.values()),
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "role": request.user.role.name if request.user.role else None,
                "user_id": request.user.id,
                "default_path": request.user.default_submenu.path if request.user.default_submenu else "/dashboard"
            }
        })


# 1️⃣ User List API
class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# 2️⃣ User Menu Permissions API
class UserMenuPermissionAPI(generics.ListAPIView):
    serializer_class = RoleMenuPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role:
            return RoleMenuPermission.objects.filter(role=user.role, can_view=True)
        return RoleMenuPermission.objects.none()

# 3️⃣ User SubMenu Permissions API
class UserSubMenuPermissionAPI(generics.ListAPIView):
    serializer_class = RoleSubMenuPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role:
            return RoleSubMenuPermission.objects.filter(role=user.role, can_view=True)
        return RoleSubMenuPermission.objects.none()
    
class UserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ToggleUserStatusAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = not user.is_active
            user.save()
            return Response({"message": "Status updated"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)



class MenuListCreateAPI(generics.ListCreateAPIView):
    queryset = Menu.objects.prefetch_related('submenus__children').all().order_by('order')
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

class MenuDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

# views.py
class SubMenuListCreateAPI(generics.ListCreateAPIView):
    queryset = SubMenu.objects.all()
    serializer_class = SubMenuSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubMenuDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubMenu.objects.all()
    serializer_class = SubMenuSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserCreateAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleSubMenuPermissionListCreateAPI(generics.ListCreateAPIView):
    queryset = RoleSubMenuPermission.objects.all()
    serializer_class = RoleSubMenuPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleSubMenuPermissionDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleSubMenuPermission.objects.all()
    serializer_class = RoleSubMenuPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleListAPI(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

# views.py
class RoleMenuPermissionListCreateAPI(generics.ListCreateAPIView):
    queryset = RoleMenuPermission.objects.all()
    serializer_class = RoleMenuPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleMenuPermissionDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleMenuPermission.objects.all()
    serializer_class = RoleMenuPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]







import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

import requests
import json
import hashlib
import hmac
import base64
from pathlib import Path
from . import global_app_settings


@api_view(['GET'])
def dashboards(request):
    """Return list of dashboards (ItemType=2) by calling Bold BI REST API server-side.
    This avoids CORS and exposing embed secrets in the browser for the sample.
    """
    try:
        cfg_path = Path(__file__).resolve().parents[1] / 'embedConfig.json'
        with open(cfg_path, 'r', encoding='utf-8-sig') as f:
            cfg = json.load(f)
        embed = cfg.get('EmbedDetails', cfg)

        server_url = (embed.get('ServerUrl') or embed.get('serverUrl') or embed.get('serverurl') or '').rstrip('/')
        site_identifier = embed.get('SiteIdentifier') or embed.get('siteIdentifier') or embed.get('siteidentifier')
        embed_secret = embed.get('EmbedSecret') or embed.get('embedSecret') or embed.get('embedsecret')
        user_email = embed.get('UserEmail') or embed.get('userEmail') or embed.get('email')

        if not server_url or not site_identifier:
            return JsonResponse({'error': 'Missing ServerUrl or SiteIdentifier in embedConfig.json'}, status=500)

        # Request API token using embed_secret grant
        token_url = f"{server_url}/api/{site_identifier}/token"
        token_payload = {
            'username': user_email,
            'embed_secret': embed_secret,
            'grant_type': 'embed_secret'
        }
        token_res = requests.post(token_url, data=token_payload, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=30)
        token_res.raise_for_status()
        token_json = token_res.json()
        access_token = token_json.get('access_token') or (token_json.get('Data') or {}).get('access_token')
        if not access_token:
            return JsonResponse({'error': 'Could not obtain access token', 'detail': token_json}, status=502)

        # Get dashboards (ItemType=2)
        items_url = f"{server_url}/api/{site_identifier}/v2.0/items?ItemType=2"
        items_res = requests.get(items_url, headers={'Authorization': f'bearer {access_token}'}, timeout=30)
        items_res.raise_for_status()
        return JsonResponse(items_res.json(), safe=False)
    except Exception as e:
        return JsonResponse({'error': 'dashboards error', 'details': str(e)}, status=500)

def index(request):
    return render(request,'index.html')

@api_view(['GET'])
def getdetails(request):
    # Read embedConfig.json at request time so changes are picked up immediately.
    try:
        cfg_path = Path(__file__).resolve().parents[1] / 'embedConfig.json'
        with open(cfg_path, 'r', encoding='utf-8-sig') as f:
            cfg = json.load(f)
        embed = cfg.get('EmbedDetails', cfg)

        # Normalize keys (allow multiple casing variants)
        server_url = embed.get('ServerUrl') or embed.get('serverUrl') or embed.get('serverurl')
        site_identifier = embed.get('SiteIdentifier') or embed.get('siteIdentifier') or embed.get('siteidentifier')
        embed_secret = embed.get('EmbedSecret') or embed.get('embedSecret') or embed.get('embedsecret')
        user_email = embed.get('UserEmail') or embed.get('userEmail') or embed.get('email')
        dashboard_id = embed.get('DashboardId') or embed.get('dashboardId') or (embed.get('Dashboard') or {}).get('id')
        embed_type = embed.get('EmbedType') or embed.get('embedType') or embed.get('embedtype')
        environment = embed.get('Environment') or embed.get('environment')

        return JsonResponse({
            'DashboardId': dashboard_id,
            'ServerUrl': server_url,
            'EmbedType': embed_type,
            'Environment': environment,
            'SiteIdentifier': site_identifier,
            'UserEmail': user_email,
            'EmbedSecret': embed_secret,
        })
    except Exception as e:
        return JsonResponse({'error': 'Could not load embed details', 'details': str(e)}, status=500)

@api_view(['POST'])
def tokenGeneration(request):
    try:
        cfg_path = Path(__file__).resolve().parents[1] / 'embedConfig.json'
        with open(cfg_path, 'r', encoding='utf-8-sig') as f:
            cfg = json.load(f)
        embed = cfg.get('EmbedDetails', cfg)

        server_url = embed.get('ServerUrl') or embed.get('serverUrl') or embed.get('serverurl')
        site_identifier = embed.get('SiteIdentifier') or embed.get('siteIdentifier') or embed.get('siteidentifier')
        embed_secret = embed.get('EmbedSecret') or embed.get('embedSecret') or embed.get('embedsecret')
        user_email = embed.get('UserEmail') or embed.get('userEmail') or embed.get('email')
        dashboard_id = embed.get('DashboardId') or embed.get('dashboardId') or (embed.get('Dashboard') or {}).get('id')

        embed_details = {
            'email': user_email,
            'serverurl': server_url,
            'siteidentifier': site_identifier,
            'embedsecret': embed_secret,
            'dashboard': { 'id': dashboard_id }
        }

        request_url = f"{embed_details['serverurl'].rstrip('/')}/api/{embed_details['siteidentifier']}/embed/authorize"
        headers = {'Content-Type': 'application/json'}

        result = requests.post(request_url, headers=headers, data=json.dumps(embed_details), timeout=30)
        result.raise_for_status()

        data = result.json()
        try:
            return HttpResponse(data.get('Data', {}).get('access_token') or data.get('token'))
        except (KeyError, TypeError):
            return HttpResponse(f"Unexpected response format: {data}", status=502)
    except Exception as e:
        return HttpResponse(str(e), status=500)
