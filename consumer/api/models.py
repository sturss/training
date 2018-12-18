import uuid
from datetime import datetime

import sqlalchemy as sql
from sqlalchemy.dialects.postgresql import UUID

metadata = sql.MetaData()
Movie = sql.Table(
    'movie',
    metadata,
    sql.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    sql.Column('title', sql.String, nullable=False),
    sql.Column('release_date', sql.Date, nullable=True),
    sql.Column('created_on', sql.DateTime, default=datetime.utcnow, nullable=False)
)

models = (Movie, )

