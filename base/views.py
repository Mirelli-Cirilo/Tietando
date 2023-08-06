from django.shortcuts import render
from security.security import CLIENT_ID, SECRET_ID
import base64
import json
import requests
client_id = CLIENT_ID
secret_id = SECRET_ID
# Create your views here.
def home(request):
    query = request.GET.get("q")

    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f'?q={query}&type=artist&limit=1'

    query_url = url + query
    response = requests.request('GET', query_url, headers=headers)
    json_result = json.loads(response.content)['artists']['items']

    if len(json_result) == 0:
        print('Artista não encontrado')
        return None 

    image = json_result[0]['images'][0]['url']
    followers = json_result[0]['followers']['total']
    context = {'json_result': json_result[0], 'image': image, 'followers':followers}
    return render(request, 'home.html', context)
    
def get_token():
    auth_string = client_id + ':' + secret_id
    auth_bytes = auth_string.encode("ascii")
    auth_base64 = str(base64.b64encode(auth_bytes), "ascii")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.request('POST', url = url, headers=headers, data=data)
    token = response.json()['access_token']
    return token

def get_auth_header(token):
    return {'Authorization': f'Bearer {token}'}


token = get_token()