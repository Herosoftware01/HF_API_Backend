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

# class SidebarView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         role = user.role

#         if not role:
#             return Response({
#                 "user": {"id": user.id, "username": user.username},
#                 "menus": []
#             })

#         # Step 1: Allowed menus
#         allowed_menus = RoleMenuPermission.objects.filter(
#             role=role, can_view=True
#         ).select_related('menu').order_by('menu__order')

#         if not allowed_menus.exists():
#             return Response({
#                 "user": {"id": user.id, "username": user.username},
#                 "menus": []
#             })

#         menu_dict = {}
#         for rm in allowed_menus:
#             menu = rm.menu
#             menu_dict[menu.id] = {
#                 "id": menu.id,
#                 "name": menu.name,
#                 "icon": request.build_absolute_uri(menu.icon.url) if menu.icon else None,
#                 "submenus": []
#             }

#         # Step 2: Allowed submenus
#         sub_permissions = RoleSubMenuPermission.objects.filter(
#             role=role,
#             can_view=True,
#             submenu__menu__in=[rm.menu for rm in allowed_menus]
#         ).select_related('submenu__menu').order_by('submenu__menu__order', 'submenu__id')

#         for perm in sub_permissions:
#             menu_id = perm.submenu.menu.id
#             menu_dict[menu_id]["submenus"].append({
#                 "id": perm.submenu.id,
#                 "name": perm.submenu.name,
#                 "path": perm.submenu.path
#             })

#         # Step 3: Sort submenus
#         for menu in menu_dict.values():
#             menu["submenus"] = sorted(menu["submenus"], key=lambda x: x["id"])

#         return Response({
#             "user": {"id": user.id, "username": user.username},
#             "menus": list(menu_dict.values())
#         })


class SidebarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        role_id = request.GET.get("role_id")

        # ✅ If role_id is passed → use that role
        if role_id:
            try:
                role = Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                return Response({"menus": []})
        else:
            # ✅ Otherwise use logged-in user role
            role = request.user.role

        if not role:
            return Response({"menus": []})

        # 🔹 Step 1: Allowed Menus
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

        # 🔹 Step 2: Allowed Submenus
        sub_permissions = RoleSubMenuPermission.objects.filter(
            role=role,
            can_view=True,
            submenu__menu__in=[rm.menu for rm in allowed_menus]
        ).select_related("submenu__menu").order_by(
            "submenu__menu__order",
            "submenu__id"
        )

        for perm in sub_permissions:
            menu_id = perm.submenu.menu.id

            if menu_id in menu_dict:
                menu_dict[menu_id]["submenus"].append({
                    "id": perm.submenu.id,
                    "name": perm.submenu.name,
                    "path": perm.submenu.path
                })

        # 🔹 Sort Submenus
        for menu in menu_dict.values():
            menu["submenus"] = sorted(menu["submenus"], key=lambda x: x["id"])

        return Response({
            "menus": list(menu_dict.values()),
            "user": {
                "id": request.user.id,
                "username": request.user.username
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


# views.py
class MenuListCreateAPI(generics.ListCreateAPIView):
    queryset = Menu.objects.all().order_by('order')
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