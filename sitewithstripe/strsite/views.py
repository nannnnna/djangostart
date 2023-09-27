from django.shortcuts import render, redirect
from decimal import Decimal
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, Order, OrderItem

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


def order(request):
    # Получаем текущую корзину из сессии или создаем пустой список, если его еще нет
    cart = request.session.get('cart', [])
    
    # Вычисляем общую стоимость всех товаров в корзине
    total_price = sum(Decimal(item['price']) for item in cart)
    
    # Передаем общую стоимость в шаблон как total_order_amount
    context = {
        'cart': cart,
        'total_order_amount': total_price,  # Передаем общую стоимость заказа
    }
    return render(request, 'order.html', context)

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    quantity = int(request.GET.get('quantity', item.quantity))
    
    # Извлекаем текущую информацию о корзине из сессии или создаем пустой список, если его еще нет
    cart = request.session.get('cart', [])
    
    # Создаем словарь для текущего товара и добавляем его в корзину
    item_data = {
        'name': item.name,
        'price': str(item.price * quantity),  # Преобразуем Decimal в строку
        'quantity': quantity
    }
    cart.append(item_data)
    
    # Сохраняем обновленную корзину в сессии
    request.session['cart'] = cart
    request.session.modified = True  # Убедитесь, что сессия будет сохранена
    
    return redirect('order')
@csrf_exempt
def create_order_session(request):
    try:
        total_amount = request.GET.get("total_order_amount")  # Изменено на "total_order_amount"

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Total Order",
                        },
                        "unit_amount": int(float(total_amount) * 100),  # Преобразуем в центы
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://yourwebsite.com/success",  # Замените на URL вашей успешной страницы
            cancel_url="http://yourwebsite.com/cancel",    # Замените на URL вашей страницы отмены
        )

        return JsonResponse({"session_id": session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


