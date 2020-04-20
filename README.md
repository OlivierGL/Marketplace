# MontreArt Marketplace

Rodrigo Lisboa Mirco - 260929545  
Olivier Grenier-Leboeuf - 260869338


# How to run

Install python3 and pip (we used python 3.7.3 and above):  
sudo apt-get update && sudo apt-get -y upgrade  
sudo apt-get install python3  
sudo apt-get install -y python3-pip  


Install django, django-channels and redis:  
sudo apt-get install redis-server  
pip3 install django  
pip3 install channels  
pip3 install channels_redis


Install specific django apps for this project (PayPal):  
pip3 install django-paypal


Run migrations, redis and the Django server in Marketplace/:  
redis-server &           
python3 manage.py migrate  
python3 manage.py runserver
 

Go to http://127.0.0.1:8000/


# Run tests

python3 manage.py test Users  
python3 manage.py test Market  


# GitHub

https://github.com/OlivierGL/Marketplace

# PayPal

Since the project is not going to be deployed, we use a Sandbox PayPal account.  
In order to test the functionality, use the email address "comp307@test.example.com", password "We3e'&28" when prompted by the PayPal login page.
