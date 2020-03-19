from django.shortcuts import render

# Create your views here.

def home(request):
  return render(request, 'Market/home.html')

def paintings(request):
# made up item to demo the browser template. 	
#  items = [ {
#    'name': 'painting1',
#    'description': 'test painting',
#    'quantity': '3',
#    'image': 'Market/painting.jpg',               #put your image in Marketplace/Market/static/Market and call it painting
#    'price': '430' },
#  ]
  context = {
  	'category': "Paintings",
    'items': "a"                                   #"a" is just used as a stub, replace it with items after uncommenting the above                                 
  }
  return render(request, 'Market/browse.html', context)

def sculptures(request):
  context = {
  	'category': "Sculptures",
    'items': "a"
  }
  return render(request, 'Market/browse.html')

def clothes(request):
  context = {
  	'category': "Clothes",
    'items': "a"
  }
  return render(request, 'Market/browse.html')

def jewelry(request):
  context = {
  	'category': "Jewelry",
    'items': "a"
  }
  return render(request, 'Market/browse.html')

def glass_art(request):
  context = {
  	'category': "Glass Art",
    'items': "a"
  }
  return render(request, 'Market/browse.html')


