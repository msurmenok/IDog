import requests
import urllib.parse

from credentials import pf_client_id
from credentials import pf_client_secret

api_key = ""

def get_api_key():
    """ Fetch access token from PetFinder api """
    url = "https://api.petfinder.com/v2/oauth2/token"
    body = {"grant_type": "client_credentials",
            "client_id": pf_client_id,
            "client_secret": pf_client_secret}
    r = requests.post(url, data=body)
    data = r.json()
    api_key = data['access_token']
    return api_key

def get_dogs_by_breed(breed="German Shepherd Dog", zipcode="94065"):
    """ Returns dogs of the specified breed near zipcode """
    # Replace space symbols with %20
    breed = urllib.parse.quote(breed)

    url = "https://api.petfinder.com/v2/animals?type=dog&breed=%s&location=%s&distance=100&sort=distance&status=adoptable" % (breed, zipcode)
    token = "Bearer " + api_key
    headers = {'Authorization': token}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['animals']

def get_dogs(zipcode="94065"):
    """ Return all type of dogs near zipcode """
    url = "https://api.petfinder.com/v2/animals?type=dog&location=%s&distance=100&sort=distance&status=adoptable" % (zipcode)
    token = "Bearer " + api_key
    headers = {'Authorization': token}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['animals']

def get_dog_by_id(id="43736184"):
    """ Return a single dog based on its id in PetFinder API """
    url = "https://api.petfinder.com/v2/animals/%s" % id
    token = "Bearer " + api_key
    headers = {'Authorization': token}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['animal']

api_key = get_api_key()
print(get_dog_by_id())
