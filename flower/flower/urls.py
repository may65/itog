# flower/urls.py
# from django.contrib import admin
# from django.urls import path, include
# # from users.views import home
# # import users
# # from users.views import home, RegisterView
# # import views
# from django.contrib.auth.views import LoginView
# from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
# from django.urls import path
# from django.contrib import admin
# # from order.views import add_to_cart
#
# urlpatterns = [
#     path('', include('users.urls'), name='home'),
#     path('admin/', admin.site.urls, name='admin'),
#     path('catalog/', include('catalog.urls'), name='catalog'),
#     path('order/', include('order.urls'), name='order'),
#     # path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     # path('add_to_cart/', add_to_cart, name='add_to_cart'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

app_name = "flower"  # Пространство имен для организации URL

urlpatterns = [
    path('users/', include('users.urls'), name='home'),
    path('admin/', admin.site.urls),
    # path('flower/', include('flower.urls')),  # Все URL приложения flower
    # path('accounts/', include('django.contrib.auth.urls')),  # Для авторизации
    # Главная страница с каталогом товаров
    path('', views.product_list, name='product_list'),
    # Работа с корзиной
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # Оформление заказа (только для авторизованных)
    path('create-order/', views.create_order, name='create_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)