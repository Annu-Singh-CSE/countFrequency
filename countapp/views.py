from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def frequencies(request):
    url_param = request.POST.get('url', request.GET.get('url', ''))
    if not url_param:
        return render(request, 'index.html', {'url': url_param})
    
    parsed_url = urlparse(url_param)
    if not parsed_url.scheme:
        url_param = "https://" + url_param if url_param.startswith('www.') else "https://www." + url_param
    url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    
    try:
        response = requests.get(url_param)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return JsonResponse({'error': 'Invalid URL please check its format' })
    
    html = response.text
    
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    words = text.split()
    
    word_frequencies = {}

    for i in words:
        if i not in word_frequencies:
            word_frequencies[i] = 0
        word_frequencies[i] += 1

    return JsonResponse(word_frequencies)
