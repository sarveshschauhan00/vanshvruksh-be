from mongo import clear_database, add_person, vanshavali, get_person
from person import Person
import flask


# anju = Person(first_name="Anju", surname="Chauhan", gender="female")
# jaswant = Person(first_name="Jaswant", surname="Chauhan", gender="male")
# sarvesh = Person(first_name="Sarvesh", surname="Chauhan", gender="male")
# rishika = Person(first_name="Rishika", surname="Chauhan", gender="female")
# ritambhara = Person(first_name="Ritambhara", surname="Chauhan", gender="female")

# add_person(sarvesh)
# add_siblings(sarvesh, siblings)
# add_mother(sarvesh, mother)
# add_father(sarvesh, father)
# add_wife(sarvesh, unknown)
# clear_database()

# print(vanshavali.find_one({}))


def getFamily(member_id):
    person = getPersonObject(member_id)
    if Person == None:
        print(f"person with id: {member_id} does not exist")
        return None
    # if person:
    #     print("Person found!!!", person.first_name)
    parents = getParents(person)
    # print(parents)
    childrens = getChildrens(person)
    if hasattr(person, "spouse"):
        spouse = getPersonObject(person.spouse)
    else:
        spouse = None
    return parents, person, spouse, childrens


def getParents(person: Person):
    if person.mother_exists:
        mother = getPersonObject(person.mother)
    else:
        mother = None

    if person.father_exists:
        father = getPersonObject(person.father)
    else:
        father = None
    
    return mother, father


def getChildrens(person: Person):
    childrens = []
    for child in person.childrens:
        childrens.append(getPersonObject(child))
    return childrens


def getPersonObject(person_id):
    person_data = get_person({"id": person_id})
    if person_data != None:
        if "spouse" in person_data:
            person = Person(
                first_name=person_data["first_name"], 
                surname=person_data["surname"], 
                gender=person_data["gender"], 
                id=person_data["id"],
                mother=person_data["mother"],
                father=person_data["father"],
                mother_exists=person_data["mother_exists"],
                father_exists=person_data["father_exists"],
                childrens=person_data["childrens"],
                spouse=person_data["spouse"],
                )
        else:
            person = Person(
                first_name=person_data["first_name"], 
                surname=person_data["surname"], 
                gender=person_data["gender"], 
                id=person_data["id"],
                mother=person_data["mother"],
                father=person_data["father"],
                mother_exists=person_data["mother_exists"],
                father_exists=person_data["father_exists"],
                childrens=person_data["childrens"],
                )
        return person
    else:
        # print("No such person exists!!!")
        return None
    

# print(getFamily(member_id="ee49cf9d-ad4a-4f39-bce9-4122e6be953a"))
id = input("Enter member id: ")
x = getFamily(member_id=id)
if x != None:
    parents, person, spouse, childrens = x

if parents[0]:
    print("mother: ", parents[0].first_name)
else:
    print("mother does not exist!!!")

if parents[1]:
    print("father: ", parents[1].first_name)
else:
    print("father does not exist")

print("person name: ", person.first_name)

if spouse:
    print("spouse name: ", spouse.first_name)
else:
    print("spouse does not exist")

for i, child in enumerate(childrens):
    print(f"child {i+1}: ", child.first_name)