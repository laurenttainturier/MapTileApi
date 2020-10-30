import os
import google.auth.transport.requests
import google.oauth2.id_token
from google.cloud import storage
from flask import Flask, send_file, request
from uuid import uuid4

app = Flask(__name__)
DEFAULT_DIR = 'images'

storage_client = storage.Client.from_service_account_json("map-catacombes-firebase-adminsdk-ilo4o-a60d85d706.json")
bucket_name = "map-catacombes.appspot.com"

for subdir, dirs, files in os.walk(DEFAULT_DIR):
    if subdir.startswith('images/17') or subdir.startswith('images/18'):
        for file in files:
            local_file = os.path.join(subdir, file)
            print(local_file)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(local_file)
            new_token = uuid4()
            metadata = {'firebaseStorageDownloadTokens': new_token}
            blob.metadata = metadata
            blob.upload_from_filename(local_file, content_type='image/png')

HTTP_REQUEST = google.auth.transport.requests.Request()


class Unauthorized(Exception):
    pass


def wraps(old_function):
    def new_function(*args, **kwargs):
        try:
            return old_function(*args, **kwargs)
        except Unauthorized as e:
            return f"Unauthorized: {e}", 401
        except Exception as e:
            return f"Unexpected error: {e}", 500

    return new_function


def authentication_required(old_function):
    def new_function(*args, **kwargs):
        try:
            id_token = request.headers['Authorization'].split(' ').pop()
            claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST, 'map-catacombes')
            if not claims:
                raise Unauthorized("Invalid token id")
            return old_function(*args, **kwargs)
        except KeyError:
            raise Unauthorized("Missing authorization parameter")

    return new_function


@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/image/<string:image_id>/zoom/<int:zoom>/<int:x>/<int:y>')
def get_zoom_image(image_id: str, zoom: int, x: int, y: int):
    try:
        return send_file(os.path.join(DEFAULT_DIR, f'{zoom}/{x}/{y}.png'), mimetype='image/png')
    except FileNotFoundError:
        return 'Not found', 404


@app.route('/image/<string:image_id>/zoom')
@wraps
@authentication_required
def get_zoom_characteristic(image_id: str):
    return {
        zoom_level: get_zoom_bounds(zoom_level) for zoom_level in filter(filter_directory, os.listdir(DEFAULT_DIR))
    }


def filter_directory(candidate_directory: str) -> bool:
    return os.path.isdir(os.path.join(DEFAULT_DIR, candidate_directory))


def convert_to_int(file: str):
    return int(file.split('.png')[0])


def get_zoom_bounds(zoom_level):
    zoom_level_directory = os.path.join(DEFAULT_DIR, zoom_level)
    x_tiles_dir = os.listdir(zoom_level_directory)
    x_tiles = list(map(int, x_tiles_dir))
    y_tiles_file = [list(map(convert_to_int, os.listdir(os.path.join(zoom_level_directory, x_dir)))) for x_dir in x_tiles_dir]

    return {
        'xMax': max(x_tiles),
        'xMin': min(x_tiles),
        'yMax': max(map(max, y_tiles_file)),
        'yMin': min(map(min, y_tiles_file)),
    }


if __name__ == '__main__':
    print('hello world')
    # app.run()
