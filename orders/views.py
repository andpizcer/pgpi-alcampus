from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem, Cart
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.models import Account


def payments(request):
    body = json.loads(request.body)
    if request.user.is_authenticated:
        order = Order.objects.get(
            user=request.user, is_ordered=False, order_number=body["orderID"]
        )
    else:
        order = Order.objects.get(
            user=Account.objects.get(username="anonymus"),
            is_ordered=False,
            order_number=body["orderID"],
        )

    payment = Payment(
        user=order.user,
        payment_id=body["transID"],
        payment_method=body["payment_method"],
        amount_id=order.order_total,
        status=body["status"],
    )

    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=order.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = order.user.id
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

    CartItem.objects.filter(user=order.user).delete()

    ordered_products = OrderProduct.objects.filter(order_id=order.id)

    mail_subject = "Tu compra fue realizada!"
    body = render_to_string(
        "orders/order_recieved_email.html",
        {
            "order": order,
            "ordered_products": ordered_products,
            "order_number": order.order_number,
            "transID": payment.payment_id,
            "payment": payment,
            "subtotal": order.order_total - order.tax,
        },
    )

    to_email = order.email
    send_email = EmailMessage(
        mail_subject, body, to=[to_email], from_email="gestor.alcampus@gmail.com"
    )
    send_email.content_subtype = "html"
    send_email.send()

    data = {
        "order_number": order.order_number,
        "transID": payment.payment_id,
    }

    return JsonResponse(data)


def _cart_id(request):
    """Helper function to get the cart ID from the session."""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Create your views here.
def place_order(request, total=0, quantity=0):
    if request.user.is_authenticated:
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    # Verificar si hay artículos en el carrito
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")

    grand_total = 0
    tax = 0

    # Calcular el total y la cantidad
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = round((16 / 100) * total, 2)
    grand_total = total + tax

    # Restringir usuarios no registrados si tienen 4 o más productos
    if not request.user.is_authenticated and quantity >= 4:
        return redirect("login")

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            # Crear una nueva orden
            data = Order()
            if request.user.is_authenticated:
                data.user = current_user
            else:
                data.user = Account.objects.get(
                    username="anonymus"
                )  # Usuario no registrado
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.city = form.cleaned_data["city"]
            data.state = form.cleaned_data["state"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()

            # Generar número de orden único
            yr = int(datetime.date.today().strftime("%Y"))
            mt = int(datetime.date.today().strftime("%m"))
            dt = int(datetime.date.today().strftime("%d"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # Contexto para la plantilla de pago
            context = {
                "order": data,
                "cart_items": cart_items,
                "total": total,
                "tax": tax,
                "grand_total": grand_total,
            }

            return render(request, "orders/payments.html", context)

    else:
        return redirect("checkout")


def order_complete(request):
    order_number = request.GET.get("order_number")
    transID = request.GET.get("payment_id")

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            "order": order,
            "ordered_products": ordered_products,
            "order_number": order.order_number,
            "transID": payment.payment_id,
            "payment": payment,
            "subtotal": subtotal,
        }

        return render(request, "orders/order_complete.html", context)

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect("home")
