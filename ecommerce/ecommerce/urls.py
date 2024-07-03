"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from ecom import views

from django.contrib.auth import views as auth_views

urlpatterns = [         
    path('admin/', admin.site.urls),

    path('',views.userpublic_view,name='userhome'),
    path('userindex/',views.userindex_view,name='userindex'),
    path('search/',views.Search_View,name='search'),
    path('shop/<int:pk>',views.shop_view,name='shop'),
    path('contact/',views.contact,name='contact'),
    path('detail/<int:pk>',views.detail,name='detail'),
    path('myorder/',views.myorder_view,name='myorder'),

    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.Payment,name='payment'),
    path('order_confirm/',views.Order_Confirm,name='order_confirm'),
    path('cancel_payment/',views.Cancel_Payment,name='cancel_payment'),
    
    path('cart/',views.Cart_View,name='cart'),
    path('add-cart/<int:pk>',views.Add_Cart,name='add-cart'),
    path('remove-cart/<int:pk>',views.Remove_Cart,name='remove-cart'),
    path('update-cart/',views.Update_Cart,name='update-cart'),
    path('wishlist/',views.Wishlist_View,name='wishlist'),
    path('add-wishlist/<int:pk>',views.Add_Wishlist,name='add-wishlist'),
    path('remove-wishlist/<int:pk>',views.Remove_Wishlist,name='remove-wishlist'),

    path('address/',views.address_view,name='address'),
    path('add-address/',views.Add_Address,name='add-address'),
    path('edit-address/<int:pk>',views.Edit_Address,name='edit-address'),
    path('delete-address/<int:pk>',views.Delete_Address,name='delete-address'),

    path('admin-dashboard/',views.adminbase_view,name='adminbase'),
    path('admin-profile/',views.adminprofile_view,name='adminprofile'),
    path('admin-add-maincategory/',views.admin_add_maincategory_view,name='admin-add-maincategory'),
    path('delete-maincategory/<int:pk>',views.delete_maincategory_view,name='delete-maincategory'),
    path('update-maincategory/<int:pk>',views.update_category_view,name='update-maincategory'),
    path('admin-subcategory/',views.admin_subcategory_view,name='admin-subcategory'),
    path('admin-add-subcategory/',views.admin_add_subcategory_view,name='admin-add-subcategory'),
    path('delete-subcategory/<int:pk>',views.delete_subcategory_view,name='delete-subcategory'),
    path('update-subcategory/<int:pk>',views.update_subcategory_view,name='update-subcategory'),
    path('admin-add-product/',views.admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>',views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>',views.update_product_view,name='update-product'),
    path('admin-product/',views.admin_product_view,name='admin-product'),

    path('login/',views.Login_view,name='login'),
    path('signup/',views.Signup_view,name='signup'),
    path('logout/',views.Logout,name='logout'),
    path('social-auth/',include('social_django.urls',namespace='social')),
    path('profile/',views.Profile,name='profile'),

    path('reset_password/', views.password_reset_request, name='password_reset'),
    path('reset_password_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset_password_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)