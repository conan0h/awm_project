from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import requests
import math
from .models import WikipediaArticle


def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

def get_nearby_wikipedia(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')

        if latitude and longitude:
            S = requests.Session()

            URL = "https://en.wikipedia.org/w/api.php"

            PARAMS = {
                "action": "query",
                "format": "json",
                "generator": "geosearch",
                "ggsprimary": "all",
                "ggsradius": 10000,  # You can adjust the radius as needed
                "ggscoord": f"{latitude}|{longitude}",
                "prop": "coordinates|pageimages"
            }

            R = S.get(url=URL, params=PARAMS)
            DATA = R.json()
            print("hello")
            print(DATA)
            # Check if 'query' key exists in the response
            if 'query' in DATA:
                PLACES = DATA['query']['pages']

                results = []
                for k, v in PLACES.items():
                    title = v.get('title', '')
                    thumbnail = v['thumbnail']['source'] if 'thumbnail' in v else ''
                    if 'coordinates' in v:
                        article_lat = v['coordinates'][0]['lat']
                        article_lon = v['coordinates'][0]['lon']
                        distance = haversine(float(latitude), float(longitude), article_lat, article_lon)

                        # Safely access the 'pageimage' key with a default value of None
                        pageimage = v.get('pageimage', None)

                        article, created = WikipediaArticle.objects.get_or_create(
                            pageid=k,
                            defaults={
                                'title': title,
                                'index': v['index'],
                                'coordinates_lat': article_lat,
                                'coordinates_lon': article_lon,
                            }
                        )

                        if not created:
                            # Update the existing article if needed
                            article.title = title
                            article.index = v['index']
                            article.coordinates_lat = article_lat
                            article.coordinates_lon = article_lon
                            article.save()



                        results.append(
                            {'title': title, 'thumbnail': thumbnail, 'distance': distance, 'latitude': article_lat,
                             'longitude': article_lon})
                    else:
                        # Handle the case where 'coordinates' are missing
                        results.append({'title': title, 'thumbnail': thumbnail, 'distance': 'N/A', 'latitude': None,
                                        'longitude': None})

                context = {
                    'results': results,
                    'latitude': latitude,
                    'longitude': longitude,
                }
                return render(request, 'nearby_wikipedia.html', context)
            else:
                return render(request, 'error.html', {'message': 'No data found from Wikipedia API'})

    return render(request, 'get_location.html')


def display_nearby_wikipedia(request):
    articles = WikipediaArticle.objects.all()
    return render(request, 'nearby_wikipedia.html', {'articles': articles})