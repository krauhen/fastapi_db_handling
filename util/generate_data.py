import json
from random import choice

from names_generator import generate_name
from db_exp.models.v1.user import User


def generate_users(n=10):
    providers = ["web.de", "gmail.com", "googlemail.com", "outlook.com", "apple.com", ]
    users = list()
    for i in range(n):
        full_name = generate_name(style='capital')
        name, surname = full_name.split(' ')
        provider = choice(providers)
        email = f"{name}.{surname}@{provider}"
        user = User(user_id=0, username=full_name, email=email)
        user = user.dict()
        del user["user_id"]
        users.append(user)
    return users


if __name__ == '__main__':
    users = generate_users()
    for user in users:
        print(user)

    with open("data/users.json", "w") as f:
        json.dump(users, f)
