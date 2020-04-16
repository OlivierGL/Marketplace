from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from Users import models as user_models
from django.http import HttpResponseRedirect
from django.contrib import messages

no_product_error_message = "Sorry, no {} are available for now."


# Create your views here.
def home(request):
    context = {
        'category': "all products",
        'items': models.Product.objects.filter(quantity__gt=0),
        'activeNavItem': "browse/all",
        'noProductErrorMessage': no_product_error_message.format("products")
    }
    return render(request, 'Market/browse.html', context)


def paintings(request):
    context = {
        'category': "Paintings",
        'items': models.Product.objects.filter(category="PAINTING", quantity__gt=0),
        'activeNavItem': "browse/paintings",
        'noProductErrorMessage': no_product_error_message.format("paintings")
    }
    return render(request, 'Market/browse.html', context)


def sculptures(request):
    context = {
        'category': "Sculptures",
        'items': models.Product.objects.filter(category="SCULPTURE", quantity__gt=0),
        'activeNavItem': "browse/sculptures",
        'noProductErrorMessage': no_product_error_message.format("sculptures")
    }
    return render(request, 'Market/browse.html', context)


def clothes(request):
    context = {
        'category': "Clothes",
        'items': models.Product.objects.filter(category="GARMENT", quantity__gt=0),
        'activeNavItem': "browse/clothes",
        'noProductErrorMessage': no_product_error_message.format("clothes")
    }
    return render(request, 'Market/browse.html', context)


def jewelry(request):
    context = {
        'category': "Jewelry",
        'items': models.Product.objects.filter(category="JEWELRY", quantity__gt=0),
        'activeNavItem': "browse/jewelry",
        'noProductErrorMessage': no_product_error_message.format("jewelry")
    }
    return render(request, 'Market/browse.html', context)


def glass_art(request):
    context = {
        'category': "Glass Art",
        'items': models.Product.objects.filter(category="GLASS_ART", quantity__gt=0),
        'activeNavItem': "browse/glass_art",
        'noProductErrorMessage': no_product_error_message.format("glass art")
    }
    return render(request, 'Market/browse.html', context)


@login_required
def cart(request):
    current_user = user_models.UserInfo.objects.get(user=request.user)

    cart_products = models.CartProduct.objects.filter(cart=current_user.cart, quantity__gt=0)

    total = 0
    for cart_product in cart_products:
        product_total_price = cart_product.product.price * cart_product.quantity
        total += product_total_price

    context = {'CartProducts': cart_products, 'total': total}
    return render(request, 'Market/cart.html', context)


def product(request, primary_key):
    product_db = models.Product.objects.get(pk=primary_key)
    previous_url = request.META.get("HTTP_REFERER") or ""
    if request.user.is_authenticated:
        current_user = models.UserInfo.objects.get(user=request.user)
        product_in_cart = current_user.cart.cart_products.filter(product=product_db, quantity__gt=0).first()
        user_is_artist = request.user.id == product_db.artist.user.id
    else:
        current_user = None
        product_in_cart = None
        user_is_artist = False

    context = {'product': product_db,
               'current_user': current_user,
               'product_in_cart': product_in_cart,
               'user_is_artist': user_is_artist,
               'previous': previous_url}
    return render(request, 'Market/product.html', context)


def add_product(request, pk):
    context = {}
    if request.method == 'POST':
        add_product_form = forms.AddProductForm(request.POST, request.FILES)
        if add_product_form.is_valid():
            product = add_product_form.save(commit=False)
            product.artist = user_models.UserInfo.objects.get(user=request.user)
            product.save()

            messages.success(request, 'Product Added Successfuly')
            return HttpResponseRedirect('../')
        else:
            messages.error(request, 'Error: Product wasn\'t Added Successfuly')
            context['form'] = forms.AddProductForm()
            return render(request, 'Market/add_product.html', context)

    else:
        form = forms.AddProductForm()
        context['form'] = form
        return render(request, 'Market/add_product.html', context)
