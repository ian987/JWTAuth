from sqlalchemy import Table, Column, Integer, String, Text
from database import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(200), unique=True),
    Column("password", String(300), nullable=False ),
    Column("role", String(10), default="User")
)
