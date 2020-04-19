from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from Users import models as user_models
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, CreateView, DeleteView
import json

no_product_error_message = "Sorry, no {} are for sale right now."


# View for the home page of the webapp (displays all products) 
def home(request):
    context = {
        'category': "all products",
        'items': models.Product.objects.filter(quantity__gt=0),
        'activeNavItem': "browse/all",
        'noProductErrorMessage': no_product_error_message.format("products")
    }
    return render(request, 'Market/browse.html', context)

# View for the paintings page (displays the paintings)
def paintings(request):
    context = {
        'category': "Paintings",
        'items': models.Product.objects.filter(category="PAINTING", quantity__gt=0),
        'activeNavItem': "browse/paintings",
        'noProductErrorMessage': no_product_error_message.format("paintings")
    }
    return render(request, 'Market/browse.html', context)


# View for the sculptures page (displays the sculptures)
def sculptures(request):
    context = {
        'category': "Sculptures",
        'items': models.Product.objects.filter(category="SCULPTURE", quantity__gt=0),
        'activeNavItem': "browse/sculptures",
        'noProductErrorMessage': no_product_error_message.format("sculptures")
    }
    return render(request, 'Market/browse.html', context)

# View for the clothes page (displays the clothes)
def clothes(request):
    context = {
        'category': "Clothes",
        'items': models.Product.objects.filter(category="GARMENT", quantity__gt=0),
        'activeNavItem': "browse/clothes",
        'noProductErrorMessage': no_product_error_message.format("clothes")
    }
    return render(request, 'Market/browse.html', context)

# View for the jewelry page (displays the jewelry)
def jewelry(request):
    context = {
        'category': "Jewelry",
        'items': models.Product.objects.filter(category="JEWELRY", quantity__gt=0),
        'activeNavItem': "browse/jewelry",
        'noProductErrorMessage': no_product_error_message.format("jewelry")
    }
    return render(request, 'Market/browse.html', context)

# View for the glass art page (displays the glass art)
def glass_art(request):
    context = {
        'category': "Glass Art",
        'items': models.Product.objects.filter(category="GLASS_ART", quantity__gt=0),
        'activeNavItem': "browse/glass_art",
        'noProductErrorMessage': no_product_error_message.format("glass art")
    }
    return render(request, 'Market/browse.html', context)


# View for the cart, which 
@login_required
def cart(request):

    current_user = user_models.UserInfo.objects.get(user=request.user)
    cart_products = models.CartProduct.objects.filter(cart=current_user.cart, quantity__gt=0)

    total = 0
    unavailable_products = []
    for cart_product in cart_products:
        # Validate if product is still available
        if cart_product.product.quantity < cart_product.quantity:
            unavailable_products.append(cart_product.product.name)
            if cart_product.product.quantity <= 0:
                cart_product.delete()
                continue
            else:
                cart_product.quantity = cart_product.product.quantity
                cart_product.save()

        product_total_price = cart_product.product.price * cart_product.quantity
        total += product_total_price

    # Get products list again since it may have been updated
    cart_products = models.CartProduct.objects.filter(cart=current_user.cart, quantity__gt=0)

    context = {'cartProducts': cart_products,
               'total': total,
               'activeNavItem': "cart",
               'unavailableProducts': json.dumps(unavailable_products)}

    return render(request, 'Market/cart.html', context)


# View that renders the page that presents a product
def product(request, pk):
    # Getting the product from the database
    product_db = models.Product.objects.get(pk=pk)
    #Getting the user's data
    if request.user.is_authenticated:
        current_user = models.UserInfo.objects.get(user=request.user)
        product_in_cart = current_user.cart.cart_products.filter(product=product_db, quantity__gt=0).first()
        # Checking if the user is the seller, aka artist. This allows to 
        # display different action buttons depending on who's accessing the 
        # product page
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


# CreateView to add a product to the market
class add_product(LoginRequiredMixin, CreateView):
    model = models.Product
    fields = ['name', 'description', 'quantity', 'price', 'image', 'category']

    def form_valid(self, form):
        # Storing the current user as the artist
        form.instance.artist = user_models.UserInfo.objects.get(user=self.request.user)
        messages.success(self.request, 'Product Added Successfuly')
        return super().form_valid(form)


# UpdateView to update a product
class modify_product(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Product
    fields = ['name', 'description', 'quantity', 'price', 'image', 'category']
    template_name_suffix = '_modify_form'
    # Goes back to the product's page after success
    success_url = '../'

    def form_valid(self, form):
        # Setting the current user as the Artist
        form.instance.artist = user_models.UserInfo.objects.get(user=self.request.user)
        return super().form_valid(form)

    # Method that verifies that the user trying to modify the product
    # is indeed the seller
    def test_func(self):
        product = self.get_object()
        if product.artist.user == self.request.user:
            return True
        return False


# DeleteView to delete a product
class delete_product(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # Goes back to the page before the product page on success
    success_url = '../../../'
    model = models.Product

    # Method that verifies that the user trying to delete the product
    # is indeed the seller
    def test_func(self):
        product = self.get_object()
        if product.artist.user == self.request.user:
            return True
        return False


# Below is only to match different url parameters. Same as product above.
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
