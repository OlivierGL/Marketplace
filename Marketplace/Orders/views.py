from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from Users import models as user_models
from Users.forms import AddressForm
from Market import models as market_models
import decimal

PROV_TAX_RATE = decimal.Decimal(0.09975)
FED_TAX_RATE = decimal.Decimal(0.05)


@login_required
def shipping_info(request):
    context = {}
    current_user = user_models.UserInfo.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address_db = user_models.Address.objects.get(user=current_user, is_default_shipping=True)
            address_form = form.save(commit=False)

            if address_db != address_form:
                address_db.is_default_shipping = False
                address_db.save()

                address_form.user = address_db.user
                address_form.is_default_shipping = True
                address_form.save()

            return HttpResponseRedirect(reverse('checkout'))
    else:
        form = AddressForm(instance=current_user.user_address.filter(is_default_shipping=True).first())

    context['form'] = form
    return render(request, "Orders/confirm_shipping.html", context)


@login_required
def checkout_order(request):
    current_user = user_models.UserInfo.objects.get(user=request.user)

    cart_products = market_models.CartProduct.objects.filter(cart=current_user.cart, quantity__gt=0)

    subtotal = 0
    for cart_product in cart_products:
        product_total_price = cart_product.product.price * cart_product.quantity
        subtotal += product_total_price

    prov_taxes = round(subtotal * PROV_TAX_RATE, 2)
    fed_taxes = round(subtotal * FED_TAX_RATE, 2)
    total = subtotal + prov_taxes + fed_taxes

    # PayPal button info
    paypal_dict = {
        "business": "rodrigo.lisboamirco@mail.mcgill.ca",
        "amount": "50.00",
        "currency_code": "CAD",
        "item_name": "The Item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('market-home')),
        "cancel_return": request.build_absolute_uri(reverse('market-paintings')),
    }

    # Create the instance.
    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        "form": paypal_form,
        "cartProducts": cart_products,
        "subtotal": subtotal,
        "provTaxes": prov_taxes,
        "fedTaxes": fed_taxes,
        "total": total
    }
    return render(request, "Orders/checkout_order.html", context)
