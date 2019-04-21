import marshmallow as ma


class CLIRepoSchema(ma.Schema):
    project_name = ma.fields.Str(required=True)
    project_id = ma.fields.Int(required=True)
    host_type = ma.fields.Str(required=True)
    token_from = ma.fields.Str()
    grooming_rules = ma.fields.List(ma.fields.Str())


class CLIGroomingRuleSchema(ma.Schema):
    author = ma.fields.Str()
    older_than = ma.fields.Int()
    newer_than = ma.fields.Int()
    name = ma.fields.Str()
    merged = ma.fields.Bool()
