from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    mobile = fields.Str(required=True)

def validate_user(data):
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return err.messages
    return None

class ExpenseSchema(Schema):
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    method = fields.Str(required=True)
    splits = fields.List(fields.Dict(), required=True)

def validate_expense(data):
    try:
        ExpenseSchema().load(data)
    except ValidationError as err:
        return err.messages
    return None

def validate_split(splits):
    total_percentage = sum([split.get('percentage', 0) for split in splits])
    if total_percentage != 100:
        return {"message": "Percentages must add up to 100%"}
    return None
