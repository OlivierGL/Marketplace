from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from Users import models as user_models
from Users.forms import AddressForm
from Market import models as market_models
from . import models
import decimal
import uuid

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

    address = current_user.user_address.filter(is_default_shipping=True).first()
    cart_products = market_models.CartProduct.objects.filter(cart=current_user.cart, quantity__gt=0)

    subtotal = 0
    product_names = ', '.join([cart_product.product.name for cart_product in cart_products])
    for cart_product in cart_products:
        product_total_price = cart_product.product.price * cart_product.quantity
        subtotal += product_total_price

    prov_taxes = round(subtotal * PROV_TAX_RATE, 2)
    fed_taxes = round(subtotal * FED_TAX_RATE, 2)
    total = subtotal + prov_taxes + fed_taxes

    # unique paypal id
    paypal_invoice = "ppal-id-"+str(uuid.uuid4())

    # PayPal button info
    paypal_dict = {
        "business": "rodrigo.lisboamirco@mail.mcgill.ca",
        "amount": total,
        "currency_code": "CAD",
        "item_name": product_names,
        "invoice": paypal_invoice,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('successful-payment')),
        "cancel_return": request.build_absolute_uri(reverse('canceled-payment')),
        "rm": 2  # Will return a POST
    }

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        "form": paypal_form,
        "cartProducts": cart_products,
        "subtotal": subtotal,
        "provTaxes": prov_taxes,
        "fedTaxes": fed_taxes,
        "total": total,
        "address": address,
        "paypalInvoice": paypal_invoice
    }
    return render(request, "Orders/checkout_order.html", context)


@csrf_exempt
def successful_payment(request):
    order = models.Order.objects.get(payPalInvoice=request.POST['invoice'])
    current_user = order.buyer

    # Change order status to paid
    order.status = "PAID"
    order.save()

    # Recreate cart
    current_user.cart.delete()
    market_models.Cart.objects.create(user=current_user)
    messages.success(request, 'Your purchase has been completed successfully!')

    return HttpResponseRedirect(reverse('market-home'))


@csrf_exempt
def canceled_payment(request):
    current_user = user_models.UserInfo.objects.get(user=request.user)

    # Change order status to canceled
    order = current_user.buyer_order.order_by('-timestamp').first()
    order.status = "CANCELED"
    order.save()

    # Put products back in stock
    order_products = models.OrderProduct.objects.filter(order=order)
    for order_product in order_products:
        db_product = order_product.product
        db_product.quantity += order_product.quantity
        db_product.save()

    messages.error(request, 'Your purchase has been canceled')

    return HttpResponseRedirect(reverse('market-home'))


