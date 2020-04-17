from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from Users import models as user_models
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, CreateView, DeleteView

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


def product(request, pk):
    product_db = models.Product.objects.get(pk=pk)
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
                }
    return render(request, 'Market/product.html', context)


'''
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
'''


class add_product(LoginRequiredMixin, CreateView):
    model = models.Product
    fields = ['name', 'description', 'quantity', 'price', 'image', 'category']

    def form_valid(self, form):
        form.instance.artist = user_models.UserInfo.objects.get(user=self.request.user)
        messages.success(self.request, 'Product Added Successfuly')
        return super().form_valid(form)


class modify_product(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Product
    fields = ['name', 'description', 'quantity', 'price', 'image', 'category']
    template_name_suffix = '_modify_form'
    success_url = '../'

    def form_valid(self, form):
        form.instance.artist = user_models.UserInfo.objects.get(user=self.request.user)
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if product.artist.user == self.request.user:
            return True
        return False

class delete_product(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    success_url = '../../../'
    model = models.Product

    def test_func(self):
        product = self.get_object()
        if product.artist.user == self.request.user:
            return True
        return False



# Below is only to match different url parameters.
def product_prof(request, pk, primary_key):
    product_db = models.Product.objects.get(pk=pk)
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
                }
    return render(request, 'Market/product.html', context)

