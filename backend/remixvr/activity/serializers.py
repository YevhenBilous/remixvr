from marshmallow import Schema, fields, pre_load, post_dump

from remixvr.activitytype.serializers import ActivityTypeSchema
from remixvr.classroom.serializers import ClassroomSchema


class ActivitySchema(Schema):
    id = fields.Int()
    activity_name = fields.Str()
    activity_type = fields.Nested(ActivityTypeSchema, only=[
                                  'pdf_link', 'slug', 'title', 'id'])
    activity_type_id = fields.Int(load_only=True)
    classroom = fields.Nested(ClassroomSchema, only=[
                              'classname', 'slug', 'school'])
    classroom_slug = fields.Str(load_only=True)
    code = fields.Str()
    is_reaction = fields.Bool()
    submissions_count = fields.Int()
    reaction_to_id = fields.Int(load_only=True)
    reaction_to = fields.Nested('self', only=['code', 'classroom.school'])
    reactions = fields.Nested('self', default=None, many=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        strict = True


class ActivitySchemas(ActivitySchema):

    @post_dump(pass_many=True)
    def dump_activities(self, data, many):
        return {'activities': data, 'activitiesCount': len(data)}


activity_schema = ActivitySchema()
activities_schema = ActivitySchemas(many=True)
