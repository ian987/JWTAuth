from sqlalchemy import MetaData
from databases import Database
from constants import DATABASE_URL

database = Database(DATABASE_URL)
metadata = MetaData()