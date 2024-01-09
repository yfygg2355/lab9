from app import app
from PIL import Image
import secrets
import os


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext;
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    size = (150, 150)
    image = Image.open(form_picture)
    image.thumbnail(size)
    image.save(picture_path)
    return picture_fn