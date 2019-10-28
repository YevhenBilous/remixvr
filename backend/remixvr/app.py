# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from remixvr.extensions import bcrypt, cache, db, migrate, jwt, cors

from remixvr import (commands, user, profile, project, theme, field,
                     space, activity, activitytype, classroom, school, submission)
from remixvr.settings import ProdConfig
from remixvr.exceptions import InvalidUsage
from raven.contrib.flask import Sentry


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    sentry = Sentry(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(user.views.blueprint, origins=origins)
    cors.init_app(profile.views.blueprint, origins=origins)
    cors.init_app(project.views.blueprint, origins=origins)
    cors.init_app(theme.views.blueprint, origins=origins)
    cors.init_app(field.views.blueprint, origins=origins)
    cors.init_app(space.views.blueprint, origins=origins)
    cors.init_app(activity.views.blueprint, origins=origins)
    cors.init_app(activitytype.views.blueprint, origins=origins)
    cors.init_app(classroom.views.blueprint, origins=origins)
    cors.init_app(school.views.blueprint, origins=origins)
    cors.init_app(submission.views.blueprint, origins=origins)

    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(profile.views.blueprint)
    app.register_blueprint(project.views.blueprint)
    app.register_blueprint(theme.views.blueprint)
    app.register_blueprint(field.views.blueprint)
    app.register_blueprint(space.views.blueprint)
    app.register_blueprint(activity.views.blueprint)
    app.register_blueprint(activitytype.views.blueprint)
    app.register_blueprint(classroom.views.blueprint)
    app.register_blueprint(school.views.blueprint)
    app.register_blueprint(submission.views.blueprint)


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User,
            'UserProfile': profile.models.UserProfile,
            'Project': project.models.Project,
            'Theme': theme.models.Theme,
            'Field': field.models.Field,
            'Position': field.models.Position,
            'Text': field.models.Text,
            'Number': field.models.Number,
            'Audio': field.models.Audio,
            'Video': field.models.Video,
            'VideoSphere': field.models.VideoSphere,
            'Image': field.models.Image,
            'PhotoSphere': field.models.PhotoSphere,
            'Space': space.models.Space,
            'Activity': activity.models.Activity,
            'ActivityType': activitytype.models.ActivityType,
            'Classroom': classroom.models.Classroom,
            'School': school.models.School,
            'Submission': submission.models.Submission
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
