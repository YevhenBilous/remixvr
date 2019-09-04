import datetime as dt
import secrets

from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import current_user, jwt_required, jwt_optional
from marshmallow import fields
from sqlalchemy.exc import IntegrityError

from remixvr.database import db
from remixvr.exceptions import InvalidUsage
from remixvr.classroom.models import Classroom

from .models import Activity
from .serializers import activity_schema, activities_schema

blueprint = Blueprint('activities', __name__)


@blueprint.route('/api/activities', methods=('GET',))
@jwt_required
@marshal_with(activities_schema)
def get_activities_by_reactions():
    profile = current_user.profile
    # activities = Activity.query.filter_by(is_reaction=False).all()
    activities = Activity.query.join(Activity.classroom).filter(
        Classroom.teacher != profile).all()
    return activities


@blueprint.route('/api/activity/<code>', methods=('GET',))
@jwt_optional
@marshal_with(activity_schema)
def get_activity(code):
    activity = Activity.query.filter_by(code=code).first()
    if not activity:
        raise InvalidUsage.item_not_found()
    return activity


@blueprint.route('/api/activity', methods=('POST',))
@jwt_required
@use_kwargs(activity_schema)
@marshal_with(activity_schema)
def create_activity(classroom_slug, activity_name, activity_type_id, **kwargs):
    classroom = Classroom.query.filter_by(slug=classroom_slug).first()
    if not classroom:
        raise InvalidUsage.classroom_not_found()
    while True:
        code = secrets.token_hex(3)
        existing_activity = Activity.query.filter_by(code=code).first()
        if not existing_activity:
            break
    try:
        activity = Activity(activity_type_id=activity_type_id,
                            activity_name=activity_name, classroom=classroom, code=code)
        if 'reaction_to_id' in kwargs:
            reaction_to = Activity.get_by_id(kwargs['reaction_to_id'])
            activity.reaction_to = reaction_to
            activity.is_reaction = True
        activity.save()
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.item_already_exists()
    return activity


@blueprint.route('/api/activity/classroom/<classroom_slug>/activity/<code>/reactions', methods=('GET',))
@jwt_required
@use_kwargs(activity_schema)
@marshal_with(activities_schema)
def get_activity_reactions(classroom_slug, code):
    classroom = Classroom.query.filter_by(slug=classroom_slug).first()
    if not classroom:
        raise InvalidUsage.classroom_not_found()
    activity = Activity.query.filter_by(classroom=classroom, code=code).first()
    if not activity:
        raise InvalidUsage.item_not_found()
    return activity.reactions


@blueprint.route('/api/activities/classroom/<classroom_slug>', methods=('GET',))
@jwt_required
@use_kwargs(activity_schema)
@marshal_with(activities_schema)
def get_classroom_activities(classroom_slug):
    classroom = Classroom.query.filter_by(slug=classroom_slug).first()
    if not classroom:
        raise InvalidUsage.classroom_not_found()
    return Activity.query.filter_by(classroom=classroom).all()
