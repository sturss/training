from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Movie(Model):
    id = columns.UUID(primary_key=True)
    title = columns.Text(required=True)
    release_date = columns.Date(required=True)


models = (Movie,)
