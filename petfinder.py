import requests
import urllib.parse
from Dog import Dog

from credentials import pf_client_id
from credentials import pf_client_secret

# Function that will return object(s) of Dog class
def get_dogs_by_breed(breed="German Shepherd Dog", zipcode="94065"):
    data = get_dogs_json_by_breed(breed, zipcode)
    dogs = []
    for el in data:
        dogs.append(Dog(el["id"],
                        el["organization_id"],
                        el["breeds"]["primary"],
                        el["breeds"]["secondary"],
                        el["age"],
                        el["gender"],
                        el["attributes"]["spayed_neutered"],
                        el["name"],
                        el["photos"][0]["large"],
                        el["contact"]["email"],
                        el["contact"]["phone"],
                        el["contact"]["address"]["city"]
                    ))
    return dogs


def get_dogs(zipcode="94063"):
    data = get_dogs_json(zipcode)
    dogs = []
    for el in data:
        dogs.append(Dog(el["id"],
                        el["organization_id"],
                        el["breeds"]["primary"],
                        el["breeds"]["secondary"],
                        el["age"],
                        el["gender"],
                        el["attributes"]["spayed_neutered"],
                        el["name"],
                        el["photos"][0]["large"],
                        el["contact"]["email"],
                        el["contact"]["phone"],
                        el["contact"]["address"]["city"]
                    ))
    return dogs


def get_dog_by_id(id="43736184"):
    data = get_dog_json_by_id(id)
    return Dog( data["id"],
                data["organization_id"],
                data["breeds"]["primary"],
                data["breeds"]["secondary"],
                data["age"],
                data["gender"],
                data["attributes"]["spayed_neutered"],
                data["name"],
                data["photos"][0]["large"],
                data["contact"]["email"],
                data["contact"]["phone"],
                data["contact"]["address"]["city"]
                )

# Functions that makes calls to PetFinder API
# Should not be used directly in the app
def get_token():
    """ Fetch access token from PetFinder api """
    url = "https://api.petfinder.com/v2/oauth2/token"
    body = {"grant_type": "client_credentials",
            "client_id": pf_client_id,
            "client_secret": pf_client_secret}
    r = requests.post(url, data=body)
    data = r.json()
    api_key = data['access_token']
    return "Bearer " + api_key

def get_dogs_json_by_breed(breed, zipcode):
    """ Returns full dogs info of the specified breed near zipcode """
    # Replace space symbols with %20
    breed = urllib.parse.quote(breed)
    token = get_token()
    url = "https://api.petfinder.com/v2/animals?type=dog&breed=%s&location=%s&distance=100&sort=distance&status=adoptable" % (breed, zipcode)
    headers = {'Authorization': token}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['animals']

def get_dogs_json(zipcode):
    """ Return full info for all type of dogs near zipcode """
    token = get_token()
    url = "https://api.petfinder.com/v2/animals?type=dog&location=%s&distance=100&sort=distance&status=adoptable" % (zipcode)
    headers = {'Authorization': token}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['animals']

def get_dog_json_by_id(id):
    """ Return full info for a single dog based on its id in PetFinder API """
    token = get_token()
    url = "https://api.petfinder.com/v2/animals/%s" % id
    headers = {'Authorization': token}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data['animal']

# Testing
# You can specify id or leave the default
#print(get_dog_by_id(45000754))

# You can specify breed or/and zipcode or leave the default
#print(get_dogs_by_breed("german shepherd dog", 94065))

# You can specify zipcode or leave the default
#print(get_dogs(94063))
