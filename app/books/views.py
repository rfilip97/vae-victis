from django.http import JsonResponse

def scan_book(request):
    isbn = request.GET.get('barcode', None)
    if isbn:
        return JsonResponse({'barcode': isbn})
    else:
        return JsonResponse({'error': 'Barcode not provided'}, status=400)
