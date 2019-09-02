from marshmallow import Schema, fields, ValidationError, validates_schema

class Retrieve(Schema):
    class Meta:
        strict = True

    # valid date range:
    # start_date = 2019-07-01
    # end_date = 2019-07-31

    start_date = fields.Str(required=True, location='json')
    end_date = fields.Str(required=True, location='json')
    num_leaders = fields.Integer(required=True, location='json')
