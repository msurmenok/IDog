import requests
import urllib.parse
from Dog import Dog

from credentials import pf_client_id
from credentials import pf_client_secret

# Function that will return object(s) of Dog class
def get_dogs_by_breed(breed="German Shepherd Dog", zipcode="94065"):
    """ Find dogs by breed sorted by distance to the specified zip code
        returns list of objects of type Dog
    """
    data = get_dogs_json_by_breed(breed, zipcode)
    dogs = []
    for el in data:
        dogs.append(convert_to_dog(el))
    return dogs


def get_dogs(zipcode="94063"):
    """ Find dogs of any breed sorted by distance to the specified zip code.
        returns list of objects of type Dog
    """
    data = get_dogs_json(zipcode)
    dogs = []
    for el in data:
        dogs.append(convert_to_dog(el))
    return dogs


def get_dog_by_id(id="43736184"):
    """ Find a dog by its PetFinder id.
        returns one object of type Dog
    """
    data = get_dog_json_by_id(id)
    return convert_to_dog(data)

# Functions defined below this point should not be used directly in the other parts of the app
# Convert dictionary returned from PetFinder API to Dog object
def convert_to_dog(element):
    """ Convert information about one dog (returned from API call) to the object of type Dog """
    # Check if photo is available (sometimes there is no picture of a dog)
    photo = None
    if (len(element["photos"]) > 0):
        photo = element["photos"][0]["large"]

    return Dog( element["id"],
                element["organization_id"],
                element["breeds"]["primary"],
                element["breeds"]["secondary"],
                element["age"],
                element["gender"],
                element["attributes"]["spayed_neutered"],
                element["name"],
                photo,
                element["contact"]["email"],
                element["contact"]["phone"],
                element["contact"]["address"]["city"]
                )


# Functions that makes calls to PetFinder API
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

def make_api_call(url):
    """ Make GET Http request to PetFinder API with specified url and return uncleaned data """
    token = get_token()
    headers = {'Authorization': token}
    r = requests.get(url, headers=headers)
    return r.json()

def get_dogs_json_by_breed(breed, zipcode):
    """ Returns full dogs info of the specified breed near zipcode """
    # Replace space symbols with %20
    breed = urllib.parse.quote(breed)
    url = "https://api.petfinder.com/v2/animals?type=dog&breed=%s&location=%s&distance=100&sort=distance&status=adoptable" % (breed, zipcode)
    data = make_api_call(url)
    return data['animals']

def get_dogs_json(zipcode):
    """ Return full info for all type of dogs near zipcode """
    url = "https://api.petfinder.com/v2/animals?type=dog&location=%s&distance=100&sort=distance&status=adoptable" % (zipcode)
    data = make_api_call(url)
    return data['animals']

def get_dog_json_by_id(id):
    """ Return full info for a single dog based on its id in PetFinder API """
    url = "https://api.petfinder.com/v2/animals/%s" % id
    data = make_api_call(url)
    return data['animal']

# Testing

# Find a dog by its PetFinder id
# You can specify id
# print(get_dog_by_id(45000754))


# Find dogs by breed sorted by distance to the specified zip code
# You can specify breed or/and zipcode
print(get_dogs_by_breed("german shepherd dog", 94065))
# print(get_dogs_by_breed("Smooth Fox Terrier", 94065))
# print(get_dogs_by_breed("terrier", 94065))


# Find dogs of any breed sorted by distance to the specified zip code
# You can specify zipcode or leave the default
# print(get_dogs(94063))
