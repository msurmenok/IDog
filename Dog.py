class Dog:
    def __init__(self, id, org_id, breed1, breed2, age, gender, spayed,
      name, photo_large, email, phone, city):
      self.id = id
      self.org_id = org_id
      self.breed1 = breed1
      self.breed2 = breed2
      self.age = age
      self.gender = gender
      self.spayed = spayed
      self.name = name
      self.photo_large = photo_large
      self.email = email
      self.phone = phone
      self.city = city

    def __str__(self):
        return "[" + str(self.id) + ", " + self.name + ", " + self.age + ", " + self.city + ", " + str(self.breed1) + ", " + str(self.breed2) + ", " + str(self.photo_large) + " ]\n"

    def __repr__(self):
        return "[" + str(self.id) + ", " + self.name + ", " + self.age + ", " + self.city + ", " + str(self.breed1) + ", " + str(self.breed2) + ", " + str(self.photo_large) + "]\n"

    def __eq__(self, other):
        return self.id == other.id and self.org_id == other.org_id and self.breed1 == other.breed1 \
        and self.breed2 == other.breed2 and self.age == other.age and self.gender == other.gender \
        and self.spayed == other.spayed and self.name == other.name and self.photo_large == other.photo_large \
        and self.email == other.email and self.phone == other.phone and self.city == other.city
