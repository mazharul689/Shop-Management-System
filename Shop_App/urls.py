from django.urls import path
from . import views

urlpatterns = [
    # Map the root URL directly to your dashboard router
    path('', views.dashboard_router, name='home'),

    # Universal traffic checkpoint after a successful login
    path('dashboard/', views.dashboard_router, name='dashboard'),

    # Standard Authentication Routes (Kept exactly as before)
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    
    # Clean, role-prefixed dashboard workspaces
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('shopkeeper/dashboard/', views.shopkeeper_dashboard, name='shopkeeper_dashboard'),

    # Master data 
    path('admin/categories/', views.category_list, name='category_list'),
    path('admin/brands/', views.brand_list, name='brand_list'),
    path('admin/units/', views.unit_list, name='unit_list'),
    path('admin/products/', views.product_list, name='product_list'),
    path('admin/suppliers/', views.supplier_list, name='supplier_list'),
    path('admin/purchases/', views.purchase_list, name='purchase_list'),
    path('admin/purchases/new/', views.purchase_create, name='purchase_create'),
]