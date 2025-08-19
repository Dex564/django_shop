from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs): # норм имена вместо артикулов
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.name #как будет отображаться в админке
    

class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='product_size')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.size.name} ({self.stock} in stock) for {self.product.name}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products') #category получает все поля которые есть в классе Category, on_delete это плашка с вопросом о удалении уверены или нет, related name - как будет отображаться в админке
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) # в отличии от IntegerField decimal позволяет адекватно считать скидки
    descripation = models.TextField(blank=True) #blank = true значит что данные поля могут быть пустыми в заполнении админки 
    main_image = models.ImageField(upload_to='products/main/') # так как в сеттингах указали media, то фотки пойдут сначала в папку медиа, а потом и туда куда указали
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs): # норм имена вместо артикулов
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/extra/')