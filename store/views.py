from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Código para el dashboard del administrador
    return render(request, 'admin_dashboard.html')

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True
        ).order_by("id")
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        "products": paged_products,
        "product_count": product_count,
    }

    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product__id=single_product.id
            ).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product__id=single_product.id, status=True)

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "orderproduct": orderproduct,
        "reviews": reviews,
        "product_gallery": product_gallery,
    }

    return render(request, "store/product_detail.html", context)


def search(request):
    # Inicializar variables
    products = Product.objects.all()
    product_count = 0

    # Obtener parámetros de búsqueda de la URL
    keyword = request.GET.get("keyword", "")  # Palabra clave
    category_id = request.GET.get("category", None)  # Categoría seleccionada

    # Filtrar por palabra clave
    if keyword:
        products = products.filter(
            Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
        )

    # Filtrar por categoría
    if category_id:
        products = products.filter(category__id=category_id)

    # Contar productos filtrados
    product_count = products.count()

    # Obtener todas las categorías para el filtro en el formulario
    categories = Category.objects.all()

    context = {
        "products": products,
        "product_count": product_count,
        "categories": categories,
        "keyword": keyword,  # Para mantener la palabra clave en el formulario
        "category_id": category_id,  # Para mantener la categoría seleccionada
    }

    return render(request, "store/store.html", context)


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(
                request, "Muchas gracias!, tu comentario ha sido actualizado."
            )
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, "Muchas gracias!, tu comentario ha sido publicado."
                )
                return redirect(url)
            
def product_list(request):
    products = Product.objects.all()
    
    # Filtrado
    category = request.GET.get('category')
    if category:
        products = products.filter(category__name=category)

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min and price_max:
        products = products.filter(price__gte=price_min, price__lte=price_max)

    brand = request.GET.get('brand')
    if brand:
        products = products.filter(brand__iexact=brand)
    
    energy_rating = request.GET.get('energy_rating')
    if energy_rating:
        products = products.filter(energy_rating=energy_rating)

    return render(request, 'store/product_list.html', {'products': products})

