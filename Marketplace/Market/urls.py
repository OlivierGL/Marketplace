from django.urls import path
from . import views

# These url patterns are quite numerous, but most of them are to handle cases
# where the product page is accessed from different places. The reason for this is
# that on the product page there is a back button, and this back button can't be
# handle through view context alone. We tried giving in the previous url in the 
# context. However, since we have a "modify" button on the product page, we can move 
# out of the product page and go back to it after modifying the product which 
# messes up the previous context. i.e. browse --> product --> modify --> product
# -back-> modify instead of browse --> product --> modify --> product
# -back-> browse. So we hadd to make lots of url patterns and make the 
# back button's href="../" to simply go back one directory.
urlpatterns = [
  path('', views.home, name='market-home'),
  path('paintings/', views.paintings, name='market-paintings'),
  path('paintings/product/<int:pk>/', views.product, name='product_with_pk_painting'),
  path('paintings/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product_painting"),
  path('paintings/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product_painting"),

  path('sculptures/', views.sculptures, name='market-sculptures'),
  path('sculptures/product/<int:pk>/', views.product, name='product_with_pk_sculpture'),
  path('sculptures/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product_sculpture"),
  path('sculptures/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product_sculpture"),

  path('clothes/', views.clothes, name='market-clothes'),
  path('clothes/product/<int:pk>/', views.product, name='product_with_pk'),
  path('clothes/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product_sculpture"),
  path('clothes/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product_sculpture"),

  path('jewelry/', views.jewelry, name='market-jewelry'),
  path('jewelry/product/<int:pk>/', views.product, name='product_with_pk_jewelry'),
  path('jewelry/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product_jewelry"),
  path('jewelry/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product_jewelry"),

  path('glass_art/', views.glass_art, name='market-glass_art'),
  path('glass_art/product/<int:pk>/', views.product, name='product_with_pk_glass_art'),
  path('glass_art/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product_glass_art"),
  path('glass_art/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product_glass_art"),

  path('cart/', views.cart, name='cart'),
  path('cart/product/<int:pk>/', views.product, name='product_with_pk_cart'),
    
  path('product/<int:pk>/', views.product, name='product_with_pk'),
  path('product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product"),
  path('product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product"),

  path('profile/<int:primary_key>/add_product/', views.add_product.as_view(), name='add_product'),
  path('profile/<int:primary_key>/product/<int:pk>/', views.product_prof, name='product_with_pk_profile'),
  path('profile/<int:primary_key>/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product_profile"),
  path('profile/<int:primary_key>/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product_profile"),
]
