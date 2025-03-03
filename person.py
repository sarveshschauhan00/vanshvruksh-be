from bson.objectid import ObjectId
import uuid
from mongo import add_person, update_person, get_persons


class Person:
    def __init__(self, gender, first_name="", surname="", middle_name="", id = None, mother = None, father = None, spouse=None, mother_exists=False, father_exists=False, childrens= None):
        # self.id = id
        if id != None:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.surname = surname
        self.middle_name = middle_name
        self.gender = gender

        self.mother_exists= mother_exists
        if mother != None:
            self.mother = mother
            self.mother_exists = True
        else:
            self.mother = str(uuid.uuid4())

        self.father_exists = father_exists
        if father != None:
            self.father = father
            self.father_exists = True
        else:
            self.father = str(uuid.uuid4())
        
        if spouse:
            self.spouse = spouse
        
        self.childrens = []
        if childrens:
            self.childrens = childrens
    
    def add_phone(self, phone_number):
        self.phone_number = phone_number

    def add_email(self, email):
        self.email = email

    def add_images(self, images):
        self.images = images
    
    def add_spouse(self, spouse):
        self.spouse = spouse.id
        # update self
        filter = {"id": self.id}
        update_person(filter, {'$set': {"spouse": spouse.id}})
        add_person(spouse)
        filter = {"id": spouse.id}
        update_person(filter, {'$set': {"spouse": self.id}})
    
    def add_mother(self, mother):
        childrens = get_persons({"mother": self.mother})
        for child in childrens:
            # change in database
            update_person({"id": child["id"]}, {'$set': {"mother_exists": True, "mother": mother.id}})
            mother.add_child( Person(first_name=child["first_name"], surname=child["surname"], gender=child["gender"], id=child["id"]) )

        # change in python object
        self.mother = mother.id
        self.mother_exists = True
        add_person(mother)

    def add_father(self, father):
        childrens = get_persons({"father": self.father})
        for child in childrens:
            # change in database
            update_person({"id": child["id"]}, {'$set': {"father_exists": True, "father": father.id}})
            father.add_child( Person(first_name=child["first_name"], surname=child["surname"], gender=child["gender"], id=child["id"]) )

        # change in python object
        self.father = father.id
        self.father_exists = True
        add_person(father)

    def add_siblings(self, siblings, same_mother:bool=False, same_father:bool=False):
        if not (same_father or same_mother):
            print("No one is added!!!")
            return
        
        for sibling in siblings:
            if same_mother:
                sibling.mother = self.mother
                sibling.mother_exists = self.mother_exists
                if self.mother_exists:
                    update_person({"id": self.mother}, {"$push": {"childrens": sibling.id}})
            if same_father:
                sibling.father = self.father
                sibling.father_exists = self.father_exists
                if self.father_exists:
                    update_person({"id": self.father}, {"$push": {"childrens": sibling.id}})
            add_person(sibling)

    def add_child(self, child):
        self.childrens.append(child.id)
        if self.gender == "male":
            child.mother = self.id
        else:
            child.father = self.id