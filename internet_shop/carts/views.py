from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from carts.utils import get_user_carts
from .models import Cart

from tovari.models import Products
from django.template.loader import render_to_string

def cart_add(request):

    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
            
    user_cart = get_user_carts(request)

    cart_items_html = render_to_string(
        "carts/includes/incleded_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def cart_add(request):

    product_id = request.POST.get("product_id")

    product = get_object_or_404(Products, id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, product=product
        )
        if not created:
            cart.quantity += 1
            cart.save()

    user_cart = get_user_carts(request)

    total_quantity = sum(item.quantity for item in user_cart)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Товар успешно добавлен в корзину",
        "cart_items_html": cart_items_html,
        "total_quantity": total_quantity,
    }

    return JsonResponse(response_data)






def cart_change(request) -> JsonResponse:
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    cart_items = get_user_carts(request).order_by('id')  

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": cart_items}, request=request
    )

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity,
    }

    return JsonResponse(response_data)




def cart_remove(request):
    cart_id = request.POST.get('cart_id')
    cart = get_object_or_404(Cart, id=cart_id)

    cart.delete()

    user_cart = get_user_carts(request)

    total_quantity = sum(item.quantity for item in user_cart)
    total_price = sum(item.quantity * item.product.sell_price() for item in user_cart)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Товар удален из корзины",
        "cart_items_html": cart_items_html,
        "total_quantity": total_quantity,  
        "total_price": total_price,        
    }

    return JsonResponse(response_data)