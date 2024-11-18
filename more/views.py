from django.shortcuts import render
from django.http import JsonResponse

from .models import NewsLetter


def SubscribeView(request):
	if request.POST:
		email = request.POST.get('email')
		if request.POST.get('action') == 'subscribe':
			newsltr, create = NewsLetter.objects.get_or_create(email=email)
			if create:
				response = JsonResponse('🎉 Congratulations and Welcome to Our Website\'s Subscriber Family! 🎉', safe=False)
			else:
				response = JsonResponse('You Have Already Been Subscribed!', safe=False)

	return response
