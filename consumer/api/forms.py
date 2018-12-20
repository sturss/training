"""
    Module with Marshmallow forms for data validation
"""

from marshmallow import Schema, fields


class MovieForm(Schema):
    title = fields.String(required=True)
    release_date = fields.Date(required=True)
