from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem, Product
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_id = order.order_total,
        status = body['status'],
    )

    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variation.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()

    mail_subject = 'Tu compra fue realizada!'
    body = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })

    to_email = request.user.email
    send_email = EmailMessage(mail_subject, body, to=[to_email])
    send_email.send()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }


    return JsonResponse(data)


# Create your views here.
# Vista para la creación de la orden
def place_order(request):
    # Verifica si el carrito tiene productos
    if not request.session.get('cart_items'):
        messages.error(request, "No hay productos en tu carrito.")
        return redirect('cart')  # Redirige al carrito si no hay productos

    # Procesar el formulario de dirección de envío
    if request.method == "POST":
        # Recoge la información del formulario
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        order_note = request.POST.get('order_note')

        # Obtener los productos del carrito (asegurándose que haya datos)
        cart_items = json.loads(request.POST.get('cart_items'))
        if not cart_items:
            messages.error(request, "No se han encontrado productos en el carrito.")
            return redirect('cart')

        # Crear la orden
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            country=country,
            city=city,
            state=state,
            order_note=order_note,
            status='pending',  # Puedes cambiar el estado según tu flujo
        )

        # Crear los detalles de la orden (productos)
        total = 0
        for item in cart_items:
            product = Product.objects.get(id=item['product_id'])
            quantity = item['quantity']
            sub_total = product.price * quantity
            total += sub_total

            CartItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
                sub_total=sub_total,
            )

        # Aquí puedes calcular impuestos y otros costos
        tax = total * 0.16  # 16% de IVA (puedes modificar este valor según tus necesidades)
        grand_total = total + tax

        # Actualiza el total de la orden con los impuestos
        order.total = total
        order.tax = tax
        order.grand_total = grand_total
        order.save()

        # Eliminar los productos del carrito después de crear la orden
        del request.session['cart_items']

        # Redirigir a la página de confirmación de la orden
        return redirect('order_complete', order_number=order.order_number)

    # Si la petición es GET, simplemente mostrar el formulario
    return render(request, 'place_order.html', {
        'cart_items': request.session.get('cart_items', []),  # Obtiene los productos del carrito
    })
