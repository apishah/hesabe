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
from django.views.decorators.csrf import csrf_exempt
from .models import Credential
from django.conf import settings


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hesabe_payment(req,amount,paymentType,args):
	with transaction_atomic.atomic():
		print("hisabe")
		credential_obj = Credential.objects.all()
		if(len(credential_obj) == 1):
			args = json.loads(args)
			merchantCode = credential_obj[0].merchant_code
			success_url = credential_obj[0].success_url
			failure_url = credential_obj[0].failure_url
			working_key = credential_obj[0].working_key
			iv = credential_obj[0].iv
			print(args.get("variable1"))
			print(args)
			variable1 = args.get("variable1",None)
			variable2 = args.get("variable2",None)
			variable3 = args.get("variable3",None)
			variable4 = args.get("variable4",None)
			variable5 = args.get("variable5",None)
			data = {'merchantCode' : merchantCode,"variable1":variable1,"variable2":variable2,"variable3":variable3,
					"variable4":variable4,"variable5":variable5, "paymentType": paymentType,"version":0,'amount':amount,'responseUrl':success_url,'failureUrl':failure_url }
			encryptedText = encrypt(str(json.dumps(data)), working_key , iv)
	        checkoutToken = checkout(encryptedText)
	        result = decrypt(checkoutToken,working_key , iv)
	        response = json.loads(result)
	        decryptToken = response['response']['data']
	        url = credential_obj[0].payment_url
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
		


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment(req):
	payment_variables = {

		"variable1" : "abc",
		"variable2" : "abc",
		"variable3" : "abc",
		"variable4" : "abc",
		"variable5" : "abc",
		"amount":10

	}
	return render(req, 'hesabe_app/pay.html',payment_variables)


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def knet_payment(req,**kwargs):
	print(req.POST)
	return hesabe_payment(req,req.POST.get('amount'), 1 ,req.POST.get('parameter'))


def mpgs_payment(req,**kwargs):
	return hesabe_payment(req,req.POST.get('amount'), 2 ,req.POST.get('parameter'))
	
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
