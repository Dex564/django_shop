from django.contrib import admin
from .models import Category, Size, Product, \
ProductImage, ProductSize
# Register your models here.


class ProductImageInline(admin.TabularInline): # я так понял по ролику (на 38:30 он говорит), это нужно для того, чтобы тут например, ProductSize и Product выводились вместе, а не отдельно 
    model = ProductImage
    extra = 1  # это значит сколько полей будет изначально в админ меню в выборе картинок

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'color', 'price'] #лист не в админке
    list_filter = ['category', 'color']
    search_fields = ['name', 'color', 'description']
    prepopulated_fields = {'slug': ('name',)}    #констукция, которая позволяет нам заполнять нужные нам параметры из того что у нас есть, ЗАПЯТАЯ НА КОНЦЕ КОРТЕЖА ОБЯЗАТЕЛЬНА при одной перемеенной в кортеже
    inlines = [ProductImageInline, ProductSizeInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product, ProductAdmin) # Зарегать можно так, а можно и через декоратор, оба примера будут
admin.site.register(Size, SizeAdmin) # Если кратко: мы берём какую-то модель (тут Size) и привязываем??? к ней настройки, которые мы прописали (тут SizeAdmin)
admin.site.register(Category, CategoryAdmin)