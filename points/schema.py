from marshmallow import Schema, fields, validates, ValidationError

class TransactionSchema(Schema):
    payer = fields.Str(required=True, error_messages={"required": "payer is required."})
    points = fields.Integer(required=True, error_messages={"required": "points is required."})
    timestamp = fields.DateTime(required=True, error_messages={"required": "timestamp is required."})



class PointsSchema(Schema):
    points = fields.Integer(required=True, error_messages={"required": "points is required."})

    @validates("points")
    def validate_points(self, value):
        if value < 0:
            raise ValidationError("Points must be greater than 0.")