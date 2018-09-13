persons = [
    {
        "name": "Liam",
        "age": 19,
        "hobbies": ["Coding"]
    },
    {
        "name": "Marlena",
        "age": 21,
        "hobbies": ["Coding", "Motocross"]
    }
]

names = [person["name"] for person in persons]
print(names)

all_twenty = all([person["age"] > 20 for person in persons])
print(all_twenty)

copy_persons = [person.copy() for person in persons]
copy_persons[0]["name"] = "Maximilian"
print(copy_persons[0])

liam, marlena = persons
print(liam)
print(marlena)
