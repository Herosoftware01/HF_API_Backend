from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Auth
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()), 

    # Sidebar
    path('sidebar/', SidebarView.as_view()),

    # Users
    path('users-create/', UserCreateAPI.as_view()),
    path("users-list/", UserListAPI.as_view(), name="user-list"),  # GET: list all users
    path("users-list-view/", UserListView.as_view(), name="user-list-view"),  # GET: list all users
    path("users/create/", UserCreateAPI.as_view(), name="user-create"),  # POST: create user
    path("users/<int:pk>/", UserDetailAPI.as_view(), name="user-detail"),  # GET/PUT/DELETE
    path("users/<int:pk>/toggle-status/", ToggleUserStatusAPI.as_view(), name="user-toggle-status"),
    path("roles/", RoleListAPI.as_view(), name="roles-list"),
    # User permissions
    path("user-menu-permissions/", UserMenuPermissionAPI.as_view(), name="user-menu-permissions"),
    path("user-submenu-permissions/", UserSubMenuPermissionAPI.as_view(), name="user-submenu-permissions"),

    # Menus
    path("menus/", MenuListCreateAPI.as_view(), name="menu-list-create"),
    path("menus/<int:pk>/", MenuDetailAPI.as_view(), name="menu-detail"),

    # SubMenus
    path("submenus/", SubMenuListCreateAPI.as_view(), name="submenu-list-create"),
    path("submenus/<int:pk>/", SubMenuDetailAPI.as_view(), name="submenu-detail"),

    # Role permissions
    path("role-menu-permissions/", RoleMenuPermissionListCreateAPI.as_view(), name="role-menu-permissions-list-create"),
    path("role-menu-permissions/<int:pk>/", RoleMenuPermissionDetailAPI.as_view(), name="role-menu-permissions-detail"),
    path("role-submenu-permissions/", RoleSubMenuPermissionListCreateAPI.as_view(), name="role-submenu-permissions-list-create"),
    path("role-submenu-permissions/<int:pk>/", RoleSubMenuPermissionDetailAPI.as_view(), name="role-submenu-permissions-detail"),
]