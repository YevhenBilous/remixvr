from .models import (Field, Position, Text, Number, Select, Audio, Video,
                     VideoSphere, Image, PhotoSphere, File, Link, Color, Object)
from flask_jwt_extended import current_user
from flask import current_app as app
from urllib.parse import urlparse, unquote
from .models import File
from remixvr.exceptions import InvalidUsage

import urllib.request
import os
import json


def generate_fields(space, fields):
    for field in fields:
        if field['type'] == 'text':
            new_field = Text(
                space=space, author=current_user.profile, label=field['label'])
        if field['type'] == 'number':
            new_field = Number(
                space=space, author=current_user.profile, label=field['label'])
        if field['type'] == 'select':
            new_field = Select(
                space=space, author=current_user.profile, label=field['label'], possible_values=field['possible_values'])
        if field['type'] == 'audio':
            new_field = Audio(
                space=space, author=current_user.profile, label=field['label'])
        if field['type'] == 'photosphere':
            new_field = PhotoSphere(
                space=space, author=current_user.profile, label=field['label'])
        if field['type'] == 'image':
            new_field = Image(
                space=space, author=current_user.profile, label=field['label'])
        if field['type'] == 'video':
            new_field = Video(
                space=space, author=current_user.profile, label=field['label'])
        if field['type'] == 'videosphere':
            new_field = VideoSphere(
                space=space, author=current_user.profile, label=field['label'])
        if field['type'] == 'color':
            new_field = Color(
                space=space, author=current_user.profile, label=field['label'])
        if field['type'] == 'object':
            new_field = Object(
                space=space, author=current_user.profile, label=field['label'])
        new_field.save()


def check_file_extension_for_type(type, file_extension):
    if type == 'image' or type == 'photosphere':
        if file_extension not in ['.png', '.jpg', '.jpeg']:
            raise InvalidUsage.invalid_file_type()
    elif type == 'audio':
        if file_extension not in ['.mp3']:
            raise InvalidUsage.invalid_file_type()
    elif type == 'video' or type == 'videosphere':
        if file_extension not in ['.mp4', '.mov']:
            raise InvalidUsage.invalid_file_type()


def save_object_files(folder, main_object_file, object_files, thumbnail):
    folder_path = os.path.join(app.root_path,
                               app.config['UPLOAD_FOLDER'], folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    os.chdir(folder_path)

    main_parsed_url = urlparse(main_object_file)
    main_filename = unquote(os.path.basename(main_parsed_url.path))

    object_files.append(main_object_file)
    object_files_urls = []

    if thumbnail is not None:
        saved_file = urllib.request.urlretrieve(thumbnail, 'thumbnail.png')
        url = '/uploads/{}/{}'.format(folder, 'thumbnail.png')
        file_object = File(filename='thumbnail.png', url=url,
                           filesize=saved_file[1]['Content-Length'])
        file_object.save()

    for object_file in object_files:
        parsed_url = urlparse(object_file)
        filename = unquote(os.path.basename(parsed_url.path))
        saved_file = urllib.request.urlretrieve(object_file, filename)
        url = '/uploads/{}/{}'.format(folder, filename)
        object_files_urls.append(url)
        file_object = File(filename=filename, url=url,
                           filesize=saved_file[1]['Content-Length'])
        file_object.save()
    object_path = '/uploads/{}/'.format(folder)
    return object_path, main_filename, object_files_urls
