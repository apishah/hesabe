# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django
from string import Template
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .utils import *
from django.db import transaction as transaction_atomic
import json
import requests
from .models import Credential
from django.conf import settings

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hesabe_payment(req,paymentType=2,amount=0):
	with transaction_atomic.atomic():
		credential_obj = Credential.objects.all()
		if(len(credential_obj)==1):

			amount = amount
			merchantCode = credential_obj[0].merchant_code
			baseUrl=credential_obj[0].base_url
			working_key = credential_obj[0].working_key
			iv =credential_obj[0].iv

		data = {'merchantCode' : merchantCode, "paymentType": paymentType,"version":0,'amount':amount,'responseUrl':baseUrl+'/response/','failureUrl':baseUrl+'/response/' }
		encryptedText = encrypt(str(json.dumps(data)), working_key , iv)
        checkoutToken = checkout(encryptedText)
        result = decrypt(checkoutToken,working_key , iv)
        response = json.loads(result)
        decryptToken = response['response']['data']
        url = "http://payment-api.eu-central-1.elasticbeanstalk.com/api/payment"
        html = '''\
            <html>
            <head>
                <title>Sub-merchant checkout page</title>
                <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
            </head>
            <body>
            <form id="nonseamless" method="get" name="redirect" action='$url'>
                    <input type="hidden" id="data" name="data" value='$data'>
                    <script language='javascript'>document.redirect.submit();</script>
            </form>
            </body>
            </html>
            '''
        fin = Template(html).safe_substitute(url=url,data=decryptToken)
        return django.http.HttpResponse(fin)
		# return render(req,'djnago_app/pay.html')


def payment(req):
	return render(req,'djnago_app/pay.html')
	


def knet_payment(req):
	return hesabe_payment(req,1,amount=10)


def mpgs_payment(req):
	return hesabe_payment(req,2,amount=10)


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def response(request):
	
	credential_obj = Credential.objects.all()
	if(len(credential_obj)==1):
		working_key = credential_obj[0].working_key
		iv =credential_obj[0].iv

	response = request.GET
	data = json.loads(decrypt(response.get('data'),working_key,iv))
	if(data.get('status') == 1):
		return django.http.JsonResponse(data.get('response'))
	elif(data.get('status') == 0):
		return django.http.JsonResponse(data.get('response'))
