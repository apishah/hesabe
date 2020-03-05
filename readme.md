# Project Title

Hesabe payment gateway application.

## Getting Started

These instructions will help you to integrate hesabe payment gateway on your local machine for development and testing purposes. 

### Prerequisites

What things you need to install the software and how to install them


```
python 2.7
django >=1.11
```

### Installing and configurations

```
git clone 

```

Step 1) Add this application to your project.

Step 2) Add this application to INSTALLED_APPS variable in settings.py

For example
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hesabe_app',-->add this 
]
```
Step 3)Do the migrations 

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```
Step 4)Go to admin panel

Step 5)Add  Configuration varaible values in admin panel.
```
Example:
Merchant code:1351719857300
Success Url:http://localhost:8000/response
Failure Url:http://localhost:8000/response
accesscode:345-5456-3434
Payment Url:api.hesbstck.com(add without http or https)
Working key:OGzgrmqyDEnlALQRNvzPv8NJ4BwWM019
IV:WjnegZ76y3PO3dwZ
Knet status:select enable/disable
mpgs status:select enable/disable
```

### how to use this application.

create one function and add parameters as shown below.
```
def payment(req):
	payment_variables = {

		"variable1" :  variable1 value,
		"variable2" :  variable1 value,
		"variable3" :  variable1 value,
		"variable4" :  variable1 value,
		"variable5" :  variable1 value,
		"amount":amount value

	}
	return render(req, 'hesabe_app/pay.html',payment_variables)

```
