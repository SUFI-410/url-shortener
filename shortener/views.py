from django.http import JsonResponse
from .models import ShortURL
from .utils import generate_unique_code
from django.shortcuts import render, redirect
from django.http import Http404

def shorten_url(request):
    # --- Handle API requests (JSON) ---
    if request.GET.get("url"):
        url = request.GET.get("url")
        code = generate_unique_code()
        obj = ShortURL.objects.create(
            original_url=url,
            short_code=code
        )
        return JsonResponse({
            "short_code": obj.short_code,
            "short_url": request.build_absolute_uri(f"/{obj.short_code}/")
        })
    
    # --- Handle Web Form (HTML) ---
    if request.method == 'POST':
        url = request.POST.get('original_url')
        if not url:
            return render(request, 'shortener/index.html', {'error': 'Please enter a URL!'})
        
        code = generate_unique_code()
        obj = ShortURL.objects.create(
            original_url=url,
            short_code=code
        )
        return render(request, 'shortener/index.html', {
            'short_url': request.build_absolute_uri(f"/{obj.short_code}/"),
            'short_code': obj.short_code
        })
    
    # --- GET request (show empty form) ---
    return render(request, 'shortener/index.html')


def redirect_url(request, short_code):
    try:
        obj = ShortURL.objects.get(short_code=short_code)
        obj.click_count += 1
        obj.save()
        return redirect(obj.original_url)
    except ShortURL.DoesNotExist:
        raise Http404("URL not found")
