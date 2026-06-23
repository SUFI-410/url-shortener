from django.http import JsonResponse
from .models import ShortURL
from .utils import generate_unique_code
from .redis_client import redis_client
from django.shortcuts import redirect
from django.http import Http404


def shorten_url(request):

    url = request.GET.get("url")

    if not url:
        return JsonResponse(
            {"error": "url required"},
            status=400
        )

    code = generate_unique_code()

    obj = ShortURL.objects.create(
        original_url=url,
        short_code=code
    )

    # NEW: Cache immediately after creation
    redis_client.set(
        obj.short_code,
        obj.original_url,
        ex=86400
    )

    return JsonResponse({
        "short_code": obj.short_code,
        "short_url": request.build_absolute_uri(
            f"/{obj.short_code}/"
        )
    })


def redirect_url(request, short_code):

    cached_url = redis_client.get(short_code)

    if cached_url:
        # NEW: Update click count even on cache HIT
        try:
            obj = ShortURL.objects.get(short_code=short_code)
            obj.click_count += 1
            obj.save()
        except ShortURL.DoesNotExist:
            pass

        return redirect(cached_url)

    try:
        obj = ShortURL.objects.get(
            short_code=short_code
        )

        redis_client.set(
            short_code,
            obj.original_url,
            ex=86400
        )

        # Update click count on database MISS too
        obj.click_count += 1
        obj.save()

        return redirect(obj.original_url)

    except ShortURL.DoesNotExist:
        raise Http404("URL not found")
