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


