from django.db import models
from datetime import datetime
from django.utils.text import slugify

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.TextField(max_length=500, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category' 
        verbose_name = 'Категорию'     
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name     


class Products(models.Model):
    name = models.CharField(max_length=150, unique=False, verbose_name='Название')
    slug = models.TextField(max_length=500, unique=False, blank=True, null=True, verbose_name='URL')
    discription = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='tovari_images', blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Скидка в %')    
    quantity = models.PositiveBigIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)



    def __str__(self):
        return f'{self.name} Количество - {self.quantity} {self.price}$' 
    
    def display_id(self):
        return f'№ {"_".join(f"_{self.id:05}_")}'

    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount/100, 2)
       
        return self.price