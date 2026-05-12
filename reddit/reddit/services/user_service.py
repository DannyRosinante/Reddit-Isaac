import random
from entities.user import User
from utils.file_handler import read_csv, write_csv, append_with_newline

USERS_FILE = "users.csv"
HEADER = "id,name,password"


def _get_existing_ids():
    """Devuelve un set con todos los IDs de usuarios existentes."""
    lines = read_csv(USERS_FILE)
    ids = set()
    for line in lines:
        parts = line.split(",")
        if parts:
            try:
                ids.add(int(parts[0]))
            except ValueError:
                continue
    return ids


def _generate_unique_id():
    existing = _get_existing_ids()
    while True:
        uid = random.randint(0, 100_000)
        if uid not in existing:
            return uid


def create_user(name, password):
    uid = _generate_unique_id()
    append_with_newline(USERS_FILE, f"{uid},{name},{password}")
    return User(name, password, uid)


def read_user(id):
    lines = read_csv(USERS_FILE)
    for line in lines:
        values = line.split(",")
        if len(values) >= 3:
            try:
                currentID = int(values[0])
            except ValueError:
                continue
            if currentID == id:
                return User(values[1], values[2], int(values[0]))
    return None


def read_all_users():
    lines = read_csv(USERS_FILE)
    users = []
    for line in lines:
        values = line.split(",")
        if len(values) >= 3:
            try:
                users.append(User(values[1], values[2], int(values[0])))
            except ValueError:
                continue
    return users


def update_user(name, password, id):
    lines = read_csv(USERS_FILE)
    new_lines = []
    found = False
    for line in lines:
        values = line.split(",")
        if len(values) >= 3:
            try:
                currentID = int(values[0])
            except ValueError:
                new_lines.append(line)
                continue
            if currentID == id:
                new_lines.append(f"{id},{name},{password}")
                found = True
            else:
                new_lines.append(line)
    if not found:
        return None
    write_csv(USERS_FILE, HEADER, new_lines)
    return User(name, password, id)


def delete_user(id):
    lines = read_csv(USERS_FILE)
    new_lines = []
    found = False
    for line in lines:
        values = line.split(",")
        if len(values) >= 3:
            try:
                currentID = int(values[0])
            except ValueError:
                new_lines.append(line)
                continue
            if currentID == id:
                found = True
            else:
                new_lines.append(line)
    if not found:
        return None
    write_csv(USERS_FILE, HEADER, new_lines)
    return User(None, None, id)
