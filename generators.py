import records_nb
from faker import Faker
import random
from datetime import timedelta

SEED = 43

Faker.seed(SEED)
fake = Faker()

date_format = '%Y-%m-%d'


# PROFILES
def profiles():
    data = []
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

    prev_emails = set()

    for i in range(records_nb.PROFILES):
        print(f"Profiles iteration: {i}")
        email = fake.email()
        while email in prev_emails:
            email = fake.email()
        prev_emails.add(email)
        row = {
            'ID': i,
            'Name': fake.first_name(),
            'Surname': fake.last_name(),
            'Description': fake.text(max_nb_chars=5000),
            'Birthday': fake.date_of_birth(minimum_age=13).strftime(date_format),
            'DateOfCreation': fake.date_this_century().strftime(date_format),
            'Sex': random.choice(["K","M"]),
            'Faith': random.choice(faiths),
            'Email': email,
            'Password': fake.password(),
            'IsActive': True if abs(random.gauss(0, 1)) < 1.8 else False
        }
        data.append(row)
    return data


# CHATS
def chats(): # date of chat start moze byc starsza niz data zalozenia ktoregos konta (mozna poustalac przedzialy na wszystko, np. konta zalozone maks do 2020 roku itp. ale nie wiem czy tak moze byc - najprosciej by bylo)
    data = []
    send_receiv_check = set()
    for i in range(records_nb.CHATS):
        print(f"Chats iteration: {i}")
        sender, receiver = random.sample(range(records_nb.PROFILES), 2)
        pair = frozenset((sender, receiver))
        while pair in send_receiv_check:
            sender, receiver = random.sample(range(records_nb.PROFILES), 2)
            pair = frozenset((sender, receiver))
        send_receiv_check.add(pair)
        row = {
            'ID': i,
            'FK_Sender': sender,
            'FK_Receiver': receiver,
            'DateOfChatStart': fake.date_this_century().strftime(date_format)
        }
        data.append(row)
    return data


# FRIENDSHIPS
def friendships(): # DateOfFriendshipStart moze byc starsza niz data zalozenia ktoregos konta
    data = []
    invit_receiv_check = set()
    for i in range(records_nb.FRIENDSHIPS):
        print(f"Friendships iteration: {i}")
        inviter, receiver = random.sample(range(records_nb.PROFILES), 2)
        pair = frozenset((inviter, receiver))
        while pair in invit_receiv_check:
            inviter, receiver = random.sample(range(records_nb.PROFILES), 2)
            pair = frozenset((inviter, receiver))
        invit_receiv_check.add(pair)
        row = {
            'ID': i,
            'FK_FriendshipInviter': inviter,
            'FK_FriendshipReceiver': receiver,
            'DateOfFriendshipStart': fake.date_this_century().strftime(date_format)
        }
        data.append(row)
    return data


# GROUPS
def groups():
    data = []
    for i in range(records_nb.GROUPS):
        print(f"Groups iteration: {i}")
        row = {
            'ID': i,
            'Name': fake.text(max_nb_chars=20)[:-1]
        }
        data.append(row)
    return data


# POSTS
def posts():
    data=[]
    for i in range(records_nb.POSTS):
        print(f"Posts iteration: {i}")
        row = {
            'ID': i,
            'FK_Author': random.randint(0, records_nb.PROFILES-1),
            'FK_Group': random.randint(0, records_nb.GROUPS-1),
            'Content': fake.text(max_nb_chars=20000),
            "DateOfPublication":fake.date_this_century().strftime(date_format)
        }
        data.append(row)
    return data


# COMMENTS
def comments():
    data = []
    for i in range(records_nb.COMMENTS):
        print(f"Comments iteration: {i}")
        row = {
            'ID': i,
            'FK_CommentProfile': random.randint(0, records_nb.PROFILES-1),
            'FK_CommentedPost': random.randint(0, records_nb.POSTS-1),
            'Content': fake.text(max_nb_chars=5000),
        }
        data.append(row)
    return data


# TYPES
def types():
    data = []
    reaction_types = ["Like", "Love", "Haha", "Wow", "Sad", "Angry", "Kitten", "Dislike", "Celebrate"]

    for i, name in enumerate(reaction_types):  # Limit to the number specified in records_nb.TYPES
        print(f"Types iteration: {i}")
        row = {
            'ID': i,
            'Name': name
        }
        data.append(row)
    return data


# REACTIONS
def reactions():
    data = []
    for i in range(records_nb.REACTIONS):
        print(f"Reactions iteration: {i}")
        row = {
            'ID': i,
            'FK_ReactionProfile': random.randint(0, records_nb.PROFILES-1),
            'FK_ReactionPost': random.randint(0, records_nb.POSTS-1),
            'FK_ReactionType': random.randint(0, records_nb.TYPES-1),
            "DateOfReaction": fake.date_this_century().strftime(date_format)
        }
        data.append(row)
    return data


# ROOMS
def rooms():
    data = []
    for i in range(records_nb.ROOMS):
        print(f"Rooms iteration: {i}")
        row = {
            'ID': i,
            'Name': fake.text(max_nb_chars=20)[:-1],
            'IsActive': True if random.random() < 0.9 else False
        }
        data.append(row)
    return data


# ROLES
def roles():
    roles = ['room_administrator', 'room_member']
    data = []
    for i in range(len(roles)):
        print(f"Roles iteration: {i}")
        row = {
            'ID': i,
            'Name': roles[i]
        }
        data.append(row)
    return data


# PARTICIPATIONS
def participations():
    data = []
    participation_id = 0
    for room in range(records_nb.ROOMS):
        # pre-pick random participants to avoid multiple instances of one profile in the same room
        participants_count = random.randint(3, 30)
        selected_profiles = random.sample(range(records_nb.PROFILES), participants_count)

        for participant in range(participants_count):
            print(f"Participations iteration: {participation_id}")
            role = 0 if participant < 2 else 1
            startdate_raw = fake.date_this_century()
            days_to_add = random.randint(5, 180)
            enddate = startdate_raw + timedelta(days=days_to_add)
            row = {
                'ID': participation_id,
                'FK_Room': room,
                'FK_ParticipantProfile': selected_profiles[participant],
                'FK_Role': role,
                'DateOfParticipationStart': startdate_raw.strftime(date_format),
                'DateOfParticipationEnd': enddate if random.random() < 0.1 else None
            }
            data.append(row)
            participation_id += 1
    return data


# NOTIFICATIONS
def notifications():
    data = []
    for i in range(records_nb.NOTIFICATIONS):
        print(f"Notifications iteration: {i}")
        row = {
            'ID': i,
            'Content': fake.text(max_nb_chars=100)[:-1],
            'FK_Profile': random.randint(0, records_nb.PROFILES - 1)
        }
        data.append(row)
    return data


# ALBUMS
def albums():
    data = []
    for i in range(records_nb.ALBUMS):
        print(f"Albums iteration: {i}")
        row = {
            'ID': i,
            'Name': fake.text(max_nb_chars=50)[:-1],
            'FK_Profile': random.randint(0, records_nb.PROFILES-1)
        }
        data.append(row)
    return data


# EXTENSIONS
def extensions():
    data = []
    for i in range(records_nb.EXTENSIONS):
        print(f"Extensions iteration: {i}")
        ext = fake.file_extension()
        while len(ext) > 5:
            ext = fake.file_extension()
        row = {
            'ID': i,
            'Name': ext
        }
        data.append(row)
    return data


# MEDIA
def media():
    data = []

    for i in range(records_nb.MEDIA):
        print(f"Media iteration: {i}")
        path = fake.text(max_nb_chars=500)
        row = {
            'ID': i,
            'PathToResource': path[:500],
            'Size': random.randint(1, 10_000),
            'FK_Extension': random.randint(0, records_nb.EXTENSIONS-1),
            'FK_Album': random.randint(0, records_nb.ALBUMS-1) if random.random() < 0.15 else None
        }
        data.append(row)
    return data


# PUBLICATIONS
def publications():
    data = []
    for i in range(records_nb.PUBLICATIONS):
        print(f"Publications iteration: {i}")
        row = {
            'ID': i,
            'FK_Media': random.randint(0, records_nb.MEDIA-1),
            'FK_Post': random.randint(0, records_nb.POSTS-1)
        }
        data.append(row)
    return data


# SHARES
def shares():
    data = []
    shares_check = set()
    for i in range(records_nb.SHARES):
        print(f"Shares iteration: {i}")
        profile = random.randint(0, records_nb.PROFILES-1)
        post = random.randint(0, records_nb.POSTS-1)
        share_check = frozenset((profile, post))
        while share_check in shares_check:
            profile = random.randint(0, records_nb.PROFILES-1)
            post = random.randint(0, records_nb.POSTS-1)
            share_check = frozenset((profile, post))
        shares_check.add(share_check)
        row = {
            'ID': i,
            'FK_Profile': profile,
            'FK_Post': post,
            'DateOfSharing': fake.date_this_century().strftime(date_format)
        }
        data.append(row)
    return data


# PERMISSIONS
def permissions():
    data = []
    permissions = ['Group Admin', 'Group Moderator', 'Group User']
    for i in range(len(permissions)):
        print(f"Permissions iteration: {i}")
        row = {
            'ID': i,
            'Name': permissions[i],
        }
        data.append(row)
    return data


# AFFILIATIONS
def affiliations():
    data = []
    id_counter = 0
    for group in range(records_nb.GROUPS):
        affiliations_count = random.randint(3, 30)
        selected_profiles = random.sample(range(records_nb.PROFILES), affiliations_count)

        for affiliation in range(affiliations_count):
            print(f"Affiliations iteration: {id_counter}")
            permission = 0 if affiliation < 1 else (1 if abs(random.gauss(0, 1)) > 1.8 else 2)
            startdate = fake.date_this_century()
            days_to_add = random.randint(5, 180)
            enddate = startdate + timedelta(days=days_to_add)
            row = {
                'ID': id_counter,
                'FK_Profile': selected_profiles[affiliation],
                'FK_Group': group,
                'DateOfJoining': startdate.strftime(date_format),
                'DateOfLeaving': enddate.strftime(date_format) if random.random() < 0.1 else None,
                'FK_Permission': permission
            }
            data.append(row)
            id_counter += 1
    return data


# MESSAGES
def messages(chats, participations, media):

    #media_search_order = random.shuffle([i for i in range(len(media))])
    def find_profile_media(profile_id):
        search_order = [i for i in range(len(media))]
        random.shuffle(search_order)
        for i in search_order:
            if media[i]['FK_Album'] == None:
                return media[i]['ID']
        return -1 # no media found :(
    
    def get_media_and_content(profile_id):
        curr_media = None
        content = None
        if random.random() < 0.05: # only media
            curr_media = find_profile_media(profile_id)
            if curr_media == -1:
                curr_media = None
                content = fake.text(max_nb_chars=5000)
        else: # only content
            content = fake.text(max_nb_chars=5000)
        return curr_media, content
    
    data = []
    current_id = 0

    # chat_messages_nb = int(random.gauss(0.5, 0.1) * records_nb.MESSAGES)
    # participations_messages_nb = records_nb.MESSAGES - chat_messages_nb

    message_nb_per_person = records_nb.MESSAGES / (len(chats)*2 + len(participations))
    created_messages = 0
    created_messages_float = 0

    for i in range(len(chats)):
        chat = chats[i]

        created_messages_float += message_nb_per_person
        messages_to_create = int(created_messages_float) - created_messages
        created_messages += messages_to_create

        messages_to_create = int(random.gauss(messages_to_create, messages_to_create*0.6))

        for _ in range(messages_to_create):
            print(f"Messages iteration: {current_id}")
            sender = chat['FK_Sender' if random.random()>0.5 else 'FK_Receiver']
            curr_media, content = get_media_and_content(sender)
            row = {
                'ID': current_id,
                'FK_Sender': sender,
                'FK_Chat': chat['ID'],
                'FK_Room': None,
                'FK_Media': curr_media,
                'Content': content,
                'Date': fake.date_this_century().strftime(date_format)
            }
            data.append(row)
            current_id += 1

    for i in range(len(participations)):
        participation = participations[i]

        created_messages_float += message_nb_per_person
        messages_to_create = int(created_messages_float) - created_messages
        created_messages += messages_to_create

        for _ in range(messages_to_create):
            print(f"Messages iteration: {current_id}")
            room = participation['FK_Room']
            sender = participation['FK_ParticipantProfile']
            curr_media, content = get_media_and_content(sender)
            row = {
                'ID': current_id,
                'FK_Sender': sender,
                'FK_Chat': None,
                'FK_Room': room,
                'FK_Media': curr_media,
                'Content': content,
                'Date': fake.date_this_century().strftime(date_format)
            }
            data.append(row)
            current_id += 1

    return data
'''
-- Tabela: Messages
CREATE TABLE Messages (
    ID              INTEGER NOT NULL UNIQUE GENERATED BY DEFAULT AS IDENTITY,
    FK_Sender       INTEGER NOT NULL,
    FK_Chat         INTEGER,
    FK_Room         INTEGER,
    FK_Media        INTEGER,
    Content         VARCHAR(5000) CHECK (LENGTH(Content) > 0),
    Date            DATE DEFAULT CURRENT_DATE CHECK (Date <= CURRENT_DATE),
    PRIMARY KEY (ID),
    FOREIGN KEY (FK_Sender) REFERENCES Profiles(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (FK_Chat) REFERENCES Chats(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (FK_Room) REFERENCES Rooms(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (FK_Media) REFERENCES Media(ID) ON DELETE SET NULL ON UPDATE CASCADE
);
'''

def main():
    pass

if __name__ == "__main__":
    main()
