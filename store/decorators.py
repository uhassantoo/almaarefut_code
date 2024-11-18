from django.core.cache import cache
from django.http import HttpResponseForbidden
from functools import wraps


def rate_limit(limit=5, period=60):
	def decorator(view_func):
		@wraps(view_func)
		def wrapped_view(request, *args, **kwargs):
			client_ip = request.META.get('REMOTE_ADDR')
			cache_key = f'rate_limit_{client_ip}'
			requests = cache.get(cache_key, 0)

			if requests >= limit:
				return HttpResponseForbidden("Rate limit exceeded. please try again later")

			cache.set(cache_key, requests + 1, period)

			return view_func(request, *args, **kwargs)
		return wrapped_view
	return decorator
