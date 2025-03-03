from mongo import clear_database, add_person, vanshavali, get_person
from person import Person
from flask import Flask, jsonify, request
from flask_cors import CORS
from typing import List


app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes by default


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
    childrens: List[Person] = []
    for child in person.childrens:
        childrens.append(getPersonObject(child))
    return childrens


def getSiblings(person: Person):
    siblings: List[Person] = []
    mother, father = getParents(person)
    if mother:
        mother_childrens = getChildrens(mother)
    if father:
        father_childrens = getChildrens(father)
    for mchild in mother_childrens:
        for fchild in father_childrens:
            if mchild.id == fchild.id:
                siblings.append(mchild)
    return siblings


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
    

@app.route('/api/data', methods=['POST'])
def send_data():
    data = request.get_json()  # Get data posted as JSON
    x = getFamily(member_id=data["id"])
    # print(x)
    if x != None:
        parents, person, spouse, childrens = x

    node = []
    
    # add siblings
    mother, father = getParents(person)
    siblings = getSiblings(person)
    # print(siblings)
    for s in siblings:
        # adding spouse
        if hasattr(s, "spouse"):
            spouse = getPersonObject(s.spouse)
            node.append({ "id": s.id, "mid": [s.mother], "fid": [s.father], "pids": [spouse.id], "name": s.first_name, "gender": s.gender })
            node.append({ "id": spouse.id, "pids": [s.id], "name": spouse.first_name, "gender": spouse.gender })
        else:
            # defining self and parents
            node.append({ "id": s.id, "mid": [s.mother], "fid": [s.father], "name": s.first_name, "gender": s.gender })

    top = 3
    bottom = 2

    # get ancestors
    crowd = [person]
    for i in range(top):
        z = []
        for p in crowd:
            mother, father = getParents(p)
            if mother and father:
                node.append({ "id": mother.id, "pids": [father.id], "name": mother.first_name, "gender": "female" },)
                node.append({ "id": father.id, "pids": [mother.id], "name": father.first_name, "gender": "male" },)

                for item in node:
                    if item["id"] == p.id:
                        item["mid"] = mother.id
                        item["fid"] = father.id
                z.append(mother)
                z.append(father)
        crowd = z
    
    # # get decendents
    crowd = [person]
    for i in range(bottom):
        z = []
        for p in crowd:
            childrens = getChildrens(p)
            for child in childrens:
                # adding spouse
                if hasattr(child, "spouse"):
                    spouse = getPersonObject(child.spouse)
                    node.append({ "id": child.id, "mid": [child.mother], "fid": [child.father], "pids": [spouse.id], "name": child.first_name, "gender": child.gender })
                    node.append({ "id": spouse.id, "pids": [child.id], "name": spouse.first_name, "gender": spouse.gender })
                else:
                    # defining self and parents
                    node.append({ "id": child.id, "mid": [child.mother], "fid": [child.father], "name": child.first_name, "gender": child.gender })
                z.append(child)
        crowd = z
    # print(node)        
    return jsonify({"message": "Data received", "node": node}), 200


@app.route('/api/update', methods=['POST'])
def update_data():
    data = request.get_json()
    update_node = data['updateNodesData']
    print(data)
    print(update_node)

    return jsonify({"message": "Data received", "sent": data}), 200

if __name__ == '__main__':
    app.run(debug=True)