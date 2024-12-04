import requests
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def search(request):
    country = request.GET.get('country', '')
    province = request.GET.get('province', '')
    universities = []
    provinces = set()

    if country:
        api_url = f"http://universities.hipolabs.com/search?country={country}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            universities = response.json()
            provinces = {uni.get('state-province') for uni in universities if uni.get('state-province')}
            if province:
                universities = [uni for uni in universities if uni.get('state-province') == province]
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            universities = []

    return render(request, 'search.html', {
        'universities': universities,
        'country': country,
        'province': province,
        'provinces': sorted(provinces)
    })

