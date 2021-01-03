from marshmallow import Schema, fields


class TestSchema(Schema):
    val = fields.Str(required=True)
