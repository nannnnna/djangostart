from django.shortcuts import render

# Create your views here.
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Item

stripe.api_key = "sk_test_51NsTBiF6oMer2mpJqJr6mXh8S7GiJLXsPzRXgiVbFnMqxHVrPiBgiQzpZRwmhXNQ14lM7Scia0c4GddMZk0HYfxX0036Nvr5fy"  # Замените на ваш ключ Stripe

@csrf_exempt
def get_session_id(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    quantity = int(request.GET.get('quantity', item.quantity))  # Получаем количество товара из запроса, по умолчанию 1
    item_price = int(item.price * 100)  # Преобразуем цену в центы
    total_price = quantity * item_price
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": item_price,  # Сумма в центах
                },
                "quantity": quantity,
            }
        ],
        mode="payment",
        success_url="http://yourwebsite.com/success",  # Замените на URL вашей успешной страницы
        cancel_url="http://yourwebsite.com/cancel",    # Замените на URL вашей страницы отмены
    )
    return JsonResponse({"session_id": session.id})


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'item_detail.html', {'item': item})


def item_list(request):
    items = Item.objects.all()  # Получаем все товары из базы данных
    return render(request, 'item_list.html', {'items': items})