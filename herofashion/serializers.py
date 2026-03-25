from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from rest_framework import generics, permissions
# from rest_framework_recursive.fields import RecursiveField


class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role.name if user.role else None
        return token


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]   


class UserSerializer(serializers.ModelSerializer):

    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source="role",
        write_only=True,
        required=False
    )

    role = serializers.SerializerMethodField(read_only=True)

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "role_id",
            "is_active",
            "date_joined",
            "password",
        ]

    def get_role(self, obj):
        return obj.role.name if obj.role else None

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


# SubMenu Serializer
# class SubMenuSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubMenu
#         fields = ["id", "menu", "name", "path"]

class SubMenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = SubMenu
        fields = ('id', 'name', 'path', 'children', 'menu_id')

    def get_children(self, obj):
        children = obj.children.all()
        if not children.exists():
            return []
        return SubMenuSerializer(children, many=True, context=self.context).data

        # Menu Serializer
# class MenuSerializer(serializers.ModelSerializer):
#     submenus = SubMenuSerializer(many=True, read_only=True)

#     class Meta:
#         model = Menu
#         fields = ["id", "name", "icon", "order", "submenus"]


class MenuSerializer(serializers.ModelSerializer):
    submenus = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "name", "icon", "order", "submenus"]

    def get_submenus(self, obj):
        top_level = obj.submenus.filter(parent__isnull=True)
        return SubMenuSerializer(top_level, many=True, context=self.context).data



class RoleMenuPermissionSerializer(serializers.ModelSerializer):
    # Accept IDs for write operations
    menu_id = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(), source='menu', write_only=True
    )
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )

    # Keep read-only nested data for GET requests
    menu = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RoleMenuPermission
        fields = ["id", "role", "menu", "can_view", "menu_id", "role_id"]

    def get_menu(self, obj):
        return {
            "id": obj.menu.id,
            "name": obj.menu.name,
            "order": obj.menu.order
        }

    def get_role(self, obj):
        return {
            "id": obj.role.id,
            "name": obj.role.name
        }

    
class RoleSubMenuPermissionSerializer(serializers.ModelSerializer):
    # write fields
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source="role",
        write_only=True
    )

    submenu_id = serializers.PrimaryKeyRelatedField(
        queryset=SubMenu.objects.all(),
        source="submenu",
        write_only=True
    )

    # read fields
    role = serializers.SerializerMethodField(read_only=True)
    submenu = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = RoleSubMenuPermission
        fields = [
            "id",
            "role",
            "submenu",
            "can_view",
            "role_id",
            "submenu_id",
        ]

    def get_role(self, obj):
        return {
            "id": obj.role.id,
            "name": obj.role.name
        }

    def get_submenu(self, obj):
        return {
            "id": obj.submenu.id,
            "name": obj.submenu.name,
            "menu_id": obj.submenu.menu.id
        }