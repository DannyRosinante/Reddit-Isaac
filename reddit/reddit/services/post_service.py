import random
from entities.post import Post
from utils.file_handler import read_csv, write_csv, append_with_newline, ensure_file_exists

POSTS_FILE = "posts.csv"
HEADER = "id,title,content,author,likes"


def _get_existing_ids():
    """Devuelve un set con todos los IDs de posts existentes."""
    lines = read_csv(POSTS_FILE)
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
        pid = random.randint(0, 100_000)
        if pid not in existing:
            return pid


def create_post(title, content, author):
    ensure_file_exists(POSTS_FILE, HEADER)
    pid = _generate_unique_id()
    likes = 0
    append_with_newline(POSTS_FILE, f"{pid},{title},{content},{author},{likes}")
    return Post(title, content, author, likes, pid)


def read_post(id):
    lines = read_csv(POSTS_FILE)
    for line in lines:
        values = line.split(",")
        if len(values) >= 5:
            try:
                currentID = int(values[0])
            except ValueError:
                continue
            if currentID == id:
                return Post(values[1], values[2], values[3], int(values[4]), int(values[0]))
    return None


def read_all_posts():
    lines = read_csv(POSTS_FILE)
    posts = []
    for line in lines:
        values = line.split(",")
        if len(values) >= 5:
            try:
                posts.append(Post(values[1], values[2], values[3], int(values[4]), int(values[0])))
            except ValueError:
                continue
    return posts


def update_post(id, title=None, content=None, likes=None):
    lines = read_csv(POSTS_FILE)
    new_lines = []
    found = False
    current_title = None
    current_content = None
    current_author = None
    current_likes = None

    for line in lines:
        values = line.split(",")
        if len(values) >= 5:
            try:
                currentID = int(values[0])
            except ValueError:
                new_lines.append(line)
                continue
            if currentID == id:
                current_title = values[1]
                current_content = values[2]
                current_author = values[3]
                current_likes = int(values[4])

                if title is not None:
                    current_title = title
                if content is not None:
                    current_content = content
                if likes is not None:
                    current_likes = likes

                new_lines.append(f"{id},{current_title},{current_content},{current_author},{current_likes}")
                found = True
            else:
                new_lines.append(line)
    if not found:
        return None

    write_csv(POSTS_FILE, HEADER, new_lines)
    return Post(current_title, current_content, current_author, current_likes, id)


def delete_post(id):
    lines = read_csv(POSTS_FILE)
    new_lines = []
    found = False
    for line in lines:
        values = line.split(",")
        if len(values) >= 5:
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
    write_csv(POSTS_FILE, HEADER, new_lines)
    return Post(None, None, None, None, id)


def add_like_to_post(id):
    """Incrementa los likes de un post en 1."""
    post = read_post(id)
    if post is None:
        return None
    return update_post(id, likes=post.likes + 1)
