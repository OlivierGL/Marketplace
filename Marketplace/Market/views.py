from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from Users import models as user_models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

no_product_error_message = "Sorry, no {} are available for now."


# Create your views here.
def home(request):
    return render(request, 'Market/home.html', {'activeNavItem': 'home'})


def paintings(request):
    # made up item to demo the browser template.
    items = [{
        'pk': 1,
        'name': 'The Creation of the Sun and the Moon',
        'description': "It is one of the frescoes from Michelangelo's nine Books of Genesis scenes on the Sistine Chapel ceiling.",
        'quantity': '3',
        'image': 'Market/thecreation.jpg',
        'price': '4300'}, {
        'pk': 2,
        'name': 'Self-portrait',
        'description': "Most probably, van Gogh's self-portraits are depicting the face as it appeared in the mirror he used to reproduce his face, i.e. his right side in the image is in reality the left side of his face.",
        'quantity': '2',
        'image': 'Market/selfportrait.jpg',
        'price': '2000'}, {
        'pk': 3,
        'name': 'Mona Lisa',
        'description': "The best known, the most visited, the most written about, the most sung about, the most parodied work of art in the world",
        'quantity': '7',
        'image': 'Market/monalisa.jpg',
        'price': '1864'}, {
        'pk': 4,
        'name': 'The Scream',
        'description': "The agonised face in the painting has become one of the most iconic images of art, seen as symbolising the anxiety of the human condition.",
        'quantity': '1',
        'image': 'Market/scream.jpg',
        'price': '4300'}, {
        'pk': 5,
        'name': 'The Kiss',
        'description': "The Kiss (in German Der Kuss) is an oil-on-canvas painting with added gold leaf, silver and platinum, by the Austrian Symbolist painter Gustav Klimt. It was painted at some point in 1907 and 1908, during the height of what scholars call his 'Golden Period'.",
        'quantity': '11',
        'image': 'Market/thekiss.jpg',
        'price': '1000'},
    ]
    context = {
        'category': "Paintings",
        'items': models.Product.objects.filter(category="PAINTING"),
        'activeNavItem': "browse/paintings",
        'noProductErrorMessage': no_product_error_message.format("paintings")
    }
    return render(request, 'Market/browse.html', context)


def sculptures(request):
    context = {
        'category': "Sculptures",
        'items': models.Product.objects.filter(category="SCULPTURE"),
        'activeNavItem': "browse/sculptures",
        'noProductErrorMessage': no_product_error_message.format("sculptures")
    }
    return render(request, 'Market/browse.html', context)


def clothes(request):
    context = {
        'category': "Clothes",
        'items': models.Product.objects.filter(category="GARMENT"),
        'activeNavItem': "browse/clothes",
        'noProductErrorMessage': no_product_error_message.format("clothes")
    }
    return render(request, 'Market/browse.html', context)


def jewelry(request):
    context = {
        'category': "Jewelry",
        'items': models.Product.objects.filter(category="JEWELRY"),
        'activeNavItem': "browse/jewelry",
        'noProductErrorMessage': no_product_error_message.format("jewelry")
    }
    return render(request, 'Market/browse.html', context)


def glass_art(request):
    context = {
        'category': "Glass Art",
        'items': models.Product.objects.filter(category="GLASS_ART"),
        'activeNavItem': "browse/glass_art",
        'noProductErrorMessage': no_product_error_message.format("glass art")
    }
    return render(request, 'Market/browse.html', context)


@login_required
def cart(request):
    current_user = user_models.UserInfo.objects.get(user=request.user)

    cart_products = models.CartProduct.objects.filter(cart=current_user.cart)

    total = 0
    for cart_product in cart_products:
        product_total_price = cart_product.product.price * cart_product.quantity
        total += product_total_price

    context = {'CartProducts': cart_products, 'total': total}
    return render(request, 'Market/cart.html', context)


def product(request, primary_key):
    product_db = models.Product.objects.get(pk=primary_key)
    if request.user.is_authenticated:
        current_user = models.UserInfo.objects.get(user=request.user)
        user_is_artist = request.user.id == product_db.artist.user.id
    else:
        current_user = None
        user_is_artist = False

    context = {'product': product_db,
               'current_user': current_user,
               'user_is_artist': user_is_artist}
    return render(request, 'Market/product.html', context)


def add_product(request):
    context = {}
    if request.method == 'POST':
        add_product_form = forms.AddProductForm(request.POST, request.FILES)
        if add_product_form.is_valid():
            product = add_product_form.save(commit=False)
            product.artist = user_models.UserInfo.objects.get(user=request.user)
            product.save()

            messages.success(request, 'Product Added Successfuly')
            return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, 'Error: Product wasn\'t Added Successfuly')
            context['form'] = forms.AddProductForm()
            return render(request, 'Market/add_product.html', context)

    else:
        form = forms.AddProductForm()
        context['form'] = form
        return render(request, 'Market/add_product.html', context)
