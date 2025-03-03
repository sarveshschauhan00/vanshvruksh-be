from pymongo import MongoClient

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client['vanshvruksh_database']  # Replace with your actual database name
vanshavali = db['vanshavali']  # Replace with your actual collection name


def add_person(person):
    print("saving file in mongo db...")
    mother_id = person.mother
    father_id = person.father

    data = {
        "id": person.id,
        "first_name": person.first_name,
        "surname": person.surname,
        "gender": person.gender,
        "mother": mother_id,
        "mother_exists": person.mother_exists,
        "father": father_id,
        "father_exists": person.father_exists,
        "childrens": [child for child in person.childrens]
    }

    if hasattr(person, "spouse"):
        data["spouse"] = person.spouse

    if vanshavali.find_one({"id": person.id}):
        update_person({"id": person.id}, {"$set": data})
    else:
        # Insert the book into the collection
        result = vanshavali.insert_one(data)
        # Print the ID of the inserted document
        print('\nSuccessfully inserted person with ID:', result.inserted_id)
        print(":) \n\n")


def remove_person(person):
    vanshavali.delete_one({'person_id': person.id})
    print("person deleted from vanshavali")


def clear_database():
    vanshavali.delete_many({})
    pass


def update_person(filter, update):
    # Step 3: Update the document
    result = vanshavali.update_one(filter, update)

    # Verify the update
    if result.modified_count > 0:
        print("Document updated successfully.")
    else:
        print("No document was updated.")
    pass

def get_persons(condition):
    return vanshavali.find(condition)

def get_person(condition):
    return vanshavali.find_one(condition)