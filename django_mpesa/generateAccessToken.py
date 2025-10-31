import requests
from django.http import JsonResponse


def get_access_token(request):
    consumer_key = 'MVKPQmxOyveUlR0ApIDGdcoqZob9dKNrv3M57HK0lI6Gtvjw'
    consumer_secret = 'Fs06jSX1n3cObGQjcnQGCoKLSGaZm6OcfXHD5zmpmuDEfIyWC5A8eSzlQulc9l3f'
    acces_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth = (consumer_key, consumer_secret)

    try:
        response = requests.get(acces_token_url, auth=auth)
        response.raise_for_status()
        result = response.json()
        # print(result)
        access_token = result['access_token']
        return JsonResponse({'access_token': access_token})
    except requests.exceptions.RequestException as error:
        return JsonResponse({'error': str(error)})
