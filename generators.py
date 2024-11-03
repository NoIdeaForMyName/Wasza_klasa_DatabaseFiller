import records_nb
from faker import Faker
import random
from datetime import datetime

SEED = 43

Faker.seed(SEED)
fake = Faker()

date_format = '%Y-%m-%d'

# PROFILES

def profiles():
    profiles = []
    faiths = [
        "Christianity",
        "Islam",
        "Hinduism",
        "Buddhism",
        "Judaism",
        "Sikhism",
        "Baha'i Faith",
        "Jainism",
        "Shinto",
        "Taoism",
        "Zoroastrianism",
        "Confucianism",
        "Paganism",
        "Unitarian Universalism",
        "Rastafarianism"
    ]
    for i in range(records_nb.PROFILES):
        row = {
            'ID': i,
            'Name': fake.first_name(),
            'Surname': fake.last_name(),
            'Description': fake.text(max_nb_chars=5000),
            'Birthday': fake.date_of_birth(minimum_age=13).strftime(date_format),
            'DateOfCreation': fake.date_this_century().strftime(date_format),
            'Sex': random.choice(["K","M"]),
            'Faith': random.choice(faiths),
            'Email': fake.email(),
            'Password': fake.password(),
            'IsActive': True if abs(random.gauss(0, 1)) < 1.8 else False
        }
        profiles.append(row)
    return profiles
#    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))

# CHATS


# FRIENDSHIPS


# GROUPS


# POSTS


# COMMENTS


# TYPES


# REACTIONS


# ROOMS


# ROLES


# PARTICIPATIONS


# NOTIFICATIONS


# ALBUMS


# EXTENSIONS


# MEDIA


# PUBLICATIONS


# SHARES


# PERMISSIONS


# AFFILIATIONS


# MESSAGES


def main():
    pass

if __name__ == "__main__":
    main()
