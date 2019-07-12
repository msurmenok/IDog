class Dog:
    def __init__(self, id, org_id, breed1, breed2, age, gender, spayed,
                 name, photo_thumbnail, email, phone, city, photos, environment, description, address):
        """
        environment:
            if the dog is good with other children, dogs, and cats
            is a dictionary {"children": true, "dogs": None,"cats": false}
            where None means no information
        photos:
            each element in photos is a dictionary with keys "small", "medium", "large", "full"
        """
        self.id = id
        self.org_id = org_id
        self.breed1 = breed1
        self.breed2 = breed2
        self.age = age
        self.gender = gender
        self.spayed = spayed
        self.name = name
        self.photo_thumbnail = photo_thumbnail
        self.email = email
        self.phone = phone
        self.city = city
        self.photos = photos
        self.environment = environment
        self.description = description
        self.address = address

    def __str__(self):
        return "[" + str(self.id) + ", " + self.name + ", " + self.age + ", " + self.city + ", " + str(
            self.breed1) + ", " + str(self.breed2) + ", " + str(self.photo_thumbnail) + " ]\n"

    def __repr__(self):
        return "[" + str(self.id) + ", " + self.name + ", " + self.age + ", " + self.city + ", " + str(
            self.breed1) + ", " + str(self.breed2) + ", " + str(self.photo_thumbnail) + "]\n"

    def __eq__(self, other):
        return self.id == other.id and self.org_id == other.org_id and self.breed1 == other.breed1 \
               and self.breed2 == other.breed2 and self.age == other.age and self.gender == other.gender \
               and self.spayed == other.spayed and self.name == other.name and self.photo_thumbnail == other.photo_large \
               and self.email == other.email and self.phone == other.phone and self.city == other.city

    # Getters and setters
    @property
    def photos(self):
        return self.__photos

    @photos.setter
    def photos(self, photos):
        self.__photos = photos

    @property
    def environment(self):
        return self.__environment

    @environment.setter
    def environment(self, environment):
        self.__environment = environment

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def org_id(self):
        return self.__org_id

    @org_id.setter
    def org_id(self, org_id):
        self.__org_id = org_id

    @property
    def breed1(self):
        return self.__breed1

    @breed1.setter
    def breed1(self, breed1):
        self.__breed1 = breed1

    @property
    def breed2(self):
        return self.__breed2

    @breed2.setter
    def breed2(self, breed2):
        self.__breed2 = breed2

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender):
        self.__gender = gender

    @property
    def spayed(self):
        return self.__spayed

    @spayed.setter
    def spayed(self, spayed):
        self.__spayed = spayed

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def photo_thumbnail(self):
        return self.__photo_thumbnail

    @photo_thumbnail.setter
    def photo_thumbnail(self, photo_thumbnail):
        self.__photo_thumbnail = photo_thumbnail

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city
