import requests
import urllib.parse
from Dog import Dog

from credentials import pf_client_id
from credentials import pf_client_secret


class PetFinderClient:
    def __init__(self):
        self.api_key = self._get_token()

    # Function that will return object(s) of Dog class
    def get_dogs_by_breed(self, breed="German Shepherd Dog", zipcode="94065"):
        """ Find dogs by breed sorted by distance to the specified zip code
            returns list of objects of type Dog
        """
        data = self._get_dogs_json_by_breed(breed, zipcode)
        dogs = []
        for el in data:
            dogs.append(_convert_to_dog(el))
        return dogs

    def get_dogs(self, zipcode="94063"):
        """ Find dogs of any breed sorted by distance to the specified zip code.
            returns list of objects of type Dog
        """
        data = self._get_dogs_json(zipcode)
        dogs = []
        for el in data:
            dogs.append(_convert_to_dog(el))
        return dogs

    def get_dog_by_id(self, id="43736184"):
        """ Find a dog by its PetFinder id.
            returns one object of type Dog
        """
        data = self._get_dog_json_by_id(id)
        return _convert_to_dog(data)

    # Functions that makes calls to PetFinder API
    def _get_token(self):
        """ Fetch access token from PetFinder api """
        url = "https://api.petfinder.com/v2/oauth2/token"
        body = {"grant_type": "client_credentials",
                "client_id": pf_client_id,
                "client_secret": pf_client_secret}
        r = requests.post(url, data=body)
        data = r.json()
        api_key = data['access_token']
        return "Bearer " + api_key

    def _make_api_call(self, url):
        """ Make GET Http request to PetFinder API with specified url and return uncleaned data """
        headers = {'Authorization': self.api_key}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        # api key expired, get a new key
        self.api_key = self._get_token()
        print("Api key expired")
        headers = {'Authorization': self.api_key}
        r = requests.get(url, headers=headers)
        return r.json()


    def _get_dogs_json_by_breed(self, breed, zipcode):
        """ Returns full dogs info of the specified breed near zipcode """
        # Replace space symbols with %20
        breed = urllib.parse.quote(breed)
        url = "https://api.petfinder.com/v2/animals?type=dog&breed=%s&location=%s&distance=100&sort=distance&status=adoptable" % (
            breed, zipcode)
        data = self._make_api_call(url)
        return data['animals']

    def _get_dogs_json(self, zipcode):
        """ Return full info for all type of dogs near zipcode """
        url = "https://api.petfinder.com/v2/animals?type=dog&location=%s&distance=100&sort=distance&status=adoptable" % (
            zipcode)
        data = self._make_api_call(url)
        return data['animals']

    def _get_dog_json_by_id(self, id):
        """ Return full info for a single dog based on its id in PetFinder API """
        url = "https://api.petfinder.com/v2/animals/%s" % id
        data = self._make_api_call(url)
        return data['animal']


# Functions defined below this point should not be used directly in the other parts of the app
# Convert dictionary returned from PetFinder API to Dog object
def _convert_to_dog(element):
    """ Convert information about one dog (returned from API call) to the object of type Dog """
    # Check if photo is available (sometimes there is no picture of a dog)
    photo_thumbnail = None
    if len(element["photos"]) > 0:
        photo_thumbnail = element["photos"][0]["large"]

    address_line1 = ""
    if element["contact"]["address"]["address1"] is not None:
        address_line1 = element["contact"]["address"]["address1"]
    address_line2 = ""
    if element["contact"]["address"]["address2"] is not None:
        address_line2 = element["contact"]["address"]["address2"]

    address = address_line1 + " " + address_line2 + " " + \
              element["contact"]["address"]["city"] + " " + element["contact"]["address"]["state"] + \
              " " + element["contact"]["address"]["postcode"]

    return Dog(element["id"],
               element["organization_id"],
               element["breeds"]["primary"],
               element["breeds"]["secondary"],
               element["age"],
               element["gender"],
               element["attributes"]["spayed_neutered"],
               element["name"],
               photo_thumbnail,
               element["contact"]["email"],
               element["contact"]["phone"],
               element["contact"]["address"]["city"],
               element["photos"],
               element["environment"],
               element["description"],
               address,
               )

# Testing
# Uncomment one print statement at a time

# Find a dog by its PetFinder id
# You can specify id
# print(get_dog_by_id(45000754))


# Find dogs by breed sorted by distance to the specified zip code
# You can specify breed or/and zipcode
# print(get_dogs_by_breed("french bulldog", 94065))
# print(get_dogs_by_breed("Smooth Fox Terrier", 94065))
# print(get_dogs_by_breed("terrier", 94065))


# Find dogs of any breed sorted by distance to the specified zip code
# You can specify zipcode or leave the default
# print(get_dogs(94063))
