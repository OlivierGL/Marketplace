from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'Market/home.html', {'activeNavItem': 'home'})


def paintings(request):
    # made up item to demo the browser template.
    items = [{
        'name': 'painting1',
        'description': 'test painting',
        'quantity': '3',
        'image': 'Market/painting.jpg',               #put your image in Marketplace/Market/static/Market and call it painting
        'price': '430'},
    ]
    context = {
        'category': "Paintings",
        'items': items,                                   #"a" is just used as a stub, replace it with items after uncommenting the above
        'activeNavItem': "browse/paintings"
    }
    return render(request, 'Market/browse.html', context)


def sculptures(request):
    context = {
        'category': "Sculptures",
        'items': "a",
        'activeNavItem': "browse/sculptures"
    }
    return render(request, 'Market/browse.html', context)


def clothes(request):
    context = {
        'category': "Clothes",
        'items': "a",
        'activeNavItem': "browse/clothes"
    }
    return render(request, 'Market/browse.html', context)


def jewelry(request):
    context = {
        'category': "Jewelry",
        'items': "a",
        'activeNavItem': "browse/jewelry"
    }
    return render(request, 'Market/browse.html', context)


def glass_art(request):
    context = {
        'category': "Glass Art",
        'items': "a",
        'activeNavItem': "browse/glass_art"
    }
    return render(request, 'Market/browse.html', context)


