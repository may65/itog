# flower\admin.py
from django.contrib import admin
from .models import * #Product
# from django.utils.html import formathtml


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    listdisplay = ('id', 'name', 'price', 'createdat', 'imagepreview') # Добавляем imagepreview в список отображения
    listfilter = ('createdat',)
    searchfields = ('name', 'description')

    readonlyfields = ('imagepreview',)
#
#     def imagepreview(self): # Создаем метод для отображения превью изображения
#         if self.image:
#             pass
#             # return formathtml('<img src="{}" width="150" height="150" />', self.image.url)
#         return 'No Image'
#     imagepreview.shortdescription = 'Image Preview'
admin.site.register(Order)
admin.site.register(OrderItem)